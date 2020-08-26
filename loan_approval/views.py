from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from loan_approval.models import *
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
        col = ['adidmd5', 'adunitshowid', 'apptype', 'carrier', 'city', 'dvctype', 'h', 'idfamd5', 'imeimd5', 'lan',
               'macmd5', 'make', 'mediashowid', 'model', 'ntt', 'openudidmd5', 'orientation', 'os', 'osv', 'pkgname',
               'ppi', 'province', 'ver', 'w']
        data = data[col]
        # 预测label
        result_label = model.predict(data)
        queryset = Anti_Fraud_Yes.objects.filter(status=None).values_list('sid', 'ip', 'make', 'city')
        json_list = []
        flag = 0
        for i in queryset:
            label = result_label[flag]
            if label == 1:
                dic = {'sid': i[0],
                       'ip': i[1],
                       'make': i[2],
                       'city': i[3],
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
        col = ['adidmd5', 'adunitshowid', 'apptype', 'carrier', 'city', 'dvctype', 'h', 'idfamd5', 'imeimd5', 'lan',
               'macmd5', 'make', 'mediashowid', 'model', 'ntt', 'openudidmd5', 'orientation', 'os', 'osv', 'pkgname',
               'ppi', 'province', 'ver', 'w']
        data = data[col]
        # 预测label
        result_label = model.predict(data)
        queryset = Anti_Fraud_Yes.objects.filter(status=None).values_list('sid', 'ip', 'make', 'city')
        json_list = []
        flag = 0
        for i in queryset:
            label = result_label[flag]
            if label == 0:
                dic = {'sid': i[0],
                       'ip': i[1],
                       'make': i[2],
                       'city': i[3],
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
        user_data = CreditLevel.objects.filter(status=None).values('user_id')

        for x in id_data:
            id_list.append(x['sid'])
        user_list = []
        for x in user_data:
            user_list.append(x['user_id'])

        list1 = list(set(id_list).intersection(set(user_list)))
        json_list = []
        for x in list1:
            data = pd.DataFrame(list(CreditLevelPredict.objects.filter(user_id=x).values()))
            data.drop(['user_id', 'id'], axis=1, inplace=True)
            result_prob = model2.predict_proba(data)
            result_label = result_prob[:, 0]
            queryset = CreditLevel.objects.filter(user_id=x)
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
                    'sid': i.user_id,
                    'gender': i.Gender,
                    'LoanAmount': i.LoanAmount,
                    'LoanTerm': i.Loan_Amount_Term,
                    'credit_level': final_label
                }
                json_list.append(dic)
                flag += 1
        return Response(json_list)


'''
    显示贷款申请细节
    url:http://127.0.0.1:8000/loan_approval/show_details
    接收数据形式：
    {
      "user_id":"person_1"
    }
'''


class ShowDetails(APIView):
    def post(self, request):
        sid = request.data.get('user_id')
        data = CreditLevel.objects.filter(user_id=sid).values('user_id', 'Gender', 'Married', 'Education',
                                                              'Self_Employed', 'ApplicantIncome', 'LoanAmount',
                                                              'Loan_Amount_Term', 'Property_Area')
        print(data)
        json_list = []
        for i in data:
            json_list.append({
                'sid': i['user_id'],
                'gender': i['Gender'],
                'married': i['Married'],
                'edu': i['Education'],
                'selfEmployed': i['Self_Employed'],
                'income': float(i['ApplicantIncome']) * 1000,
                'LoanAmount': i['LoanAmount'],
                'LoanTerm': i['Loan_Amount_Term'],
                'propertyArea': i['Property_Area']
            })
        return Response(json_list)


'''
    允许贷款模型
    url:http://127.0.0.1:8000/loan_approval/permit_loan
    接收数据形式：
    {
      "user_id":"person_1"
    }
    
'''


class permit_loan(APIView):
    def post(self, request):
        try:
            CreditLevel.objects.filter(user_id=request.data.get('user_id')).update(status='1')
            return Response({'mes': 'accept'})
        except:
            return Response(request.data)


'''
    拒绝贷款模型
    url:http://127.0.0.1:8000/loan_approval/reject_loan
    接收数据形式：
    {
      "user_id":"person_1"
    }

'''


class reject_loan(APIView):
    def post(self, request):
        try:
            CreditLevel.objects.filter(user_id=request.data.get('user_id')).update(status='0')
            return Response({'mes': 'reject'})
        except:
            return Response(request.data)


'''
    修改贷款金额
    url:http://127.0.0.1:8000/loan_approval/edit_loan
    接收数据形式：
    {
      "user_id":"person_1"
      "loanAmount":500000
    }

'''


class edit_loan(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            loanAmount = request.data.get('loanAmount')
            loan_data = CreditLevel.objects.filter(user_id=user_id).values('LoanAmount')
            loan = None
            for i in loan_data:
                loan = i['LoanAmount']
                # 当修改金额大于原来的时候就会报错
            if float(loanAmount) > float(loan):
                return Response({'mes': 'error'})
            CreditLevel.objects.filter(user_id=user_id).update(LoanAmount=loanAmount)
            CreditLevel.objects.filter(user_id=user_id).update(status='1')
            return Response({'mes': 'accept'})
        except:
            return Response(request.data)


'''
    url:http://127.0.0.1:8000/loan_approval/behavior_score
    贷中模型
    逾期还款的概率
'''


class behaviour_score(APIView):
    def get(self, request):
        id_data = CreditLevel.objects.filter(status=1).values('user_id', 'repaymentPeriod')
        id_list = []
        # 还款期限小于0.5才进入贷中模型
        for i in id_data:
            if float(i['repaymentPeriod']) < 0.5:
                id_list.append(i['user_id'])
        json_list = []
        for x in id_list:
            data = pd.DataFrame(list(BehaviorScore.objects.filter(CUST_ID=x).values()))
            data.set_index(['CUST_ID'], inplace=True)
            data1 = data.copy()
            data1.drop(['id', 'Loan_Amount', 'OS', 'Payment', 'Spend', 'delq', 'label'], axis=1, inplace=True)
            label = model3.predict(data1)
            for index, i in data.iterrows():
                dic = {
                    'sid': index,
                    # 用户ID
                    'LoanAmount': i['Loan_Amount'],
                    # 用户贷款额
                    'Payment': i['Payment'],
                    # 用户已支付贷款
                    'Spend': i['Spend'],
                    # 用户消费总额
                    'label': label[0]
                    # 逾期率
                }
                json_list.append(dic)
        return Response(json_list)


'''
    url:http://127.0.0.1:8000/loan_approval/after_loan
    贷后模型
    还款率
'''


class after_loan(APIView):
    def get(self, request):
        id_data = CreditLevel.objects.filter(status=1).values('user_id', 'repaymentPeriod')
        id_list = []
        # 还款期限小于0.5才进入贷中模型
        for i in id_data:
            sublist = []
            if float(i['repaymentPeriod']) < 0.05:
                sublist.append(i['user_id'])
                sublist.append(i['repaymentPeriod'])
                id_list.append(sublist)
        json_list = []
        for x in id_list:

            data = pd.DataFrame(list(AfterLoan.objects.filter(ListingKey=x[0]).values()))
            loan_data = CreditLevel.objects.filter(user_id=x[0]).values('LoanAmount', 'Loan_Amount_Term')
            loanAmount = None
            loanTerm = None
            for h in loan_data:
                loanAmount = h['LoanAmount']
                loanTerm = h['Loan_Amount_Term']
            data.set_index(['ListingKey'], inplace=True)
            data1 = data.copy()
            data1.drop(['label', 'id', 'CreditGrade', 'Term', 'EmploymentStatus'], axis=1, inplace=True)
            label = model4.predict(data1)
            flag = 0
            for index, i in data.iterrows():
                dic = {
                    'sid': index,
                    # 用户id
                    'loanAmount': loanAmount,
                    # 贷款额度
                    'loanTerm': loanTerm,
                    # 贷款期限
                    'timeRemaining': int(float(loanTerm) * float(x[1])),
                    # 剩余期限
                    'label': label[flag]
                    # 还款率
                }
                json_list.append(dic)
                flag += 1
        return Response(json_list)


'''
    修改贷款金额
    url:http://127.0.0.1:8000/loan_approval/send_email
    接收数据形式：
    {
      "user_id":"person_1"
    }

'''


class sendEmail(APIView):
    def post(self, request):
        user = request.data.get('user_id')
        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，
        # 收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        mailmsg = send_mail("标题test", "邮件正文test", 'example_admin@163.com', ['example_person01@163.com'],
                            fail_silently=True)
        return Response(mailmsg)


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
