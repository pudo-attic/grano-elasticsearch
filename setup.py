import os
from setuptools import setup, find_packages

setup(
    name='grano-elasticsearch',
    version=os.environ.get('GRANO_RELEASE', '0.3.2'),
    description="An entity and social network tracking software for news applications (ElasticSearch support)",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords='sql graph sna networks journalism ddj elasticsearch',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/granoproject/grano-elasticsearch',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grano>=0.3.1',
        'elasticsearch>=0.4.4'
    ],
    entry_points={
        'grano.startup': [
            'es_boot = grano.es.base:Configure'
        ],
        'grano.entity.change': [
            'es_entity_indexer = grano.es.indexer:Indexer'
        ],
        'grano.project.change': [
            'es_project_indexer = grano.es.indexer:Indexer'
        ]
    },
    tests_require=[]
)
