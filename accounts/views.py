from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSignUpSerializer, UserSerializer, UserDetailProfile
from accounts.manager import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import schemas, response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from accounts.models import User, UserDetail
from accounts.token import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os

# Create your views here.
load_dotenv(find_dotenv())
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request, format=None):
	data = {"message": "This is the Home page."}
	return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request, format=None):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request, format=None):
    try:
        request.user.auth_token.delete()
    except ObjectDoesNotExist:
        return Response(
            {"message": "Auth Token doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {"message": "User Logged out Successfully !"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_mobile(request, format=None):
    try:
        session_otp = request.META.get('HTTP_VERIFICATION_OTP')
        user = request.user
    except:
        return Response(
            {"message": "Verification OTP Expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    #print(session_otp)
    input_otp = request.POST.get('otp', '')
    if user.mobile_verified: 
        return Response(
            {"message": "Mobile Number Already Verified."}, status=status.HTTP_200_OK
        )
    if session_otp == input_otp and not user.mobile_verified:
        user.mobile_verified = True
        user.save()
        return Response(
            {"message": "Mobile Number Verified."}, status=status.HTTP_200_OK
        )
    return Response(
            {"message": "Verification OTP didn't match. "}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_otp(request, format=None):
    if request.user.mobile_verified:
        return Response(
            {"message": "Mobile Number Already Verified."}, status=status.HTTP_200_OK
        )

    random_otp = randint(100000, 999999)
    request.META['HTTP_VERIFICATION_OTP'] = random_otp
    #print(request.META['HTTP_VERIFICATION_OTP'])
    message = client.messages.create(
        body='Hi there! Your One Time Password for you mobile verification is {}. This OTP is valid for only 2 minutes'.format(random_otp),
        from_= os.environ.get('TWILIO_NUMBER'),
        to = '+91{}'.format(request.user.mobile_no)
    )
    #print(message.sid)
    return Response(
            {"message": "Verification OTP send to your registered Mobile Number."}, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_details(request, format=None):
    auth_user = User.objects.get(email=request.user.email)
    data = JSONParser().parse(request)
    data["user"] = auth_user.id
    #print(data)
    serializer = UserDetailProfile(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_details(request, format=None):
    auth_user = User.objects.get(email=request.user.email)
    try:
        user = UserDetail.objects.get(user=auth_user)
    except UserDetail.DoesNotExist:
        return Response(
            {"error": "User doesn't exist in the Database"},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = JSONParser().parse(request)
    data["user"] = auth_user
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_details(request, format=None):
    auth_user = User.objects.get(email=request.user.email)
    try:
        user = UserDetail.objects.get(user=auth_user)
    except UserDetail.DoesNotExist:
        return Response(
            {"error": "User doesn't exist in the Database"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if (
        user is not None
        and account_activation_token.check_token(user, token)
        and user.is_active is False
    ):
        user.is_active = True
        user.save()
        subject = "[IMP] Account Verification: {}".format(user.name)
        message = render_to_string(
            "account/confirmation_mail.html",
            {
                "user": user,
            },
        )
        send_mail(
            subject,
            message,
            "msbproject1234@gmail.com",
            [user.email],
            fail_silently=False,
        )
        return Response({"data": "Account Activated !"}, status=status.HTTP_200_OK)
    else:
    	return Response({"data": "Activation Link is invalid."}, status=status.HTTP_400_BAD_REQUEST)
