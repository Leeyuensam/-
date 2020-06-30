from django.urls import path
from loan_approval.views import *

urlpatterns = [
    path('', AntiFraudList.as_view()),
    # path('/credit_score', credit_score_list.as_view()),
    path('/credit_lavel', CreditLevelList.as_view()),
    path('/graph_data', graph_data.as_view()),
    path('/stat_data', stat_data.as_view()),
    path('/user_relation', user_relation.as_view()),
    path('/user_transaction', user_transaction.as_view())
]
