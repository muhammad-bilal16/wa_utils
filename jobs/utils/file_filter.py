from files_logs.models import Action, File, FileJob


def filter_imported_files(file_list):
    filtered_list = []
    for file in file_list:
        if not File.objects.filter(file_name=file).exists():
            filtered_list.append(file)
    
    return filtered_list