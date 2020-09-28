from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "authenticate"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authenticate/logout.html'), name='logout'),
    path('register/', views.register_user, name='register'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='authenticate/change_password.html' , success_url=reverse_lazy('authenticate:password_change_done')), name='change_password'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='authenticate/password_change_done.html'),name='password_change_done'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html' , success_url=reverse_lazy('authenticate:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html' , success_url=reverse_lazy('authenticate:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
