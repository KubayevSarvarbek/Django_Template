from django.urls import path
from .views import HomePageView
from .views import AboutPageView

urlpatterns = [
    path('about/',AboutPageView.as_view(),name='about'),
    path('',HomePageView.as_view(),name='home'),
]