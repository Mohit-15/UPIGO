from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.manager import TokenAuthentication
from rest_framework.response import Response
from .serializers import TransactionDetailSerializer, TransactionSerializer
from .models import Transaction
from accounts.models import User, UserDetail
from upi_ids.models import UPI
from passlib.hash import pbkdf2_sha256


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def test(request, format=None):
	return Response({"message": "Transaction API working."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def view_all_transactions(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		transactions = Transaction.objects.filter(user=auth_user.id)
	except:
		message = {"Error": "No Transaction exist for this account."}
		return Response(message, status=status.HTTP_400_BAD_REQUEST)

	serializer = TransactionDetailSerializer(transactions, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def make_transaction(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		account_bal = UserDetail.objects.get(user=auth_user.id)
	except UserDetail.DoesNotExist:
		return Response({
			"Error": "User details not added. Please add it first."
		}, status=status.HTTP_404_NOT_FOUND)

	if account_bal.account_balance == 0:
		return Response({
				"Error": "User Wallet balance is zero. Please add some money in the wallet first."
		}, status=status.HTTP_404_NOT_FOUND)

	if not auth_user.mobile_verified:
		return Response({
				"Error": "Your Mobile Number is not verified. Please verify first to make any transaction."
			}, status=status.HTTP_400_BAD_REQUEST)

	try:
		receiver_upi = UPI.objects.get(upi_id=request.data['transfer_to'])
	except UPI.DoesNotExist:
		return Response({
				"Error": "The Receiver's UPI ID is not found or incorrect. Please check."
			}, status=status.HTTP_404_NOT_FOUND)

	if not receiver_upi.is_active:
		return Response({
				"Error": "The Receiver's UPI ID is not active. Sorry for the In-Convenience!"
			}, status=status.HTTP_400_BAD_REQUEST)

	if not pbkdf2_sha256.verify(request.data['password'], receiver_upi.upi_pin):
		return Response({
				"Error": "Entered UPI PIN is incorrect. Please check."
		}, status=status.HTTP_400_BAD_REQUEST)

	request.data['user'] = auth_user.id
	request.data['amount'] = '-' + str(request.data['amount'])
	serializer = TransactionSerializer(data=request.data)
	if serializer.is_valid():
		serializer.validated_data['not_pending'] = True
		serializer.save()
		account_bal.account_balance -= int(serializer.validated_data['amount'][1:])
		account_bal.save()
		second_request = {
			"user": UPI.objects.get(upi_id=serializer.validated_data['transfer_to']).username.id,
			"amount": '+' + str(serializer.validated_data['amount'])[1:],
			"received_from": UPI.objects.get(username=serializer.validated_data['user']).upi_id,
			"is_credit": 1
		}
		try:
			credit_account = UserDetail.objects.get(user=second_request['user'])
		except UserDetail.DoesNotExist:
			return Response({
				"Error": "The Receiver's Account details does not exist. Please check."
			}, status=status.HTTP_404_NOT_FOUND)

		serializer2 = TransactionSerializer(data=second_request)
		if serializer2.is_valid():
			serializer2.validated_data['not_pending'] = True
			serializer2.save()
			credit_account.account_balance += int(serializer2.validated_data['amount'][1:])
			credit_account.save()
		else:
			return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def debit_history(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		transactions = Transaction.objects.filter(user=auth_user.id, is_credit=False)
	except:
		message = {"Error": "No Transaction exist for this account."}
		return Response(message, status=status.HTTP_400_BAD_REQUEST)

	serializer = TransactionDetailSerializer(transactions, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def credit_history(request, format=None):
	auth_user = User.objects.get(email=request.user.email)
	try:
		transactions = Transaction.objects.filter(user=auth_user.id, is_credit=True)
	except:
		message = {"Error": "No Transaction exist for this account."}
		return Response(message, status=status.HTTP_400_BAD_REQUEST)

	serializer = TransactionDetailSerializer(transactions, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
