
from django.urls import path
from good import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login_view,name="login"),
    path('register/', views.register, name='register'),

    path('first',views.first,name="first"),
    path('preferences', views.preferences_page, name='preferences_page'),
   path('send_notification',views.send_notification,name="send_notification"),
   path('save_preference', views.save_preference, name="save_preference"),

]
