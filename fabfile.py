import os
import shutil

from fabric.api import local, env, abort
from jinja2 import Template
import markdown
import yaml

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
    base = 'src/pages'
    for root, sub_folders, filenames in os.walk(base):
        for filename in filenames:
            with open(os.path.join(root, filename), 'r') as f:
                content = f.read()
            # pull out the yaml-formatted metadata at the top
            meta = yaml.safe_load(content.split('---')[0])

            # extract the actual content (in markdown)
            # rejoin as a precaution against other instances of "---"
            content = content.split('---')
            content.pop(0)
            md_content = '---'.join(content)

            if not meta:
                abort("file %s has no metadata" % filename)

            # create the folder for this page
            if ' ' in meta['route']:
                abort("route for %s has a space -- let's try to avoid that" % filename)

            if meta['route'] == '/':
                path = os.path.join('build', 'index.html')
            else:
                if not os.path.exists(os.path.join('build', meta['route'])):
                    os.makedirs(os.path.join('build', meta['route']))
                path = os.path.join('build', meta['route'], 'index.html')

            # generate the css and js
            css = ''
            if 'css' in meta.keys():
                for css_file in meta['css']:
                    css += '<link rel="stylesheet" href="../css/%s">' % css_file
            js = ''
            if 'js' in meta.keys():
                for js_file in meta['js']:
                    js += '<script src="../js/%s">' % js_file

            # render the markdown content
            md_content = markdown.markdown(md_content)

            # inject all this into the template
            template_files = 'src/templates'
            template = Template(open(os.path.join(template_files, meta['template']), 'r').read())
            out = template.render(title=meta['title'], date=meta['date'], content=md_content, css=css, js=js)

            # write the data
            with open(path, 'w') as f:
                f.write(out)

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
