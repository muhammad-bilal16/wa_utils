from django.urls import path
from reporting import views

app_name = 'reporting'

urlpatterns = [
    path('services/', views.ServiceListView.as_view(), name='ServiceListViewAPI'),
    path('', views.ReportByDateRange, name='ReportByDateRange'),
    path('<str:notification_no>/', views.ReportByJob, name='ReportByJob'),
]
