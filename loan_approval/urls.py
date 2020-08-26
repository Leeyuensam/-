from django.urls import path
from loan_approval.views import *

urlpatterns = [
    path('', AntiFraudList_yes.as_view()),
    path('AntiFraudList_no', AntiFraudList_no.as_view()),
    path('credit_lavel', CreditLevelList.as_view()),
    path('pass_approval', pass_approval.as_view()),
    path('reject_approval', reject_approval.as_view()),

    path('permit_loan', permit_loan.as_view()),
    path('reject_loan', reject_loan.as_view()),
    path('edit_loan', edit_loan.as_view()),
    path('show_details', ShowDetails.as_view()),

    path('behavior_score', behaviour_score.as_view()),
    path('after_loan', after_loan.as_view()),
    path('send_email', sendEmail.as_view()),

    path('graph_data', graph_data.as_view()),
    path('stat_data', stat_data.as_view()),
    path('user_relation', user_relation.as_view()),
    path('user_transaction', user_transaction.as_view())
]
