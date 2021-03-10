from django.db import models

class Service(models.Model):  
    code                = models.CharField(verbose_name="New Service Code", max_length=1000, null=True, blank=True, unique=True)
    sap_code            = models.CharField(verbose_name="SAP Code", max_length=1000, null=True, blank=True)
    drawing             = models.CharField(verbose_name="Drawing", max_length=1000, null=True, blank=True)
    service_type        = models.CharField(verbose_name="Service Type", max_length=1000, null=True, blank=True)
    service_description = models.CharField(verbose_name="Service Description", max_length=1000, null=True, blank=True)
    rate_type           = models.CharField(verbose_name="Rate Type", max_length=1000, null=True, blank=True)
    notes               = models.CharField(verbose_name="Notes", max_length=1000, null=True, blank=True)
    wa_utilities_rate   = models.FloatField(verbose_name="WA Utilities Rate", null=True, blank=True)
    subby_rate          = models.FloatField(verbose_name="Subby Rate", null=True, blank=True)

    def __str__(self):
        return self.code
