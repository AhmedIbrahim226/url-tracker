from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UrlModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	url = models.URLField()
	checking_length = models.IntegerField()
	updating_time = models.IntegerField()
	source_code	= models.TextField()

	
	def __str__(self):
		return self.name


class ChangesInLines(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	url_model = models.ForeignKey(UrlModel, on_delete=models.CASCADE)
	old_line = models.TextField()
	new_line = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name