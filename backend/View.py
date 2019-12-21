from flask_restful import reqparse, Resource
from DBPostgresql import *




def buf_to_jsonstr(input_string_list):
    # res = {}
    res = []
    index = 0;
    for input_element in input_string_list:
        index += 1
        output_element = {}
        input_element = list(input_element)
        output_element["owner"] = input_element[0]
        output_element["symbol"] = input_element[1]
        output_element["note"] = input_element[2]
        output_element["latest_date"] = input_element[3].strftime('%Y-%m-%d')
        output_element["previous_date"] = input_element[5].strftime('%Y-%m-%d')
        output_element["latest_bal"] = float(input_element[4])
        output_element["previous_bal"] = float(input_element[6])
        output_element["increment"] = float(input_element[7])
        res.append(output_element)
        # res[index] = output_element
    return res


parser = reqparse.RequestParser()
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('source', type=str)


class ViewIncrement(Resource):
    def get(self):
        start_date = ""
        end_date = ""
        func_name = ""
        # DB select * from f_inc_fin('yyyy-mm-dd','yymm-mm-dd');
        args = parser.parse_args()
        if args['start_date'] and args['end_date']:
            try:
                start_date = args['start_date']
                end_date = args['end_date']
                # func_name = args['callback']
            except ValueError:
                return "invalid request {} {}".format(args['start_date'], args['end_date']), 422
        stmt = "select * from f_inc_fin('{}','{}')".format(start_date, end_date)
        buf = db.execcteSelectSQL(stmt)
        # Decimal datetime can't dump to json
        res_string = buf_to_jsonstr(buf)
        db.commit()
        return res_string, {'Access-Control-Allow-Origin': '*'}
        # return "{} ( {} )".format(func_name, (json.dumps(res_string))), {'Access-Control-Allow-Origin': '*'}


class ViewTime(Resource):
    def get(self):
        stmt = "select * from v_fiscal_date"
        buf = db.execcteSelectSQL(stmt)
        res =[]
        db.commit()
        for x in buf:
            res.append(x[0].strftime('%Y-%m-%d'))
        return res, {'Access-Control-Allow-Origin': '*'}

class ViewAccount(Resource):
    def get(self):
        args = parser.parse_args()
        condition = ""
        param = ""
        if args['source']:
            try:
                param = args['source']
            except ValueError:
                return "invalid request {}".format(args['source']), 422
        if param == "direct":
            condition = "where source = 1"
        elif param == "accumulate":
            condition = "where source = 2"
        elif param == "all":
            condition = "where 1 = 1"
        else:
            return "unrecognized param {}".format(args['source']), 422
        stmt = "select * from account {} order by account_id ".format(condition)
        buf = db.execcteSelectSQL(stmt)
        res =[]
        db.commit()
        for x in buf:
            res.append([x[1],x[3]])
        return res, {'Access-Control-Allow-Origin': '*'}