from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
	test,
)

urlpatterns = [
    path('test/', test, name='test'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
