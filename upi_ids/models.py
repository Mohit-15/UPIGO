from django.db import models
from accounts.models import User
from passlib.hash import pbkdf2_sha256
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode


# Create your models here.
class UPI(models.Model):
	username = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	upi_id = models.CharField(max_length=150, unique=True)
	upi_pin = models.CharField(max_length=1000)
	scan_code = models.ImageField(upload_to = 'upi/qr_codes', unique = True, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
	is_active = models.BooleanField(default=True)


	def __str__(self):
		return self.username.mobile_no

	def save(self, *args, **kwargs):
		if not self.scan_code:
			encrypted_upi = pbkdf2_sha256.encrypt(self.upi_id, rounds=12000, salt_size=32) + "@upigo"
			upi_qrcode = qrcode.make(encrypted_upi)
			canvas = Image.new('RGB', (520,520), 'white')
			draw = ImageDraw.Draw(canvas)
			canvas.paste(upi_qrcode)
			file_name = f'qrcode-{self.username.mobile_no}'+'.png'
			buff = BytesIO()
			canvas.save(buff, "PNG") 
			self.scan_code.save(file_name, File(buff), save=False)
			canvas.close()
		super().save(*args, **kwargs)
