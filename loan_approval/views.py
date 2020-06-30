from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from loan_approval.models import *
from loan_approval.serializers import AntiFraudSerializer, CreditScoreSerializer
import joblib
import xgboost
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
from sklearn.ensemble import RandomForestClassifier
from py2neo import Graph
from loan_approval.graphUtils import demotest, graphCU, graphEva, graphService

# 导入模型
model = joblib.load('anti_fraud_model.pkl')
model2 = joblib.load('regr.pkl')

# Create your views here.

'''
反欺诈队列  url = http://127.0.0.1:8000/loan_approval
'''


class AntiFraudList(APIView):

    def get(self, request):

        data = pd.DataFrame(list(Anti_Fraud_Yes.objects.all().values()))

        def one_hot_col(col):
            """标签编码"""
            lbl = LabelEncoder()
            lbl.fit(col)
            return lbl

        object_cols = list(data.dtypes[data.dtypes == np.object].index)
        # 返回字段名为object类型的字段
        # 对object类型的字段进行标签编码：
        for col in object_cols:
            if col != 'sid':
                data[col] = one_hot_col(data[col].astype(str)).transform(data[col].astype(str))
        data.drop(['sid', 'nginxtime', 'ip', 'reqrealip', 'id', 'label'], axis=1, inplace=True)

        # 预测label
        result_label = model.predict(data)

        queryset = Anti_Fraud_Yes.objects.all()
        json_list = []
        flag = 0
        for i in queryset:
            label = result_label[flag]
            dic = {'sid': i.sid,
                   'ip': i.ip,
                   'city': i.city,
                   'label': label
                   }
            json_list.append(dic)
            flag += 1

        return Response(json_list)

    def post(self, request):
        data = AntiFraudSerializer(data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)


'''
    信用等级模型 url = http://127.0.0.1:8000/loan_approval/credit_lavel
'''


class CreditLevelList(APIView):
    def get(self, request):
        data = pd.DataFrame(list(CreditLevelPredict.objects.all().values()))
        data.drop(['user_id', 'id'], axis=1, inplace=True)
        result_prob = model2.predict_proba(data)
        result_label = result_prob[:, 0]

        queryset = CreditLevel.objects.all()
        json_list = []
        flag = 0

        for i in queryset:
            level = result_label[flag]
            final_label = None
            if level >= 0.8:
                final_label = 'AAA'
            elif level >= 0.65:
                final_label = 'AA'
            elif level >= 0.5:
                final_label = 'A'
            elif level >= 0.35:
                final_label = 'B'
            elif level >= 0.2:
                final_label = 'C'
            else:
                final_label = 'D'
            dic = {
                'user_id': i.user_id,
                'gender': i.Gender,
                'credit_level': final_label
            }
            json_list.append(dic)
            flag += 1
        return Response(json_list)


'''
    下面是查询图数据库部分
'''


class graph_data(APIView):
    def post(self, request):
        # url = 'localhost:7474'
        # username = 'neo4j'
        # password = '123'
        # print(request.data)
        # print(request.data['value'])
        graphServiceObject = graphService.GraphService()
        # data = graphServiceObject.networkSearch(value=request.data)
        data = graphServiceObject.networkSearch(value=request.data.get('value'))
        if data != -1:
            ret = json.dumps(data)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})


'''
    neo4j统计得到的额外数据
'''


class stat_data(APIView):
    def post(self, request):
        graphServiceObject = graphService.GraphService()
        data = graphServiceObject.statExData(value=request.data.get('value'))
        if data != -1:
            ret = json.dumps(data)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})


'''
neo4j搜索用户两层内的关系网
        SPO: S为搜索的user，P为rel，O为相关联user实体
        Input: personID (避免重名)
        Return: dict(ID存在）
               -1（ID不存在）
'''


class user_relation(APIView):
    def post(self, request):
        graphServiceObject = graphService.GraphService()
        data = graphServiceObject.userRel(value=request.data.get('value'))
        if data != -1:
            ret = json.dumps(data)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})


'''
    用户手机
'''


class user_phone(APIView):
    def post(self, request):
        graphServiceObject = graphService.GraphService()
        data = graphServiceObject.userPhone(value=request.data.get('value'))
        if data != -1:
            ret = json.dumps(data)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})


'''
    用户历史交易
'''


class user_transaction(APIView):
    def post(self, request):
        graphServiceObject = graphService.GraphService()
        data = graphServiceObject.userTx(value=request.data.get('value'))
        if data != -1:
            ret = json.dumps(data)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})

# Create your views here.
