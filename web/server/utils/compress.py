# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-02-06'

import cStringIO
import gzip


def gzip_string(data, compresslevel=6):
    zbuf = cStringIO.StringIO()

    zfile = gzip.GzipFile(mode='wb', compresslevel=compresslevel, fileobj=zbuf)
    zfile.write(data.decode('utf-8').encode('utf-8'))
    zfile.close()

    compressed_content = zbuf.getvalue()

    return compressed_content