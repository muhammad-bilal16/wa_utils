from django.urls import path
from jobs.views import JobListViewset, JobActivityViewset, JobServiceViewset
from jobs.views import (
    JobDetailAPI,
    JobCreateAPI,
    JobUpdateAPI,
    JobBulkUpdateAPI,
    JobDeleteAPI,
    JobExportApi,
    JobImportApi,
)
app_name = 'jobs'

urlpatterns = [
    path('<int:pk>/', JobDetailAPI, name='JobAPI'),
    path('activities/', JobActivityViewset.as_view(), name='JobActivityAPI'),
    path('<int:job_id>/services/', JobServiceViewset.as_view(), name='JobServiceAPI'),
    path('create/', JobCreateAPI, name='APIJobCreate'),
    path('update/<int:pk>', JobUpdateAPI, name='APIJobUpdate'),
    path('update/', JobBulkUpdateAPI, name='APIJobBulkUpdate'),
    path('delete/<int:pk>', JobDeleteAPI, name='APIJobDelete'),
    path('list/', JobListViewset.as_view(), name='JobList'),
    path('import/', JobImportApi, name='APIJobImport'),
    path('export/', JobExportApi, name='APIJobExport'),
]
