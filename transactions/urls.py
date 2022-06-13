from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
	test,
	view_all_transactions,
	make_transaction,
	debit_history,
	credit_history
)

urlpatterns = [
    path('test/', test, name='test'),
    path('viewTransactions/', view_all_transactions, name='view_all_transactions'),
    path('makeTransaction/', make_transaction, name='make_transaction'),
    path('debitHistory/', debit_history, name='debit_history'),
    path('creditHistory/', credit_history, name='credit_history'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
