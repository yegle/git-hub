import re
import glob
import os

escape_code_re = re.compile('\033\\[([^m]+)m')
codes = {
    1: {"font-weight": "bold"},
    4: {"text-decoration": "underline"},
    30: {"color": "black"},
    31: {"color": "red"},
    32: {"color": "green"},
    33: {"color": "yellow"},
    34: {"color": "blue"},
    35: {"color": "magenta"},
    36: {"color": "cyan"},
    37: {"color": "white"},
    40: {"background_color": "black"},
    41: {"background_color": "red"},
    42: {"background_color": "green"},
    43: {"background_color": "yellow"},
    44: {"background_color": "blue"},
    45: {"background_color": "magenta"},
    46: {"background_color": "cyan"},
    47: {"background_color": "white"},
}

def process_escape(match):
    items = [int(x) for x in match.group(1).split(';')]
    if 0 in items:
        return "</span>"
    else:
        attrs = [codes[x] for x in codes if x in items]
        return '<span style="%s">' % '; '.join([", ".join([': '.join(x) for x in attr.items()]) for attr in attrs])
    print match.groups()

def mangle_html(app, exception):
    if app.builder.name != 'html' or exception:
        return
    for file in glob.glob(os.path.join(app.builder.outdir, '*.html')):
        with open(file, 'r+') as fd:
            data = fd.read()
            data2 = re.sub(escape_code_re, process_escape, data)
            if data2 != data:
                fd.seek(0, os.SEEK_SET)
                fd.truncate()
                fd.write(data2)

def setup(app):
    app.connect('build-finished', mangle_html)
