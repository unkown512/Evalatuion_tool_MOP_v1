"""
file utility
"""
import glob
import os


def get_folder_name_from_path(folder_path):
    """
    get the last chunk

    :param folder_path:
    :return:
    """
    folder_path = folder_path.replace("\\",'/')
    if folder_path.endswith("/"):
        folder_path = folder_path[:-1]
    if folder_path.count("/") > 0:
        return folder_path[folder_path.rindex('/')+1:]
    else:
        return folder_path


def get_file_name(file_path):
    """

    :param file_path:
    :return:
    """
    file_path = file_path.replace("\\", "/")
    file_name = file_path[file_path.rindex("/")+1:]
    return file_name


def get_file_name_prefix(file_path):
    """

    :param file_path:
    :return:
    """
    file_name = get_file_name(file_path)
    if '.' in file_name:
        return file_name[:file_name.rindex('.')]
    return file_name


def get_file_path_in_folder(folder_path, suffix=None):
    """

    :param folder_path:
    :param suffix:
    :return:
    """
    pattern = "{}/*".format(folder_path)
    if suffix is not None:
        pattern = "{}/*.{}".format(folder_path, suffix)
    file_path_list = []
    for file_path in glob.glob(pattern):
        file_path = file_path.replace("\\", "/")
        file_path_list.append(file_path)
    return file_path_list


def get_folder_from_path(file_path):
    """

    :param file_path:
    :return:
    """
    file_path = file_path.replace("\\", "/")
    return file_path[:file_path.rindex("/")]


def test_folder_exist_for_file_path(file_path):
    """

    :param file_path:
    :return:
    """
    folder = get_folder_from_path(file_path)
    if not os.path.isdir(folder):
        os.makedirs(folder)


def test_folder_exist(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
