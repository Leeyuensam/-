from django.shortcuts import render

from .models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

'''
    登录模块，url=http://127.0.0.1:8000
'''


class login(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'mes': None}
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            obj = User.objects.filter(username=username, password=password).first()
            if not obj:
                ret['code'] = 1001
                ret['mes'] = '用户名或密码错误！'
                return Response(ret)
            ret['mes'] = '登陆成功'
        except Exception as e:
            ret['code'] = 1002
            ret['mes'] = '请求异常'
        return Response(ret)
# Create your views here.
