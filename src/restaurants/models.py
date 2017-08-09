from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from .validators import validate_category
from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			return self.filter(
					Q(name__icontains = query) |
					Q(location__icontains = query) |
					Q(category__icontains = query) |
					Q(item__name__icontains = query) |
					Q(item__contents__icontains = query)
				).distinct()
		return self


class RestaurantLocationManager(models.Manager):

	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using = self._db)

	def search(self, query):
		return self.get_queryset().search(query)


# Create your models here.
class RestaurantLocation(models.Model):

	# RestaurantLocation.objects.filter(owner__id=1)
	# User.objects.get(id=1).restaurantlocation_set.all()
	# User = RestaurantLocation.objects.first().owner.__class__
	# RestaurantLocation = User.objects.first().restaurantlocation_set.first().__class__

	owner 		= models.ForeignKey(User)
	name 		= models.CharField(max_length=120)
	location 	= models.CharField(max_length=120,null=True,blank=True)
	category	= models.CharField(max_length=120,null=True,blank=True, validators=[validate_category])
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	slug 		= models.SlugField(unique=True,null=True, blank=True)

	objects = RestaurantLocationManager()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('restaurants:detail', kwargs={'slug':self.slug})

	@property
	def title(self):
		return self.name

def RestaurantLocationPreSave(sender, instance, *args, **kwargs):
	instance.category = instance.category.capitalize()
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(RestaurantLocationPreSave, sender=RestaurantLocation)