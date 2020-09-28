from django.urls import path 
from .import views
app_name = 'poll'
urlpatterns = [
    path('', views.HomeView.as_view() , name="home"),
    path('poll-list', views.PollView.as_view() , name = "poll"),
    path('poll-list/<str:username>', views.MyPollView.as_view() , name = "mypoll"),
    path('add-Poll', views.AddPollView.as_view() , name = "addpoll")
]
