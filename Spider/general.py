import os

# Create New Project
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating New Project ' + directory)
        os.makedirs(directory)

# Create Queued and Crawled Files
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# Write Contents
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# Append Contents
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete File Contents
def delete_file_contents(path):
    with open(path, 'w'):
        pass


def remove_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if os.path.isfile(queue):
        os.remove(queue)
    if os.path.isfile(crawled):
        os.remove(crawled)


# Create Set from File
def file_to_set(file_name):
    url_set = set()
    with open(file_name, 'rt') as f:
        for line in f:
            url_set.add(line.replace('\n', ''))
    return url_set

# Create File from Set
def set_to_file(url_set, file_name):
    delete_file_contents(file_name)
    for url in sorted(url_set):
        append_to_file(file_name, url)