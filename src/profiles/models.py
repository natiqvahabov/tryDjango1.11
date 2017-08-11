from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
	user 		= models.OneToOneField(User)
	followers 	= models.ManyToManyField(User, related_name='is_following', blank=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now = True)
	activated	= models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def send_activation_email(self):
		print("Activation")
		pass

# create auto profile after user model is created
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = Profile.objects.get_or_create(user = instance)

post_save.connect(post_save_user_receiver, sender=User)