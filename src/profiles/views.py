from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth import get_user_model
# Create your views here.

from restaurants.models import RestaurantLocation
from menus.models import Item

User = get_user_model()

class ProfileDetailView(DetailView):
	template_name = 'profiles/user.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User, username__iexact=username, is_active=True)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileDetailView,self).get_context_data(*args, **kwargs)
		user = context['user']
		
		query = self.request.GET.get('q')
		qs = RestaurantLocation.objects.filter(owner = user).search(query)
		is_item_exist = Item.objects.filter(user = user).exists()
		
		if qs.exists() and is_item_exist:
			context['locations'] = qs

		return context