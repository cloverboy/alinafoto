# -*- coding: utf-8 -*-

import sys
import inspect
import traceback
import logging

from collections import namedtuple

Report = namedtuple('Report', ['exception', 'frames'])
Frame = namedtuple('Frame', ['file', 'line', 'code', 'locals'])

logger = logging.getLogger('default')


class TracebackCollector(object):

    def collect(self, exception):
        frames = []
        exc_info = sys.exc_info()
        tb = exc_info[2]

        while tb:
            try:
                frame = self._collect_frame(tb.tb_frame)
            except Exception as e:
                formatted_lines = traceback.format_exc().splitlines()
                tb = ', '.join(formatted_lines)
                logger.error(self._format(exception, tb))
                break
            else:
                frames.append(frame)
                tb = tb.tb_next

        return self._format_report(Report(
            exception=exception,
            frames=frames[::-1],
        ))

    def _collect_frame(self, frame):
        return Frame(
            file=inspect.getfile(frame),
            line=frame.f_lineno,
            locals=frame.f_locals,
            code=inspect.getsourcelines(frame),
        )

    def _format(self, exception, tb):
        return '\n\nException:\n%(exception)s\n\nTraceback:\n%(tb)s' % {
            'exception': exception,
            'tb': tb,
        }

    def _format_report(self, report):
        tb = '\n'.join(self._format_frame(frame) for frame in report.frames)
        return self._format(report.exception, tb)

    def _format_frame(self, frame):
        lines, current_line = frame.code
        code = ''.join(
            '    ' +
            ('>>' if lines.index(line) == frame.line - current_line else '  ') +
            ' ' + line
            for line in lines
        )
        return '    %(file)s:%(line)s\n%(locals)s\n%(code)s' % {
            'file': frame.file,
            'line': frame.line,
            'locals': frame.locals,
            'code': code,
        }