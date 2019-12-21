from flask_restful import reqparse, abort, Resource
from DBPostgresql import *


parser = reqparse.RequestParser()
parser.add_argument('source', type=str)

class Account(Resource):
    def get(self):
        start_date = ""
        end_date = ""
        func_name = ""
        #args = parser.parse_args()
        # if args['start_date'] and args['end_date']:
        #     try:
        #         start_date = args['start_date']
        #         end_date = args['end_date']
        #         # func_name = args['callback']
        #     except ValueError:
        #         return "invalid request {} {}".format(args['start_date'], args['end_date']), 422
        stmt = "select * from f_inc_fin('{}','{}')".format(start_date, end_date)
        buf = db.execcteSelectSQL(stmt)
        # Decimal datetime can't dump to json
        res_string = str(buf)
        db.commit()
        return res_string, {'Access-Control-Allow-Origin': '*'}
        # return "{} ( {} )".format(func_name, (json.dumps(res_string))), {'Access-Control-Allow-Origin': '*'}

    def post(self):
        args = parser.parse_args()
        if args['owner'] and args['bank']:
            owner = args['owner']
            bank = args['bank']
            card_no = args['card_no']
            credit = args['credit']
        else:
            return "invalid request", 402
        # DB insert
        return "POST owner {} bank {} card_no {} credit {}".format(owner, bank, card_no, credit), 201
