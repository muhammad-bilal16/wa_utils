import os
import csv
import shutil
import datetime
from django.conf import settings
from jobs.models import job
from jobs.sftp import sftp
from jobs.utils import file_log
from jobs.exports.job_headers import job_headers
from reporting.models import Service
from pathlib import Path
from django.db.models import Q


def export_to_sftp_server(action):
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H%M%S')

    # Create temporary folder
    # path = f'temp_export_{date}_{time}'

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    path = os.path.join(BASE_DIR, 'temp_export')
    file_name = ""
    # os.mkdir(path)
    files = []
    all_completed_jobs = job.objects.filter(Q(job_status='Completed') | (
        Q(job_status='On Hold') & (Q(exported=False) | Q(exported=None))))
    jobs_count = all_completed_jobs.count()
    all_completed_work_centers = all_completed_jobs.values_list(
        'work_center', flat=True).distinct()

    for wc in all_completed_work_centers:
        file_name = f'JC_{wc}_{date}_{time}.csv'
        with open(path + '/' + file_name, 'w', newline='') as f:
            c = csv.writer(f)
            c.writerow(job_headers)
            job_list = all_completed_jobs.filter(work_center=wc).all()
            for j in job_list:
                l_job, l_activities = get_ordered_list_from_job(j)
                c.writerow(l_job)
                for a in l_activities:
                    c.writerow(a)
        files.append([file_name, job_list])

    try:
        ssh_client = sftp.get_ssh_client(
            settings.SSH_HOST,
            settings.SSH_USERNAME,
            settings.SSH_PASSWORD
        )

        sftp_client = sftp.get_sftp_client(ssh_client)

        for csv_file in files:
            filename = csv_file[0]
            sftp_client.put(
                localpath=f'{path}/{filename}',
                remotepath=f'{settings.EXPORT_JOB_FOLDER_PATH}/{filename}'
            )

            # Add file name and data into the db to mark as read
            file_log.log_file_to_db(
                action,
                filename,
                csv_file[1]  # Jobs of that file
            )

        sftp_client.close()
        ssh_client.close()

    except Exception as e:
        action.status = 'failed'
        action.save()
        print(e)
        return e.args

    # Archive all of the exported jobs

    all_completed_jobs.filter(job_status="Completed").update(
        job_status="Archived", exported=True)
    all_completed_jobs.filter(job_status="On Hold").update(exported=True)
    # if os.path.exists(path) and os.path.isdir(path):
    # shutil.rmtree(path/file_name)  # Delete the temporary directory and files
    
    action.status = 'completed'
    action.save()

    exported_files = {
        'jobs_exported': jobs_count,
        'exported_count': len(all_completed_work_centers),
        'files_exported': [f[0] for f in files]
    }
    return exported_files


def get_ordered_list_from_job(u_job):
    # Get 10 services from this job
    services = u_job.services.all()[:10]

    services_csv = []
    
    # Fill up the csv service data (there may be fewer than 10)
    for s in services:
        services_csv.append({ 'code': s.service.code, 'quantity': s.quantity })

    # Fill up the remaining service slots with empty templates
    for i in range(len(services_csv), 10):
        services_csv.append({ 'code': '', 'quantity': '' })
    
    resp = [
        u_job.notification_no,
        u_job.notification_type,
        u_job.job_type,
        u_job.work_center,
        u_job.functional_location,
        u_job.work_order,
        u_job.operation,
        u_job.operation_description,
        u_job.notification_long_text,
        u_job.task_number,
        u_job.task_code,
        '',  # task long text
        u_job.task_completion_date.strftime(
            '%Y%m%d') if u_job.task_completion_date else '',
        u_job.task_completed_by if u_job.job_status != 'On Hold' else '',
        u_job.task_user_status_shld,
        u_job.task_user_status_varq,
        u_job.task_user_status_reic,
        u_job.task_user_status_trmg,
        u_job.task_user_status_cpls,
        u_job.code_group1,
        u_job.activity_code_1,
        u_job.activity_start_date1.strftime(
            '%Y%m%d') if u_job.activity_start_date1 else '',
        u_job.activity_end_date1.strftime(
            '%Y%m%d') if u_job.activity_end_date1 else '',
        u_job.activity_long_text_1,
        u_job.quantity_factor1,
        u_job.meter_number,
        u_job.meter_model,
        u_job.install_date.strftime('%Y%m%d') if u_job.install_date else '',
        u_job.meter_type,
        u_job.meter_reading,
        u_job.pressure,
        u_job.meter_possition,
        'OFF' if u_job.job_status == 'Completed' and u_job.service_alignment==''  else u_job.service_alignment.upper(),
        u_job.removed_meter_number,
        u_job.removed_model,
        u_job.removed_date.strftime('%Y%m%d') if u_job.removed_date else '',
        u_job.removed_meter_reading,
        u_job.new_regulator_serial_number,
        u_job.old_regulator_serial_number,
        services_csv[0]['code'],
        services_csv[0]['quantity'],
        services_csv[1]['code'],
        services_csv[1]['quantity'],
        services_csv[2]['code'],
        services_csv[2]['quantity'],
        services_csv[3]['code'],
        services_csv[3]['quantity'],
        services_csv[4]['code'],
        services_csv[4]['quantity'],
        services_csv[5]['code'],
        services_csv[5]['quantity'],
        services_csv[6]['code'],
        services_csv[6]['quantity'],
        services_csv[7]['code'],
        services_csv[7]['quantity'],
        services_csv[8]['code'],
        services_csv[8]['quantity'],
        services_csv[9]['code'],
        services_csv[9]['quantity'],
    ]

    activity_lines = []
    # Get activities
    if u_job.job_type in 'SNF':
        activities = u_job.activities.all()
        if activities.count() > 0:
            activity1 = activities[0]
            resp[19] = u_job.code_group1
            resp[20] = activity1.code
            resp[21] = u_job.activity_start_date1.strftime('%Y%m%d') if u_job.activity_start_date1 else ''
            resp[22] = u_job.activity_end_date1.strftime('%Y%m%d') if u_job.activity_end_date1 else ''
            resp[24] = activity1.quantity

            # Fetching the rest of the activities for extra lines
            activities = activities[1:]
            
            for a in activities:
                activity_line = [ '' for i in range(len(resp)) ]
                activity_line[0] = u_job.notification_no
                activity_line[19] = u_job.code_group1
                activity_line[20] = a.code
                activity_line[21] = u_job.activity_start_date1.strftime('%Y%m%d') if u_job.activity_start_date1 else ''
                activity_line[22] = u_job.activity_end_date1.strftime('%Y%m%d') if u_job.activity_end_date1 else ''
                activity_line[24] = a.quantity
                activity_lines.append(activity_line)

    return (resp, activity_lines)
