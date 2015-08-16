# -*- coding: utf-8 -*-

import cStringIO
import gzip


def gzip_string(data, compresslevel=6):
    zbuf = cStringIO.StringIO()

    zfile = gzip.GzipFile(mode='wb', compresslevel=compresslevel, fileobj=zbuf)
    zfile.write(data)
    zfile.close()

    compressed_content = zbuf.getvalue()

    return compressed_content


def minify_string(chunk, iterations=1):
    replace_dict = {
        '\t': '',
        '\n': '',
        '\r\n': '',
        '    \r\n': '',
        '  \r\n': ' ',
        '    ': '',
        '  ': ' ',
        '> <': '><',
    }
    for _ in xrange(iterations):
        for a, b in replace_dict.iteritems():
            chunk = chunk.replace(a, b)
    return chunk