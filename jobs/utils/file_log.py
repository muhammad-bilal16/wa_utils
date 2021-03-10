from files_logs.models import Action, File, FileJob


def log_file_to_db(action, filename, jobs):
    f = File.objects.create(
        action=action,
        file_name=filename,
    )
    for job in jobs:
        FileJob.objects.create(
            file=f,
            job=job
        )
    return