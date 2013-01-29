import os
import SimpleHTTPServer
import SocketServer
import sys

from fabric.api import local, env
from jinja2 import Environment, FileSystemLoader

from bugle import bugle, entry, meta

def prod():
    env.user = 'matt'
    env.host = 'kepler'
    env.dir = '/home/matt/yosemitebandit.com/bugle'
    env.root = 'yosemitebandit.com'
    env.source_path = 'src/'
    env.out_path = 'out/'

def dev():
    env.user = 'matt'
    env.host = 'kepler'
    env.dir = '/home/matt/yosemitebandit.com/public/test'
    env.root = '127.0.0.1:8000'
    env.source_path = 'src/'
    env.out_path = 'out/'

def deploy():
    pass
    #local('rsync -avz --del build/ %s@%s:%s' % (env.user, env.host, env.dir))

def serve():
    ''' from http://stackoverflow.com/a/10614360/232638
    address reuse makes it superior to "local('python -m SimpleHTTPServer')"
    '''
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    class MyTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    port = 8080
    server = MyTCPServer(('0.0.0.0', port), Handler)
    print '\nserving on localhost:%s\n' % port

    os.chdir(env.out_path)
    server.serve_forever()


def clean():
    ''' removes the output directory and its contents after a confirmation
    '''
    r = raw_input('\nconfirm removal of "%s" and all of its contents (y/n) ' % 
            env.out_path)
    if r in ['y', 'yes']:
        local('rm -rf %s' % env.out_path)
    else:
        print 'canceled.'


def build():
    b = bugle.Bugle(env.source_path, env.out_path)
    b.ensure_path_exists(b.out_path)

    # finds and instantiates entries
    entry_filepaths = b.discover_files(b.entry_path)
    entries = [entry.Entry(f) for f in entry_filepaths]
    for e in entries:
        if not e.valid:
            print 'validation failed for %s with message %s.' % (e
                    , e.validation_message)
            sys.exit()


    # find and instantiate meta files
    meta_filepaths = b.discover_files(b.meta_path)
    meta_files = [meta.Meta(f) for f in meta_filepaths]
    for m in meta_files:
        if not m.valid:
            print 'validation failed for %s with message %s.' % (m
                    , m.validation_message)
            sys.exit()
    # sort them by the slug
    meta_files.sort(key=lambda k: k.slug)


    # slugs from tags and entries should all be unique together
    if not b.verify_unique_routes(entries, meta_files):
        print 'paths not unique'
        sys.exit()

    # find all tags
    tags = b.compile_tags(entries)

    # copy over the css
    css_files = os.path.join(b.css_path, '*.css')
    css_out_path = os.path.join(b.out_path, 'css')
    b.ensure_path_exists(css_out_path)
    local('cp -L %s %s' % (css_files, css_out_path))


    # render entry templates
    for e in entries:
        out_dir = os.path.join(b.out_path, e.slug)
        b.ensure_path_exists(out_dir)

        # create a jinja env and render the template
        environ = Environment(loader=FileSystemLoader(b.template_path))
        template = environ.get_template('entry.html')
        html = template.render(entry=e, tags=tags, meta_files=meta_files)

        # write the page
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)


    # render tag templates
    for tag in tags:
        tagged_entries = []
        for e in entries:
            if tag['name'] in e.config['tags']:
                tagged_entries.append(e)

        # sort the entries by date
        tagged_entries.sort(key=lambda e: e.config['last_update']
                , reverse=True)

        # create a jinja env and render the template
        environ = Environment(loader=FileSystemLoader(b.template_path))
        template = environ.get_template('tag.html')
        html = template.render(tags=tags, tag=tag['name']
                , entries=tagged_entries, meta_files=meta_files)

        # write the page
        tag_slug = tag['name'].replace(' ', '-')
        out_dir = os.path.join(b.out_path, tag_slug)
        b.ensure_path_exists(out_dir)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)

    # render the meta pages
    for m in meta_files:
        # create a jinja env and render the template
        environ = Environment(loader=FileSystemLoader(b.template_path))
        template = environ.get_template('entry.html')
        html = template.render(entry=m, tags=tags, meta_files=meta_files
                , current_page=m.slug)

        # check for the root page
        if m.slug == '':
            out_dir = b.out_path
        else:
            # write the page
            out_dir = os.path.join(b.out_path, m.slug)
            b.ensure_path_exists(out_dir)

        # write the file
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)
