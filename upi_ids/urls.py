from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
	test,
	create_upi,
	change_upi_pin,
	change_upi_id,
	deactivate_upi,
	reactivate_upi,
	show_upi_detail,
	scan_qr_code
)

urlpatterns = [
    path('test/', test, name='test'),
    path('createUpi/', create_upi, name='create_upi'),
    path('changeUpiPin/', change_upi_pin, name='change_upi_pin'),
    path('changeUpiID/', change_upi_id, name='change_upi_id'),
    path('deactivateUpi/', deactivate_upi, name='deactivate_upi'),
    path('reactivateUpi/', reactivate_upi, name='reactivate_upi'),
    path('showUpiDetails/', show_upi_detail, name='show_upi_detail'),
    path('scanQRCode/', scan_qr_code, name='scan_qr_code'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
