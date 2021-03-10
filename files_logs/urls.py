from django.urls import path
from files_logs import views

app_name = 'files_logs'

urlpatterns = [
    path('actions/', views.ActionsListView.as_view(), name='ActionListAPI'),
    path('actions/<int:action_id>/files/', views.FileListView.as_view(), name='FileListAPI'),
    path('files/<int:file_id>/jobs/', views.FileJobListView.as_view(), name='FileJobListAPI'),
]
