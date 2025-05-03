from django.urls import path
from . import views


app_name = 'short_links'

urlpatterns = [
    path('s/<str:slug>/', views.handle_short_link)
]