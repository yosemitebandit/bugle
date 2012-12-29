Oh, a static site built from markdown.
There are entries and tags.
A home page and something about the author.

A python script builds up the tag indices and renders entries.


### Source
The organization of `src/`:

    - src/
       |- meta/
       |- entries/
       |- templates/
       \- static/

The root and about pages are contained in `meta/`.
These pages are HTML, not markdown, and are injected into the `base.html` template.

The real content is in `entries/` in the form of markdown files.
Some of these files are project write-ups, others are blog entries:

    - src/
       \- entries/
           |- trebuchet.md
           |- never.md
           |- ps2keyboard-leonardo-port.md
           |- meduele.md
           \- khmer-in-ubuntu.md

Each of these markdown files is secretly half `yaml`:

    title: never.md
    blurb: an sms time-capsule
    created: September, 2012
    updated: October, 2012
    ongoing: true
    where: San Francisco
    tags:
        - python
        - twilio
        - projects
    thumb: http://s3.aws.com/screenshot.png
    route: sms-time-capsule
    css:
        - css/never.css
        - css/other.css
    js:
        - js/jquery.min.js
    ---

    ### oh, memory

    it's a fickle thing.
    we should try to make it better..
    with *texts*.

So that's `---` as a separator between the metadata and the content.
The value of `thumb` is shown in the indices.
Set a custom URL with the optional `route` parameter.
The date-type parameters, `created` and `updated`, must be of the form `September, 2012` or `September 10, 2012`.

Templates are in the source directory, they use Jinja syntax.
Tagged entries can also be gathered up under one roof.

    - src/
       \- templates/
           |- base.html
           |- entry.html
           \- tag.html

And any custom styles or js for a note or project, the build script pulls those in based on the metadata:

    - src/
       \- static/
           |- js/
           |   |- khmer-in-ubuntu.js
           |   |- meduele.js
           |   \- never.js
           |
           \- css/
               |- trebuchet.css
               \- khmer-in-ubuntu.css


### Building
The build script does the following:

 1. gathers all the markdown files
 1. validates each of them
 1. compiles tags
 4. generates slugs and checks that they are unique
 2. creates indices for all detected tags
 3. sets up the vanilla pages..
 5. renders markdown
 6. injects resultant html into templates
 7. pulls relevant css and js into templates
 8. saves resulting files in output directory

Start this process with fabric:

    $ ./path/to/venv/bin/activate
    (venv)$ fab dev build

Clean up the build via:

    $ ./path/to/venv/bin/activate
    (venv)$ fab dev clean


### Run the dev server

    $ ./path/to/venv/bin/activate
    (venv)$ fab dev serve


### Deploying
Maybe `rsync` or S3.


### Testing
Test the build process with

    $ ./path/to/venv/bin/activate
    (venv)$ nosetests
