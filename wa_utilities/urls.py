"""wa_utilities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs for job API
    path('api/jobs/', include('jobs.urls')),
    # URLs for job API
    path('api/reporting/', include('reporting.urls')),
    # URLs for files_logs API
    path('api/files_logs/', include('files_logs.urls')),
    # URLs for LogIn & Logout API
    path('api/', include('authentcation.urls')),
    # URLs for Rest Password API
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]