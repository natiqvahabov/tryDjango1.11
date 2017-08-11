from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
# Create your views here.

from restaurants.models import RestaurantLocation
from menus.models import Item

from .models import Profile
from .forms import RegisterForm
User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)


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
		print(context)
		query = self.request.GET.get('q')
		qs = RestaurantLocation.objects.filter(owner = user).search(query)
		is_item_exist = Item.objects.filter(user = user).exists()
		
		is_following = False

		if user.profile in self.request.user.is_following.all():
			is_following = True

		context['is_following'] = is_following
		if qs.exists() and is_item_exist:
			context['locations'] = qs

		return context


class FollowView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		follow_user = request.POST.get("username")
		profile = Profile.objects.get(user__username__iexact = follow_user.strip())
		user = request.user

		if user in profile.followers.all():
			profile.followers.remove(user)
		else:
			profile.followers.add(user)

		return redirect(f"/users/{profile.user.username}")

