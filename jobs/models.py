from django.db import models
from reporting.models import Service
from reporting.utils.float_arithmetic import multiply_float, add_float

choice = [
    ('New', 'New'),
    ('Completed', 'Completed'),
    ('In Progress', 'In Progress'),
    ('On Hold', 'On Hold'),
    ('Archived', 'Archived'),
    ('Off Hold', 'Off Hold'),
]

class job(models.Model):
    job_status                  = models.CharField(default='In Progress',verbose_name="Job Status", max_length=11, choices=choice)

    date_issued                 = models.DateField(verbose_name='Date Issued', null=True, blank=True)
    time_issued                 = models.CharField(verbose_name='Time Issued', max_length=1000, blank=True)
    notification_no             = models.CharField(verbose_name='Notification Number', max_length=1000, blank=True)
    notification_type           = models.CharField(verbose_name='Notification Type', max_length=1000, blank=True)
    functional_location         = models.CharField(verbose_name='Functional Location', max_length=1000, blank=True)
    task_number                 = models.CharField(verbose_name='Task Number', max_length=1000, blank=True)
    task_code                   = models.CharField(verbose_name='Task Code', max_length=1000, blank=True)
    job_type                    = models.CharField(verbose_name='Job Type', max_length=1000, blank=True)
    work_order                  = models.CharField(verbose_name='Word Order', max_length=1000, blank=True)
    operation                   = models.CharField(verbose_name='Operation', max_length=1000, blank=True)
    task_completed_by           = models.CharField(verbose_name='Task completed by', max_length=1000, blank=True)
    task_completion_date        = models.DateField(verbose_name='Task completion date', null=True, blank=True)
    task_long_text              = models.TextField(verbose_name='Task Long Text', blank=True)
    notification_long_text      = models.TextField(verbose_name='Notification Long Text(Comments 150 chars)', blank=True)
    work_order_number           = models.CharField(verbose_name='Work order Number', max_length=1000, blank=True)
    work_center                 = models.CharField(verbose_name='Work Center', max_length=1000, blank=True)

    operation_description       = models.CharField(verbose_name='Operation Description', max_length=1000, blank=True)
    code_group_object_parts     = models.CharField(verbose_name='Code Group Object Parts', max_length=1000, blank=True)
    part_of_object              = models.CharField(verbose_name='Part of Object', max_length=1000, blank=True)
    code_group_problem          = models.CharField(verbose_name='Code Group Problem', max_length=1000, blank=True)
    problem_damage_code         = models.CharField(verbose_name='Problem/Damage Code', max_length=1000, blank=True)
    location                    = models.CharField(verbose_name='Location', max_length=1000, blank=True)
    mains_details               = models.CharField(verbose_name='Mains Details', max_length=1000, blank=True)
    planned_start_date          = models.DateField(verbose_name='Planned Start Date', null=True, blank=True)
    planned_end_date            = models.DateField(verbose_name='Planned End Date', null=True, blank=True)
    check_digit                 = models.CharField(verbose_name='Check Digit', max_length=1000, blank=True)
    functional_loc_desc         = models.CharField(verbose_name='Functional Loc Desc', max_length=1000, blank=True)
    old_regulator_serial_number = models.CharField(verbose_name='Old Regulator Serial Number', max_length=1000, blank=True)
    new_regulator_serial_number = models.CharField(verbose_name='New Regulator Serial No', max_length=1000, blank=True)
    removed_meter_reading       = models.CharField(verbose_name='Removed Meter Reading', max_length=1000, blank=True)    
    removed_model               = models.CharField(verbose_name='Removed Model', max_length=1000, blank=True)
    removed_date                = models.DateField(verbose_name='Removed Date', null=True, blank=True)
    removed_meter_number        = models.CharField(verbose_name='Removed Meter Number', max_length=1000, blank=True)
    service_alignment           = models.CharField(verbose_name='Service Alignment', max_length=1000, blank=True)
    meter_possition             = models.CharField(verbose_name='Meter Possition', max_length=1000, blank=True)
    pressure                    = models.CharField(verbose_name='Pressure', max_length=1000, blank=True)
    meter_reading               = models.CharField(verbose_name='Meter Reading', max_length=1000, blank=True)    
    meter_type                  = models.CharField(verbose_name='Meter Type', max_length=1000, blank=True)
    install_date                = models.DateField(verbose_name='Install Date', null=True, blank=True)
    meter_number                = models.CharField(verbose_name='Meter Number', max_length=1000, blank=True)
    meter_model                 = models.CharField(verbose_name='Meter Model', max_length=1000, blank=True)
    activity_long_text_1        = models.TextField(verbose_name='Activity long Text1', blank=True)
    quantity_factor1            = models.CharField(verbose_name='Quantity Factor1', max_length=1000, blank=True)
    activity_end_date1          = models.DateField(verbose_name='Activity End date1', null=True, blank=True)    
    activity_start_date1        = models.DateField(verbose_name='Activity Start Date1', null=True, blank=True)
    activity_code_1             = models.CharField(verbose_name='Activity Code1', max_length=1000, blank=True)
    code_group1                 = models.CharField(verbose_name='Code Group1', max_length=1000, blank=True)
    task_user_status_cpls       = models.CharField(verbose_name='Task User Status (CPLS)', max_length=1000, blank=True)
    task_user_status_reic       = models.CharField(verbose_name='Task User Status (REIC)', max_length=1000, blank=True)
    task_user_status_trmg       = models.CharField(verbose_name='Task User Status (TRMG)', max_length=1000, blank=True)
    task_user_status_varq       = models.CharField(verbose_name='Task User Status (VARQ)', max_length=1000, blank=True)
    task_user_status_shld       = models.CharField(verbose_name='Task User Status (SHLD)', max_length=1000, blank=True)
    work_centre                 = models.CharField(verbose_name='Work Centre', max_length=1000, blank=True)
    suburb                      = models.CharField(verbose_name='Suburb', max_length=1000, blank=True)
    assigned_to                 = models.CharField(verbose_name='Assigned To', max_length=1000, blank=True)
    exported                    = models.BooleanField(default=False, blank=True, null=True)
    date_updated                = models.DateField(verbose_name='Last Updated On', auto_now=True)
    date_added                  = models.DateField(verbose_name='Imported On', auto_now=True)

    @property
    def calculated_rates(self):
        wa_utils_rate = 0
        subby_rate = 0
        for s in self.services.all():
            # Calculating the quantity * rates for WA Utils and Subby rates
            wa_utils_rate = add_float(wa_utils_rate, multiply_float(s.quantity, s.service.wa_utilities_rate))
            subby_rate = add_float(subby_rate, multiply_float(s.quantity, s.service.subby_rate))
        return (wa_utils_rate, subby_rate)
            

    def __str__(self):
        return self.work_center


class JobService(models.Model):
    job         = models.ForeignKey(job, on_delete=models.CASCADE, related_name='services')
    service     = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='+')
    quantity    = models.IntegerField(verbose_name='Quantity', default=0, null=False)

    @property
    def service_details(self):
        return self.service

    def __str__(self):
        return self.job.notification_no


class JobActivity(models.Model):
    job         = models.ForeignKey(job, on_delete=models.CASCADE, related_name='activities')
    code        = models.CharField(verbose_name='Activity Code', max_length=1000, null=True, blank=True)
    code_group  = models.CharField(verbose_name='Activity Code Group', max_length=1000, null=True, blank=True)
    quantity    = models.IntegerField(verbose_name='Quantity', default=0, null=False)
    start_date  = models.DateField(verbose_name='Activity Start Date', null=True, blank=True)
    end_date    = models.DateField(verbose_name='Activity End Date', null=True, blank=True)

    def __str__(self):
        return self.job.notification_no
