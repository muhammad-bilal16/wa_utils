import csv
from django.conf import settings
from jobs.models import job
from jobs.sftp import sftp
from jobs.utils import file_filter
from jobs.utils import file_log
from datetime import datetime
import logging
# Reads job files from server and imports new jobs
# Returns list of new files
def import_from_sftp_server(action):
    jobs_count = 0

    try:
        ssh_client = sftp.get_ssh_client(
            settings.SSH_HOST,
            settings.SSH_USERNAME,
            settings.SSH_PASSWORD
        )

        sftp_client = sftp.get_sftp_client(ssh_client)

        sftp_client.chdir(settings.IMPORT_JOB_FOLDER_PATH)  # Change into import directory
        
        file_list = sftp_client.listdir()  # Get list of all present files
        filtered_list = file_filter.filter_imported_files(file_list) # Remove already imported files

        for filename in filtered_list:
            csv_file = sftp_client.open(filename)
            job_list = []
            try:
                reader = csv.reader(csv_file, delimiter=',')
                next(reader)  # Skipping metadata
                next(reader)  # Skipping headers
                for row in reader:
                    job_list.append(row)
            except:
                action.status = 'failed'
                action.save()
                logger = logging.getLogger(__name__)
                logger.error('Something went wrong while reading CSV file!')
            finally:
                csv_file.close()

            jobs_count += len(job_list)  # Increasing total jobs count
            job_objs = []
            for job in job_list:
                job_objs.append(create_or_update_job(job))  # Add this job into the database
            
            # Add file name and data into the db to mark as read
            file_log.log_file_to_db(
                action,
                filename,
                job_objs
            )

        sftp_client.close()
        ssh_client.close()

        imported_files = {
            'jobs_imported': jobs_count,
            'files_count': len(file_list),
            'imported_count': len(filtered_list),
            'files_found': file_list,
            'files_imported': filtered_list,
        }

        action.status = 'completed'
        action.save()

        return imported_files

    except Exception as e:
        action.status = 'failed'
        action.save()
        print(e)
        return e.args


# Creates or updates a Job object in the database
# Identifies the Job object through work_order field
# Returns Job object
def create_or_update_job(job_detail):
    # Either get or create a new object using the work_order attribute
    new_or_updated_job, created = job.objects.get_or_create(
        notification_no=job_detail[3],  # notification_no will be used as unique identifier
    )

    job_status = 'New'
    if not created:
        if new_or_updated_job.job_status in ['Completed', 'Archived']:
            return new_or_updated_job
        if new_or_updated_job.job_status in 'On Hold':
            job_status = 'Off Hold'
        else:
            job_status = new_or_updated_job.job_status
    
    new_or_updated_job.job_status = job_status
    new_or_updated_job.work_center = job_detail[0]
    new_or_updated_job.date_issued = datetime.strptime(job_detail[1], '%d/%m/%Y')
    new_or_updated_job.time_issued = job_detail[2]
    new_or_updated_job.notification_no = job_detail[3]
    new_or_updated_job.functional_location = job_detail[4]
    new_or_updated_job.task_number = job_detail[5]
    new_or_updated_job.task_code = job_detail[6]
    new_or_updated_job.job_type = job_detail[7]
    new_or_updated_job.work_order = job_detail[8]
    new_or_updated_job.operation = job_detail[9]
    new_or_updated_job.operation_description = job_detail[10]
    new_or_updated_job.code_group_object_parts = job_detail[11]
    new_or_updated_job.part_of_object = job_detail[12]
    new_or_updated_job.code_group_problem = job_detail[13]
    new_or_updated_job.problem_damage_code = job_detail[14]
    new_or_updated_job.location = job_detail[15]
    new_or_updated_job.mains_details = job_detail[16]
    new_or_updated_job.planned_start_date = datetime.strptime(job_detail[17], '%d/%m/%Y')
    new_or_updated_job.planned_end_date = datetime.strptime(job_detail[18], '%d/%m/%Y')
    new_or_updated_job.check_digit = job_detail[19]
    new_or_updated_job.functional_loc_desc = job_detail[20]
    new_or_updated_job.task_long_text = job_detail[21]
    new_or_updated_job.exported = False
    new_or_updated_job.save()

    return new_or_updated_job
