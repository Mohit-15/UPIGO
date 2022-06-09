from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os
import uuid

load_dotenv(find_dotenv())
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)


# Create your models here.
class Transaction(models.Model):
	transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	transfer_to = models.CharField(max_length=100, blank=True, null=True)
	received_from = models.CharField(max_length=100, blank=True, null=True)
	amount = models.CharField(max_length=8)
	is_credit = models.BooleanField(default=False)
	not_pending = models.BooleanField(default=False)
	done_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)


	def __str__(self):
		return str(self.transaction_id)


@receiver(post_save, sender=Transaction)
def send_transaction_message(sender, instance, created, **kwargs):
    if created:
        name = instance.user.name if instance.user.name else "No name given"
        if instance.is_credit:
        	amount_credit = int(instance.amount[1:])
        	received_from = str(instance.received_from)
        	message = client.messages.create(
		        body='Hello {}, Rs. {} has been credited in your account from {}.'.format(name, amount_credit, received_from) +\
		        		'\n\nThe transaction id for this transaction is : {}.'.format(instance.transaction_id) +\
		        		'\n\nThank you for using UPI GO.',
		        from_= os.environ.get('TWILIO_NUMBER'),
		        to = '+91{}'.format(instance.user.mobile_no)
		    )
        else:
        	amount_deducted = int(instance.amount[1:])
        	transfer_to = str(instance.transfer_to)
        	message = client.messages.create(
		        body='Hello {}, Rs. {} has been debited from your account to {}.'.format(name, amount_deducted, transfer_to) +\
		        		'\n\nThe transaction id for this transaction is : {}.'.format(instance.transaction_id) +\
		        		'\n\nThank you for using UPI GO.',
		        from_= os.environ.get('TWILIO_NUMBER'),
		        to = '+91{}'.format(instance.user.mobile_no)
		    )
