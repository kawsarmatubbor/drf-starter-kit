from django.urls import path
from .views import ContactCreateView

urlpatterns = [
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
]
