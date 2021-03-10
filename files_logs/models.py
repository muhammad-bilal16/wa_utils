from django.db import models
from jobs.models import job


class Action(models.Model):
    action_type = models.CharField(verbose_name='Action Type', max_length=1000, blank=True)
    actioned_on = models.DateTimeField(verbose_name='Actioned On', auto_now_add=True)
    account_id  = models.CharField(verbose_name='Account ID', max_length=1000, blank=True)
    status      = models.CharField(verbose_name='Action Status', max_length=1000, blank=True)


class File(models.Model):
    action      = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='files')
    file_name   = models.CharField(verbose_name='File Name', max_length=1000, blank=True)
    
    def __str__(self):
        return self.file_name


class FileJob(models.Model):
    file    = models.ForeignKey(File, on_delete=models.CASCADE, related_name='jobs')
    job     = models.ForeignKey(job, on_delete=models.CASCADE, related_name='+')
    
    def __str__(self):
        return self.file.file_name