from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .validators import validate_category
from .utils import unique_slug_generator

# Create your models here.
class RestaurantLocation(models.Model):
	name 		= models.CharField(max_length=120)
	location 	= models.CharField(max_length=120,null=True,blank=True)
	category	= models.CharField(max_length=120,null=True,blank=True, validators=[validate_category])
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	slug 		= models.SlugField(unique=True,null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def title(self):
		return self.name

def RestaurantLocationPreSave(sender, instance, *args, **kwargs):
	instance.category = instnce.category.capitalize()
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(RestaurantLocationPreSave, sender=RestaurantLocation)