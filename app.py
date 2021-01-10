from flask import Flask, request, Response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from pandas_datareader import data as pdr
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
api = Api(app)
CORS(app)

task_post_args_stock = reqparse.RequestParser()
task_post_args_stock.add_argument("Stockname", type=str, help="Stockcode you want to retrieve info from.", required=True)
task_post_args_stock.add_argument("Timespan", type=int, help="The timespan in years you want to retrieve", required=True)


class FinanceInfo(Resource):
    def get(self):
        start = datetime.today()
        start = start - relativedelta(years=1)
        data = pdr.get_data_yahoo("ABI.BR", start=start, end=datetime.today())
        return data['Adj Close'].to_json(orient="index", date_format='iso')

    def post(self):
        args = task_post_args_stock.parse_args()
        stock = args.get("Stockname")
        timespan = args.get("Timespan")
        start = datetime.today()
        #start = start - relativedelta(years=1)
        start = start - relativedelta(years=timespan)
        #data = pdr.get_data_yahoo("ABI.BR", start=start, end=datetime.today())
        try:
            data = pdr.get_data_yahoo(stock, start=start, end=datetime.today())
            return data['Adj Close'].to_json(orient="index", date_format='iso')
        except:
            return Response("{'Invalid argument'}", status=403, mimetype='invalid argument')


api.add_resource(FinanceInfo, "/stock")
