import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation
# Create your views here.

# class based view
class ContactView(View):
	def get(self,request,*args,**kwargs):
		#print(kwargs) - ^contact/(?P<id>\d+)/$. - contact/23/ - kwargs: {'id': 23}
		return render(request, 'contact.html', {})

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self,*args,**kwargs):
		context = super(HomeView,self).get_context_data(*args,**kwargs)
		num = random.randint(1,10)
		some_list = [num, random.randint(1,10), random.randint(1,10)]
		context = {
			"bool_item":True,
			"num":num,
			"some_list":some_list
		}
		return context


class RestaurantLocationDeleteView(DeleteView):
	queryset = RestaurantLocation.objects.all()
	# def get_queryset(self, pk):
	# 	queryset = RestaurantLocation.objects.get(pk=pk)
	# 	queryset.delete()
	# 	return queryset

@login_required()
def RestaurantLocationCreate(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	if form.is_valid():
		if request.user.is_authenticated():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			return HttpResponseRedirect('/restaurants/')
		else:
			return HttpResponseRedirect('/login/')
	if form.errors:
		print(form.errors)

	context = {'form':form}
	template_name = 'restaurants/form.html'
	return render(request, template_name, context)


class RestaurantLocationCreateView(LoginRequiredMixin,CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/form.html'

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.owner =self.request.user
		return super(RestaurantLocationCreateView,self).form_valid(form)


class RestaurantListView(ListView):
	template_name = 'restaurants/restaurant_list.html'

	def get_queryset(self):
		slug = self.kwargs.get("slug")
		if slug:
			queryset = RestaurantLocation.objects.filter(
				Q(category__iexact=slug) |
				Q(category__icontains=slug)
			)
			if not queryset:
				print("Nothing Found")
		else:
			queryset = RestaurantLocation.objects.all()

		return queryset


class RestaurantDetailView(DetailView):
	queryset = RestaurantLocation.objects.all()

	# def get_context_data(self,*args,**kwargs):
	# 	#print(self.kwargs). {(rest_id, 2)}
	# 	context = super(RestaurantDetailView,self).get_context_data(*args,**kwargs)
	# 	print(context)
	# 	return context

	# def get_object(self,*args,**kwargs):
	# 	rest_id = self.kwargs.get("rest_id")
	# 	restaurant = get_object_or_404(RestaurantLocation,id=rest_id)
	# 	return restaurant


# function-based view
def restaurants(request):
	template_name = 'restaurants/restaurant_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		'object_list':queryset
	}
	return render(request,template_name,context)


