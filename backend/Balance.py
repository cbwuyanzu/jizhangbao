from flask import request, json, make_response
from flask_restful import reqparse, abort, Resource
from DBPostgresql import *


class Direct(Resource):
    def post(self, account):
        content = request.data
        text = str(content, encoding="utf-8")
        try:
            input_request = json.loads(text)
            fiscal_date = input_request['date']
            balance = input_request['val']
        except KeyError:
            return "key error [date] [balance] [{}]".format(text), 400
        # DB update
        stmt = "insert into balance_direct(fiscal_date, symbol, bal) values('{}', '{}', {})".format(fiscal_date,
                                                                                                    account,
                                                                                                    balance)
        print(stmt)
        # e.g insert into balance_direct(fiscal_date, symbol, bal) VALUES('2017-11-08','cjsec',3000)
        try:
            db.execcteCUDSQL(stmt)
            print("success balance")
        except Exception as e:
            return "internal error CUD db [{}]".format(e), 500
        db.commit()
        return "POST success balance {} date {} position {}".format(account, fiscal_date, balance), {
            'Access-Control-Allow-Origin': '*'}

    def options(self, account):
        headers = {
            'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Request-Method': 'POST'}
        return make_response("", 200, headers)

    def get(self, account):
        stmt = "select * from  balance_direct where symbol = '{}' order by fiscal_date desc limit 3".format(account)
        print(stmt)
        try:
            buf = db.execcteSelectSQL(stmt)
        except Exception as e:
            return "internal error query db [{}]".format(e), 500
        db.commit()
        return buf_to_jsonstr2(buf, 1), {'Access-Control-Allow-Origin': '*'}

    def delete(self, account):
        # DB insert
        return "", 204


class Accumulate(Resource):
    def post(self, account):
        content = request.data
        text = str(content, encoding="utf-8")
        try:
            input_request = json.loads(text)
            fiscal_date = input_request['date']
            transfer = input_request['val']
        except KeyError:
            return "key error [date] [balance] {}".format(text), 400
        # DB update
        stmt = "INSERT INTO balance_accumulate(fiscal_date, symbol, transfer) VALUES ('{}', '{}', {})".format(
            fiscal_date, account,
            transfer)
        print(stmt)
        # e.g INSERT INTO balance_accumulate(fiscal_date, symbol, transfer) VALUES ('2019-07-22', 'CMBC', 8607.01)
        try:
            db.execcteCUDSQL(stmt)
            print("success accumulate")
        except Exception as e:
            return "internal error CUD db {}".format(e), 500
        db.commit()
        return "POST success accumulate {} date {} position {}".format(account, fiscal_date, transfer), {
            'Access-Control-Allow-Origin': '*'}
    def options(self, account):
        headers = {
            'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Request-Method': 'POST'}
        return make_response("", 200, headers)
    def get(self, account):
        stmt = "select * from  balance_accumulate where symbol = '{}' order by fiscal_date desc limit 3".format(account)
        print(stmt)
        try:
            buf = db.execcteSelectSQL(stmt)
        except Exception as e:
            return "internal error query db [{}]".format(e), 500
        db.commit()
        return buf_to_jsonstr2(buf, 2), {'Access-Control-Allow-Origin': '*'}
    def delete(self, account):
        # DB insert
        return "", 204


def buf_to_jsonstr2(input_string_list, type):
    '''type :1 -- fiscal_date, symbol, bal, record_time
             2 -- fiscal_date, symbol, transfer, record_time'''
    # res = {}
    res = []
    index = 0
    for input_element in input_string_list:
        index += 1
        output_element = {}
        input_element = list(input_element)
        output_element["fiscal_date"] = input_element[0].strftime('%Y-%m-%d')
        output_element["symbol"] = input_element[1]
        if type == 1:
            output_element["bal"] = float(input_element[2])
        elif type == 2:
            output_element["transfer"] = float(input_element[2])
        output_element["record_time"] = input_element[3].strftime('%Y-%m-%d %H:%M:%S')
        res.append(output_element)
        # res[index] = output_element
    return res
