# -*- coding: utf-8 -*-

import string
import re


def escape(s):
    """
    Escapes html entities
    """
    items = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
    )
    for item in items:
        s = s.replace(item[0], item[1])
    return s


def unescape(s):
    """
    Unescapes html entities
    """
    items = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;'),
    )
    for item in items:
        s = s.replace(item[1], item[0])
    return s


def addslashes(s):
    """
    Adds slash to \, " and '
    """
    return s.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


def stripslashes(s):
    """
    Strips slash from \, " and '
    """
    return s.replace('\\\\', '\\').replace('\\"', '"').replace("\\'", "'")


def html_char_entities(text):
    """
    >>> html_char_entities('info@mydomain.com')
    <<< '&#105;&#110;&#102;&#111;&#64;&#119;&#121;&#115;&#101;&#112;&#108;&#97;&#121;&#46;&#99;&#111;&#109;'
    """
    return ''.join(['&#%s;' % str(ord(char)) for char in text])


def encode_rot13(text):
    """
    >>> 'info@mydomain.com'.encode('rot13')
    <<< 'vasb@jlfrcynl.pbz'
    import codecs
    codecs.encode('info@mydomain.com', 'rot13')
    <<< 'vasb@jlfrcynl.pbz'
    """
    rot13 = string.maketrans('ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
                             'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
    return string.translate(text, rot13)


def encode_emails_with_rot13(text):
    p = re.compile(ur'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}', re.IGNORECASE)
    emails = re.findall(p, text)
    for email in emails:
        changed = re.sub('@', '\\\\100', re.sub('\.', '\\\\056', escape(email))).encode('rot13')
        rotten_link = """<script type="text/javascript">document.write \
            ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
            function(c){return String.fromCharCode((c<="Z"?90:122)>=\
            (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (changed, changed)
        text = re.sub(email, rotten_link, text)
    return text