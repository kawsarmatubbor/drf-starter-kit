from django.urls import path
from .views import ContactMessageCreateView, LandingPageView, ContactPageView

urlpatterns = [
    path('pages/landing/', LandingPageView.as_view(), name='landing-page'),
    path('pages/contact/', ContactPageView.as_view(), name='contact-page'),
    path('pages/contact/message/', ContactMessageCreateView.as_view(), name='contact-message-create'),
]