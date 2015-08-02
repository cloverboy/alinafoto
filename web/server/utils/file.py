# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2013-11-21'

import codecs
import os
import string
import time
import shutil
import logging

from utils.crypt import generate_random_uuid4_string
from utils.date import time_to_datetime, datetime_now_as_string

from settings import STATIC_PATH, TMP_PATH

logger = logging.getLogger('mail_error')


def get_file_basename_ext(f):
    basename, ext = os.path.splitext(string.split(f, '/')[-1])
    return basename, ext.lower()


def get_file_basename(f):
    basename, ext = get_file_basename_ext(f)
    return basename


def get_file_ext(f):
    basename, ext = get_file_basename_ext(f)
    return ext


def get_file_name(f, lowercase=True):
    if lowercase:
        f = f.lower()
    return string.split(f, '/')[-1]


def get_file_path__file_name(f, lowercase=True):
    file_name = get_file_name(f, lowercase=lowercase)
    try:
        file_path = f.split(file_name)[0]
    except ValueError:
        return f, None
    return file_path, file_name


def get_file_path__basename__ext(f):
    file_path, file_name = get_file_path__file_name(f, lowercase=False)
    return (file_path,) + get_file_basename_ext(file_name)


def get_file_path(f):
    file_path, file_name = get_file_path__file_name(f, lowercase=False)
    return file_path


def format_path_as_string(path):
    return path.replace('/', '_').replace('.', '_')


def read_file(file_name, path=STATIC_PATH):
    full_path = os.path.join(path, file_name)

    if os.path.isfile(full_path):
        result = file(full_path, 'r').read()
    else:
        logger.error('File not found. full_path: <%s>' % full_path)
        result = False

    return result


def output_file(file_name, data, path=STATIC_PATH):
    full_file_path = os.path.join(path, file_name)

    # cyrillic text needs to be exported in this way
    if isinstance(data, list):
        fp = codecs.open(full_file_path, 'w', 'utf-8')
        for row in data:
            fp.write(row)
        fp.close()

    else:
        fp = open(full_file_path, 'w')
        fp.write(data)
        fp.close()


def get_files_by_ext(path, ext_list):
    result = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)) and get_file_ext(filename) in ext_list:
            result.append(filename)
    return result


def copy_file(src_full_path, dest_full_path):
    if os.path.isfile(src_full_path):
        shutil.copy(src_full_path, dest_full_path)
        return True
    logger.error('File not found. src_full_path: <%s>' % src_full_path)
    return False


def remove_old_files(path, days):
    time_now = time.time()
    removed_file_list = []

    for file_name in os.listdir(path):

        file_path = os.path.join(path, file_name)
        modified = os.stat(file_path).st_mtime

        if modified < time_now - days * 86400:

            if remove_file(file_path):
                removed_file_list.append(file_path)

    return removed_file_list


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    logger.error('File not found. file_path: <%s>' % file_path)
    return False


def remove_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        return True
    logger.error('Folder not found. folder_path: <%s>' % folder_path)
    return False


def get_static_file_relative_path(f):
    file_path, file_basename, file_ext = get_file_path__basename__ext(f)
    full_file_path = os.path.join(STATIC_PATH, f)
    file_name = u'%s%s' % (file_basename, file_ext)

    if os.path.isfile(full_file_path):
        slug = time_to_datetime(long(os.stat(full_file_path).st_mtime), output_format='%d%H%M%S')
    else:
        logger.error('File not found. full_file_path: <%s>' % full_file_path)
        slug = datetime_now_as_string(output_format='%d%H%M%S')

    return '%s%s/%s' % (file_path, slug, file_name)


def get_unique_file_name(ext='.jpg', path=TMP_PATH):
    file_name = None
    attempt = 0

    while attempt < 100:
        file_name = '{}{}'.format(generate_random_uuid4_string(), ext)
        save_path = os.path.join(path, file_name)

        if os.path.isfile(save_path):
            attempt += 1
        else:
            break

    if attempt == 100:
        logger.error('Cant find unique file name. ext: <%s>, path: <%s>' % (ext, path))
        return False

    return file_name