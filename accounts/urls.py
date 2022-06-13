from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
	home, 
	user_signup, 
	logout_user, 
	verify_mobile,
	generate_otp,
    add_details,
    edit_details,
    show_details,
    add_money,
	activate
)

urlpatterns = [
    path('home/', home, name='home'),
    path('createUser/', user_signup, name='signup'),
    path('loginUser/', obtain_auth_token, name='login'),
    path('logoutUser/', logout_user, name='logout'),
    path('verifyMobileNumber/', verify_mobile, name='verify_mobile'),
    path('generateOTP/', generate_otp, name='generate_otp'),
    path('addUserDetails/', add_details, name='add_details'),
    path('editUserDetails/', edit_details, name='edit_details'),
    path('showUserDetails/', show_details, name='show_details'),
    path('addMoneyToWallet/', add_money, name='add_money'),
    path('activate/<uidb64>/<token>/', activate, name='activate')
]
urlpatterns = format_suffix_patterns(urlpatterns)
