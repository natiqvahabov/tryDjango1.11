from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView
# Create your views here.

from .models import Item
from .forms import ItemForm

class ItemListView(ListView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)


class ItemDetailView(DetailView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
	template_name = "form.html"
	form_class =  ItemForm
	
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user =self.request.user
		return super(ItemCreateView,self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Menu'
		return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "form.html"
	form_class = ItemForm

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Menu'
		return context

