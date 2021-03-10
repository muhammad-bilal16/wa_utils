from django.db import models
from ftpserver.ftp import FTPStorage

fs = FTPStorage()

class FTPTest(models.Model):
    file = models.FileField(upload_to='ftp_files', storage=fs)
