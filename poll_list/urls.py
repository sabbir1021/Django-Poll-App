
from django.urls import path 
from .import views
app_name = 'poll'
urlpatterns = [
    path('', views.HomeView.as_view() , name="home"),
    path('poll-list', views.PollView.as_view() , name = "poll")
]
