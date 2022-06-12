from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.manager import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from accounts.models import User
from .serializers import UpiSerializer, UpiDetailSerializer
from .models import UPI
from passlib.hash import pbkdf2_sha256
from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
fernet = Fernet(os.environ.get('ENC_KEY').encode())

@api_view(["GET"])
@permission_classes([AllowAny])
def test(request, format=None):
	data = {"message": "This is the Testing Page."}
	return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_upi(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	if not auth_user.mobile_verified:
		return Response({
				"Error": "Mobile Number is not Verified. Please verify first."
			}, status=status.HTTP_400_BAD_REQUEST)

	request_data = {}
	data = JSONParser().parse(request)
	request_data["username"] = auth_user.id
	if data["pin1"] != data["pin2"]:
		return Response({
				"Error": "UPI Pin didn't Match. Please correct the error."
			}, status=status.HTTP_400_BAD_REQUEST)

	if data["set_default"]:
		request_data["upi_id"] = str(auth_user.mobile_no) + "@upigo"
	else:
		request_data["upi_id"] = data["upi_id"] + "@upigo"
	
	enc_password = pbkdf2_sha256.encrypt(data["pin1"], rounds=12000, salt_size=32)
	request_data["upi_pin"] = enc_password

	serializer = UpiSerializer(data=request_data)
	if serializer.is_valid():
		serializer.save()
		subject = "[IMP] UPI ID Created for - {}".format(auth_user.name)
		message = render_to_string(
			"upi_id/confirmation_mail.html",
			{
				"user": auth_user,
				"upi_id": request_data["upi_id"],
				"upi_pin": data["pin1"],
				"qrcode": serializer.data['scan_code']
			},
		)
		send_mail(
			subject,
			message,
			"msbproject1234@gmail.com",
			[auth_user.email],
			fail_silently=False,
		)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_upi_pin(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		upi_profile = UPI.objects.get(username=auth_user.id)
	except UPI.DoesNotExist:
		return Response({
				"Error": "UPI Profile doesn't exist for this account. Please create a new UPI ID."
			}, status=status.HTTP_400_BAD_REQUEST)

	request_data = {}
	data = JSONParser().parse(request)
	request_data["username"] = auth_user.id
	request_data["upi_id"] = upi_profile.upi_id
	if data["pin1"] != data["pin2"]:
		return Response({
				"Error": "UPI Pin didn't Match. Please correct the error."
			}, status=status.HTTP_400_BAD_REQUEST)
	
	enc_password = pbkdf2_sha256.encrypt(data["pin1"], rounds=12000, salt_size=32)
	request_data["upi_pin"] = enc_password
	serializer = UpiSerializer(upi_profile, data=request_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deactivate_upi(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		upi_profile = UPI.objects.get(username=auth_user.id)
	except UPI.DoesNotExist:
		return Response({
				"Error": "UPI Profile doesn't exist for this account. Please create a new UPI ID."
			}, status=status.HTTP_400_BAD_REQUEST)

	upi_profile.is_active = False
	upi_profile.save()
	return Response({"Message": "UPI ID successfully Deactivated"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_upi_detail(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		upi_profile = UPI.objects.filter(username=auth_user.id)
	except UPI.DoesNotExist:
		return Response({
				"Error": "No UPI Profile created for this account."
			}, status=status.HTTP_404_NOT_FOUND)

	serializer = UpiDetailSerializer(upi_profile, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scan_qr_code(request, format=None):
	code = os.environ.get('PREFIX') + request.data['qr_code'][:-6] + os.environ.get('SUFFIX') + request.data['qr_code'][-6:]
	print(code)
	decoded_upi = fernet.decrypt(code.encode()).decode()
	try:
		upi_account = UPI.objects.get(upi_id=decoded_upi+"@upigo")
	except UPI.DoesNotExist:
		return Response({
				"Error": "No UPI Details found."
			}, status=status.HTTP_404_NOT_FOUND)

	serializer = UpiDetailSerializer(upi_account)
	return Response(serializer.data, status=status.HTTP_200_OK)

