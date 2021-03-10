from knox import views as knox_views
from authentcation.views import LoginAPI
from django.urls import path

app_name = 'authentcation'

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]
