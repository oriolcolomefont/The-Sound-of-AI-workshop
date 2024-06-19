import datetime
import hashlib
import os


def get_absolute_path_from_relative_to_source(relative_path):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))
    return absolute_path



def create_uuid():
    return hashlib.sha256(datetime.datetime.now().isoformat().encode()).hexdigest()[:32]
