from django.urls import path
from .views import LandingPageView

urlpatterns = [
    path('pages/landing/', LandingPageView.as_view(), name='landing-page'),
]