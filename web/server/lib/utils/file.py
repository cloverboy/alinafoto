# -*- coding: utf-8 -*-

import codecs
import os
import re
import string
import time
import shutil
import logging
import tempfile

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from lib.utils.crypt import generate_random_uuid4_string
from lib.utils.date import time_to_datetime, datetime_now_as_string
from lib.utils.collector import TracebackCollector

from settings import STATIC_PATH, TMP_PATH, BASE_DOMAIN, MEDIA_DOMAIN, MEDIA_DOMAIN_PROTOCOL

console_logger = logging.getLogger('console')


def get_file_basename_ext(f):
    basename, ext = os.path.splitext(string.split(f, '/')[-1])
    found = re.compile('(\.[a-zA-Z]{1,4})').search(ext)
    if found:
        ext = found.group().lower()
    else:
        console_logger.error('failed to find ext. f: <%s>' % f)
        ext = None
    return basename, ext


def get_file_basename(f):
    basename, ext = get_file_basename_ext(f)
    return basename


def get_file_ext(f):
    basename, ext = get_file_basename_ext(f)
    return ext


def get_file_name(f, lowercase=True):
    basename, ext = get_file_basename_ext(string.split(f, '/')[-1])
    file_name = None

    if ext is not None:
        found = re.compile('([a-zA-Z0-9_-]+%s)' % ext).search(f)
        if found:
            file_name = found.group()
            if lowercase:
                file_name = file_name.lower()

    if file_name is None:
        console_logger.error('failed to find file_name. f: <%s>' % f)

    return file_name


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


def file_exists(path):
    return os.path.isfile(path)


def dir_exists(path):
    return os.path.isdir(path)


def format_path_as_string(path):
    return path.replace('/', '_').replace('.', '_')


def read_file(file_name, path=STATIC_PATH):
    if path is None:
        full_path = file_name
    else:
        full_path = os.path.join(path, file_name)

    if file_exists(full_path):
        result = file(full_path, 'r').read()
    else:
        console_logger.error('file not found. full_path: <%s>' % full_path)
        result = None

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


def get_dirs(path, name_only=True):
    result = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
    if not name_only:
        result = map(lambda dir_name: os.path.join(path, dir_name), result)
    return result


def get_files_by_ext(path, ext_list):
    result = []
    for filename in os.listdir(path):
        if file_exists(os.path.join(path, filename)) and get_file_ext(filename) in ext_list:
            result.append(filename)
    return result


def move_file(src_full_path, dest_full_path):
    if file_exists(src_full_path):
        shutil.move(src_full_path, dest_full_path)
        return True
    console_logger.error('file not found. src_full_path: <%s>' % src_full_path)
    return False


def copy_file(src_full_path, dest_full_path):
    if file_exists(src_full_path):
        shutil.copy(src_full_path, dest_full_path)
        return True
    console_logger.error('file not found. src_full_path: <%s>' % src_full_path)
    return False


def remove_old_files(path, days):
    time_now = time.time()
    removed_files = []

    for file_name in os.listdir(path):

        file_path = os.path.join(path, file_name)
        modified = os.stat(file_path).st_mtime

        if modified < time_now - days * 86400:

            if remove_file(file_path):
                removed_files.append(file_path)

    return removed_files


def remove_file(file_path):
    result = False
    if file_exists(file_path):
        os.remove(file_path)
        result = True
    else:
        console_logger.error('file not found. file_path: <%s>' % file_path)
    return result


def remove_dir(path):
    result = False
    if dir_exists(path):
        shutil.rmtree(path)
        result = True
    else:
        console_logger.error('directory not found. path: <%s>' % path)
    return result


_static_file_relative_path_cache = {}


def get_static_file_relative_path(f):
    global _static_file_relative_path_cache

    result = _static_file_relative_path_cache.get(f)

    if result is None:
        file_path, file_basename, file_ext = get_file_path__basename__ext(f)
        full_file_path = os.path.join(STATIC_PATH, f)
        file_name = u'%s%s' % (file_basename, file_ext)

        if file_exists(full_file_path):
            slug = time_to_datetime(long(os.stat(full_file_path).st_mtime), output_format='%d%H%M%S')
        else:
            console_logger.error('file not found. full_file_path: <%s>' % full_file_path)
            slug = datetime_now_as_string(output_format='%d%H%M%S')

        result = '%s%s/%s' % (file_path, slug, file_name)

        _static_file_relative_path_cache[f] = result

    return result


def get_unique_file_name(ext='.png', path=TMP_PATH):
    file_name = None
    found = False

    for _ in xrange(0, 101):
        file_name = '{}{}'.format(generate_random_uuid4_string(), ext)
        save_path = os.path.join(path, file_name)

        if not file_exists(save_path):
            found = True
            break

    if not found:
        console_logger.error('cant find unique file name. ext: <%s>, path: <%s>' % (ext, path))
        file_name = None

    return file_name


def get_static_file(path, full_url=None):
    relative_path = get_static_file_relative_path(path)

    if full_url is None:
        full_url = BASE_DOMAIN != MEDIA_DOMAIN

    if full_url:
        result = '%s://%s/%s' % (MEDIA_DOMAIN_PROTOCOL, MEDIA_DOMAIN, relative_path)

    else:
        result = '/%s' % relative_path

    return result


def valid_img_url(value):
    regex = re.compile(ur'^(https?://.*/(?:[\w\-]{3,}\.(?:gif|jpe?g|png)(?:[^\w]*\?.*)?))$',
                       re.IGNORECASE | re.UNICODE)
    return bool(regex.search(value))


class HttpDownload(object):

    def __init__(self):
        tempfile.tempdir = TMP_PATH
        self.tmp_file = None
        self.req = None
        self.http_client = AsyncHTTPClient()

    @coroutine
    def fetch(self, url):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tmp')
        self.req = HTTPRequest(url=url, streaming_callback=self.streaming_callback)

        response = None
        error = False
        error_code = None
        error_response = None
        tmp_file_path = None
        tmp_file_body = None

        try:
            response = yield Task(self.http_client.fetch, self.req)
        except Exception, e:
            error = True
            if hasattr(e, 'getcode'):
                error_code = e.getcode()
            else:
                error_code = 502
            error_response = TracebackCollector().collect(e)

        self.tmp_file.flush()
        self.tmp_file.close()

        if not error:
            error_code = response.code
            error = response.error is not None or error_code != 200
            tmp_file_path = self.tmp_file.name
            tmp_file_body = read_file(tmp_file_path, path=None)

        result = {
            'error': error,
            'error_code': error_code,
            'error_response': error_response,
            'tmp_file_path': tmp_file_path,
            'tmp_file_body': tmp_file_body,
        }

        raise Return(result)

    def streaming_callback(self, data):
        self.tmp_file.write(data)