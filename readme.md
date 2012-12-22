Hey, a website, built from markdown.
There are projects and notes.
A home page and something about the author.

A python script builds up the index of notes and projects.
And each note and project is rendered and injected into templates.


### Source
The organization of `src/`:

    - src/
       |- home.html
       |- about.html
       |- projects/
       |- notes/
       |- templates/
       |- css/
       \- js/

That is to say, `home.html` and `about.html` are vanilla html, and frankly quite boring.
The content is in `projects/` and `notes/`, in the form of markdown files:

    - src/
       |- projects/
       |   |- trebuchet.md
       |   |- never.md
       |   \- meduele.md
       |
       \- notes/
           |- ps2keyboard-leonardo-port.md
           \- khmer-in-ubuntu.md

Each of these markdown files is secretly half `yaml`:

    title: never.md
    blurb: an sms time-capsule
    when: September, 2012
    ongoing: true
    where: San Francisco
    tags:
        - python
        - twilio
    group: projects
    thumb: http://s3.aws.com/screenshot.png
    css:
        - css/never.css
        - css/other.css
    js:
        - js/jquery.min.js
    ---

    ### oh, memory

    it's a fickle think.
    we should try to make it better..
    with *texts*.

So that's `---` as a separator between the metadata and the content.
In the metadata, the `group` is currently either `projects` or `notes`.
Indices are built for these sections.
The value of `thumb` is shown in the indices.

Basic templates, guess where those are.
The project index will be tiles of photos, titles and a short description.
Notes will be a title and blurb - they may get paginated.
Tagged projects and notes can also be gathered up under one roof.

    - src/
       \- templates/
           |- project_index.html
           |- project.html
           |- note_index.html
           |- note.html
           \- tag.html

And any custom styles or js for a note or project, the build script pulls those in based on the metadata:

    - src/
       |- css/
       |   |- trebuchet.css
       |   \- khmer-in-ubuntu.css
       |
       \- js/
           |- khmer-in-ubuntu.js
           |- meduele.js
           \- never.js


### Building
The build script does the following:

 1. gathers all the markdown files and validates their yaml
 1. compiles `tags` and `groups`
 2. creates indices for all detected `groups` and `tags`
 3. sets up the vanilla pages..
 4. generates slugs and checks that they are unique
 5. renders markdown
 6. injects resultant html into templates
 7. pulls relevant css and js into templates
 8. saves resulting files in output directory

Generate the html pages with fabric

    $ ./path/to/venv/bin/activate
    (venv)$ fab build


### Deploying
Maybe `rsync` or S3.


### Testing
Test the build process with

    $ ./path/to/venv/bin/activate
    (venv)$ nosetests
