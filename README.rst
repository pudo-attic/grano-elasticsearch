Grano ElasticSearch Support
===========================

`grano <http://grano.cc/>`_ is a toolkit for building journalistic social
network analysis applications on the web. This package contains full-text
search support based on ElasticSearch. 


Installation
------------

``grano-ui`` requires that you have installed and configured
`grano <http://grano.cc/>`_. Please refer to `grano's documentation <http://docs.grano.cc/>`_
for further instructions. Afterwards, install the ``grano-elasticsearch``
package (from PyPI or source) into the same virtual environment. You will
also need to install and configure ElasticSearch.


Web API
-------

This plugin provides the following public API to expose full-text search:

::

    GET /api/1/entities/_search

Full-text search API for entitues. Given a query, the API will return a set 
of ElasticSearch results (i.e. not complete entity serializations). Standard
:ref:`pager` arguments are available.

* ``q`` the term to be searched.
* ``filter-<name>`` filter field ``<name>`` for the given value.
* ``facet`` add the value of the argument as a facet field. This argument 
  can be supplied multiple times to have more than one facet.
* ``facet-size`` can be used to specify the number of results to be returned
  for each ``facet``.


Management commands
-------------------

In order to manage the index, the plugin exposes a set of management commands.
Some examples::

    # re-index all projects:
    $ grano es_index 
    
    # re-index a specific project (by slug):
    $ grano es_index -p my_project

    # delete all data in the index:
    $ grano es_delete

    # delete all data in a specific project:
    $ grano es_delete -p my_project


Configuration
-------------

By default, ``grano-elasticsearch`` will deploy itself and add its endpoint to
the ``grano`` API. To specify the name of the ElasticSearch index, you can set
the ``ES_INDEX`` setting in your ``grano`` configuration file. If no index name
is specified, the application's name (``APP_NAME``) will be used.
