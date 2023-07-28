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

	class Meta:
		unique_together = ('user', 'name', 'url')

	
	def __str__(self):
		return self.name


class ChangesStore(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	url_model = models.ForeignKey(UrlModel, on_delete=models.CASCADE)
	description = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.url_model.name