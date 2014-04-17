from elasticsearch import Elasticsearch

from grano.core import app, app_name
from grano.model import Entity, Project
from grano.logic import entities
from grano.interface import EntityChangeProcessor, ProjectChangeProcessor


es = Elasticsearch()
es_index = app.config.get('ES_INDEX', app_name)


class Indexer(EntityChangeProcessor, ProjectChangeProcessor):

    def index_entity(self, entity):
        """ Index a single entity. """
        if entity.same_as is not None:
            return
        body = entity.to_index()
        es.index(index=es_index, doc_type='entity',
                 id=body.pop('id'), body=body)


    def index_project(self, project=None):
        """ Index an entire project, or the entire database if no
        project is given. """
        q = Entity.all().filter_by(same_as=None)
        if project is not None:
            q = q.filter(Entity.project==project)

        for i, entity in enumerate(q):
            self.index_entity(entity)
            if i > 0 and i % 1000 == 0:
                log.info("Indexed: %s entities", i)
                es.indices.refresh(index=es_index)
        es.indices.refresh(index=es_index)


    def delete_project(self, project_slug):
        field = {'project.slug': project_slug}
        query = {'query': {'term': field}}
        es.delete_by_query(index=es_index, doc_type='entity',
            query=query)


    def delete_all(self):
        es.delete_by_all(index=es_index, doc_type='entity')


    def entity_changed(self, entity_id, operation):
        if operation == 'delete':
            es.delete(index=es_index, doc_type='entity', id=entity_id)
        else:
            entity = Entity.by_id(entity_id)
            if entity is None:
                return
            self.index_entity(entity)
            es.indices.refresh(index=es_index)


    def project_changed(self, project_slug, operation):
        if operation == 'delete':
            self.delete_project(project_slug)

