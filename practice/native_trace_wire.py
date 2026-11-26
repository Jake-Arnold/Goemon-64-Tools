"""Private inspector wire: isolate native logs, bound packets, recover traces."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile

PREFIX = 'GOEMON_NATIVE '
CHUNK_ROWS = 32
MAX_ROWS = 3600
MAX_LINE = 256 * 1024


def private_stdout():
    """Call only inside the managed child, before loading native libraries."""
    sys.stdout.flush()
    stream = os.fdopen(os.dup(1), 'w', encoding='utf-8', buffering=1)
    os.dup2(2, 1)  # C printf and Python stdout are now logs, never protocol
    return stream


class TraceWriter:
    def __init__(self, stream):
        self.stream = stream
        self.rows = []
        self.watches = None

    def packet(self, value):
        line = PREFIX + json.dumps(value, allow_nan=False, separators=(',', ':')) + '\n'
        if len(line.encode('utf-8')) > MAX_LINE:
            raise ValueError('Native protocol packet exceeds limit')
        self.stream.write(line)
        self.stream.flush()

    def send(self, value):
        report = value.get('report')
        if report is None:
            self.packet(value)
            return
        rows = report['rows']
        if len(rows) > MAX_ROWS:
            raise ValueError('Native trace exceeds row limit')
        append = (self.watches == report['watches'] and len(rows) >= len(self.rows)
                  and rows[:len(self.rows)] == self.rows)
        start = len(self.rows) if append else 0
        metadata = dict(value, report={k: v for k, v in report.items() if k != 'rows'})
        self.packet(dict(wire='begin', start=start, total=len(rows), reset=not append, value=metadata))
        for i in range(start, len(rows), CHUNK_ROWS):
            self.packet(dict(wire='rows', start=i, rows=rows[i:i+CHUNK_ROWS]))
        self.packet(dict(wire='end'))
        self.rows = list(rows)
        self.watches = report['watches']


class TraceReader:
    """Reassemble reports in the reader thread, never in the Tk thread."""
    def __init__(self):
        self.rows = []
        self.pending = None
        self.total = 0
        self.staged = []

    def receive(self, line):
        if not line.startswith(PREFIX) or len(line.encode('utf-8')) > MAX_LINE:
            raise ValueError('Invalid native protocol record')
        p = json.loads(line[len(PREFIX):])
        if not isinstance(p, dict):
            raise ValueError('Invalid native protocol object')
        kind = p.get('wire')
        if kind == 'begin':
            if self.pending is not None:
                raise ValueError('Overlapping native reports')
            start, total = p['start'], p['total']
            if (type(start) is not int or type(total) is not int or not 0 <= start <= total <= MAX_ROWS
                    or (start != 0 if p['reset'] else start != len(self.rows))):
                raise ValueError('Invalid native trace offset')
            self.staged = [] if p['reset'] else list(self.rows)
            self.pending = p['value']
            self.total = total
            return None
        if kind == 'rows':
            rows = p['rows']
            if (self.pending is None or p['start'] != len(self.staged) or not isinstance(rows, list)
                    or not 1 <= len(rows) <= CHUNK_ROWS or len(self.staged) + len(rows) > self.total
                    or not all(isinstance(row, dict) for row in rows)):
                raise ValueError('Invalid native trace chunk')
            self.staged.extend(rows)
            return None
        if kind == 'end':
            if self.pending is None or len(self.staged) != self.total:
                raise ValueError('Incomplete native trace report')
            value = self.pending
            self.rows = self.staged
            value['report']['rows'] = self.rows
            self.pending = None
            self.staged = []
            return value
        if kind is not None or self.pending is not None or 'report' in p:
            raise ValueError('Unexpected native protocol record')
        return p


def checkpoint(path, report):
    """Replace only after a complete valid snapshot; leave prior trace on error."""
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.trace-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(report, f, allow_nan=False, separators=(',', ':'))
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
