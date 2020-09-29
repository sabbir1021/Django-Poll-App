from django.urls import path 
from .import views
app_name = 'poll'
urlpatterns = [
    path('', views.HomeView.as_view() , name="home"),
    path('poll-list', views.PollView.as_view() , name = "poll"),
    path('poll-list/<str:username>', views.MyPollView.as_view() , name = "mypoll"),
    path('add-Poll', views.AddPollView.as_view() , name = "addpoll"),
    path('Poll-end/<int:id>', views.PollEndView.as_view() , name = "pollend"),
    path('edit-poll/<int:id>', views.EditPollView.as_view() , name = "editpoll"),
    path('delete-poll/<int:id>', views.DeletePollView.as_view() , name = "deletepoll"),
    path('add-choice/<int:id>', views.AddChoiceView.as_view() , name = "addchoice"),
    path('edit-choice/<int:id>/<int:cid>', views.EditChoiceView.as_view() , name = "editchoice"),
    path('delete-choice/<int:id>/<int:cid>', views.DeleteChoiceView.as_view() , name = "deletechoice"),
]
