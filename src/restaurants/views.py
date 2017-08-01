import random
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


def RestaurantLocationCreate(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		# obj = RestaurantLocation.objects.create(
		# 	name = form.cleaned_data('name'),
		# 	location = form.cleaned_data('location'),
		# 	category = form.cleaned_data('category')
		# )
		return HttpResponseRedirect('/restaurants/')
	if form.errors:
		print(form.errors)

	context = {'form':form}
	template_name = 'restaurants/form.html'
	return render(request, template_name, context)


class RestaurantLocationCreateView(CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/form.html'
	success_url = '/restaurants/'


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


