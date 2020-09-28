
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('poll_list.urls', namespace="poll")),
    path('', include('authenticate.urls', namespace="authenticate")),
]
