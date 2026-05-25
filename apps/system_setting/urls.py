from django.urls import path
from .views import SystemSettingView

urlpatterns = [
    path('system-setting/', SystemSettingView.as_view(), name='system-setting'),
]
