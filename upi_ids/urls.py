from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
	test,
	create_upi,
	change_upi_pin,
	deactivate_upi,
	show_upi_detail
)

urlpatterns = [
    path('test/', test, name='test'),
    path('createUpi/', create_upi, name='create_upi'),
    path('changeUpiPin/', change_upi_pin, name='change_upi_pin'),
    path('deactivateUpi/', deactivate_upi, name='deactivate_upi'),
    path('showUpiDetails/', show_upi_detail, name='show_upi_detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
