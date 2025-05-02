from django.urls import path, include
from . import views


app_name = 'short_links'

urlpatterns = [
    path('<str:slug>/', views.handle_short_link)
]