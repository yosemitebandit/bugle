A good website, built from yaml and markdown.
A python script grabs all of the docs in the `pages` directory and generates static html.

### Source pages
Each page has meta info at the top in yaml.
The specified title and date are injected into the page template.
Tags are compiled for all pages and used to build an index of sorts.
The route parameter specifies where this page will end up.
A template can be specified, as well as custom CSS and JS.

The second half of each page is the actual content, and it's in markdown.


### Deploying
The source is rendered and then transferred to the server with `rsync`.
It's sort of superfluously driven by fabric.
Just run `fab prod deploy`.
