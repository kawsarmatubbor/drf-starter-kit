from django.urls import path
from .views import ContactMessageCreateView, LandingPageView, ContactPageView, FAQPageView, OtherPageListView, OtherPageDetailView

urlpatterns = [
    path('pages/landing/', LandingPageView.as_view(), name='landing-page'),
    path('pages/contact/', ContactPageView.as_view(), name='contact-page'),
    path('pages/contact/message/', ContactMessageCreateView.as_view(), name='contact-message-create'),
    path('pages/faq/', FAQPageView.as_view(), name='faq-page'),
    path('pages/other/', OtherPageListView.as_view(), name='other-page-list'),
    path('pages/other/<slug:slug>/', OtherPageDetailView.as_view(), name='other-page-detail'),
]