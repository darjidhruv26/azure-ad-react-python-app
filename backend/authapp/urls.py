from django.urls import path
from .views import DashboardView, UserLogout

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', UserLogout.as_view(), name='logout'),
]