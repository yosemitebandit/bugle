import os
import shutil
import sys

from fabric.api import local, env, abort
from jinja2 import Template
import markdown
import yaml

from bugle import bugle, entry

def prod():
    env.user = 'matt'
    env.host = 'kepler'
    env.dir = '/home/matt/yosemitebandit.com/bugle'
    env.root = 'yosemitebandit.com'

def dev():
    env.user = 'matt'
    env.host = 'kepler'
    env.dir = '/home/matt/yosemitebandit.com/public/test'
    env.root = '127.0.0.1:8000'

def deploy():
    local('rsync -avz --del build/ %s@%s:%s' % (env.user, env.host, env.dir))

def serve():
    local('python -m SimpleHTTPServer')

def build():
    source_path = 'src/'
    out_path = 'out/'
    b = bugle.Bugle(source_path, out_path)

    entry_filepaths = b.discover_entries(b.entry_path)
    entries = [entry.Entry(f) for f in entry_filepaths]
    for e in entries:
        if not e.valid:
            print 'validation failed for %s with message %s.' % (e
                    , e.validation_message)
            sys.exit()

    tags = b.compile_tags(entries)

    print tags



    '''
    # generate the css and js
    css = ''
    if 'css' in meta.keys():
        for css_file in meta['css']:
            css += '<link rel="stylesheet" href="../css/%s">' % css_file
    js = ''
    if 'js' in meta.keys():
        for js_file in meta['js']:
            js += '<script src="../js/%s">' % js_file

    # inject all this into the template
    template_files = 'src/templates'
    template = Template(open(os.path.join(template_files, meta['template']), 'r').read())
    out = template.render(title=meta['title'], date=meta['date'], content=md_content, css=css, js=js)

    # write the data
    with open(path, 'w') as f:
        f.write(out)
    '''

    '''
    # copy over the css and js
    # maybe minify and concatenate one day
    for filetype in ['css', 'js']:
        build_path = os.path.join('build', filetype)
        if not os.path.exists(build_path):
            os.makedirs(build_path)

        src_path = os.path.join('src', filetype)
        for root, sub_folders, filenames in os.walk(src_path):
            for filename in filenames:
                shutil.copy(os.path.join(src_path, filename), build_path)
    '''
