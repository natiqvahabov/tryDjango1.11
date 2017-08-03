from django.conf.urls import url

from restaurants.views import (
    RestaurantListView,
    RestaurantDetailView,
    RestaurantLocationCreateView,
    RestaurantLocationDeleteView
)

urlpatterns = [
	url(r'$',RestaurantListView.as_view(),name="list"),
    url(r'^create/$',RestaurantLocationCreateView.as_view(),name="create"),
    url(r'^(?P<slug>[\w-]+)/$',RestaurantDetailView.as_view(),name="detail"),
]