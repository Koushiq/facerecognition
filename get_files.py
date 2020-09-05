import os

def get_dir_files(path):
    arr = os.listdir(path)
    arr.sort()

    return arr

def get_next_file_id(path):
    id = len(get_dir_files(path)) + 1
    return id

def get_file_name_all(path):
    filepath = get_dir_files(path)

    filename = []
    for fp in filepath:
        fileinfo = fp.split('-')
        fileinfo = fileinfo[1].split('.')
        filename.append(fileinfo[0])
    return filename

def get_file_name_index(path, index):
    filename = get_file_name_all(path)
    if index < len(filename):
        return filename[index]
    else:
        return -1