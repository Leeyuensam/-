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
model = joblib.load('anti_fraud_model.pkl')  # 反欺诈模型
model2 = joblib.load('regr.pkl')  # 信用分模型
model3 = joblib.load('logit.pkl')  # 贷中模型
model4 = joblib.load('AfterLoan.pkl')  # 贷后模型

# Create your views here.

'''
反欺诈队列  url = http://127.0.0.1:8000/loan_approval
'''


# 欺诈队列
class AntiFraudList_yes(APIView):
    def get(self, request):
        data = pd.DataFrame(list(Anti_Fraud_Yes.objects.filter(status=None).values()))

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
        data.drop(['sid', 'nginxtime', 'ip', 'reqrealip', 'id', 'label', 'status'], axis=1, inplace=True)
        # 预测label
        result_label = model.predict(data)
        print(result_label)
        queryset = Anti_Fraud_Yes.objects.all().values_list('sid', 'ip', 'city')
        json_list = []
        flag = 0
        for i in queryset:
            label = result_label[flag]
            if label == 1:
                dic = {'sid': i[0],
                       'ip': i[1],
                       'city': i[2],
                       'label': label
                       }
                json_list.append(dic)
            flag += 1
        return Response(json_list)


'''
    url = http://127.0.0.1:8000/loan_approval/AntiFraudList_no
'''


# 非欺诈队列
class AntiFraudList_no(APIView):
    def get(self, request):
        data = pd.DataFrame(list(Anti_Fraud_Yes.objects.filter(status=None).values()))

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
        data.drop(['sid', 'nginxtime', 'ip', 'reqrealip', 'id', 'label', 'status'], axis=1, inplace=True)
        # 预测label
        result_label = model.predict(data)
        print(result_label)
        queryset = Anti_Fraud_Yes.objects.all().values_list('sid', 'ip', 'city')
        json_list = []
        flag = 0
        for i in queryset:
            label = result_label[flag]
            if label == 0:
                dic = {'sid': i[0],
                       'ip': i[1],
                       'city': i[2],
                       'label': label
                       }
                json_list.append(dic)
            flag += 1
        return Response(json_list)


'''
    接受通过反欺诈 url = http://127.0.0.1:8000/loan_approval/pass_approval
    接收数据形式：
    {
      "sid":"person_1"
    }
'''


class pass_approval(APIView):
    def post(self, request):
        # status为1时是通过反欺诈模型
        try:
            Anti_Fraud_Yes.objects.filter(sid=request.data.get('sid')).update(status='1')
            return Response({'mes': 'accept'})
        except:
            return Response(request.data)


'''
    拒绝通过反欺诈  url:http://127.0.0.1:8000/loan_approval/reject_approval
    接收数据形式：
    {
      "sid":"person_1"
    }
'''


class reject_approval(APIView):
    def post(self, request):
        # status为0时是不通过反欺诈模型
        try:
            Anti_Fraud_Yes.objects.filter(sid=request.data.get('sid')).update(status='0')
            return Response({'mes': 'reject'})
        except:
            return Response(request.data)


'''
    信用等级模型 url = http://127.0.0.1:8000/loan_approval/credit_lavel
'''


class CreditLevelList(APIView):
    def get(self, request):
        id_list = []
        id_data = Anti_Fraud_Yes.objects.filter(status=1).values('sid')
        # print(id_data)
        for x in id_data:
            # print(x)
            id_list.append(x['sid'])
        # print(id_list)
        json_list = []
        for x in id_list:
            data = pd.DataFrame(list(CreditLevelPredict.objects.filter(user_id=x).values()))
            print(data)
            data.drop(['user_id', 'id'], axis=1, inplace=True)
            result_prob = model2.predict_proba(data)
            result_label = result_prob[:, 0]
            # print(result_label)
            queryset = CreditLevel.objects.filter(user_id=x)
            print(queryset)
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
    贷中模型
'''


class behaviour_score(APIView):
    def get(self, request):
        data = pd.DataFrame(list(BehaviorScore.objects.all().values()))
        data.set_index(['CUST_ID'], inplace=True)
        data1 = data.copy()
        data1.drop(['id', 'Loan_Amount', 'OS', 'Payment', 'Spend', 'delq', 'label'], axis=1, inplace=True)
        print(data1.head())
        # print(data.columns)
        label = model3.predict(data1)
        print(label)
        json_list = []
        flag = 0
        for index, i in data.iterrows():
            dic = {
                'user_id': index,
                'Loan_Amount': i['Loan_Amount'],
                'OS': i['OS'],
                'Payment': i['Payment'],
                'Spend': i['Spend'],
                'delq': i['delq'],
                'label': label[flag]
            }
            json_list.append(dic)
            flag += 1
        return Response(json_list)


'''
    贷后模型
'''


class after_loan(APIView):
    def get(self, request):
        data = pd.DataFrame(list(AfterLoan.objects.all().values()))
        data.set_index(['ListingKey'], inplace=True)
        data1 = data.copy()
        data1.drop(['label', 'id', 'CreditGrade', 'Term', 'EmploymentStatus'], axis=1, inplace=True)
        print(data1.head())
        label = model4.predict(data1)
        print(label)
        json_list = []
        flag = 0
        for index, i in data.iterrows():
            dic = {
                'ListingKey': index,
                'CreditGrade': i['CreditGrade'],
                'Term': i['Term'],
                'EmploymentStatus': i['EmploymentStatus'],
                'label': label[flag]
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
            print(ret)
            return Response(ret)
        else:
            mes = 'CAN NOT FOUND'
            return Response({"mes": mes})

# Create your views here.
