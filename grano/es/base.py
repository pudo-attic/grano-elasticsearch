from flask import url_for

from grano.core import app
from grano.model import Project
from grano.interface import Startup
from grano.es.view import blueprint
from grano.es.indexer import Indexer


script_indexer = Indexer()


class Configure(Startup):

    def configure(self, manager):
        #manager.add_command("assets", ManageAssets(assets))
        app.register_blueprint(blueprint)
        

        @manager.command
        def es_index(project=None):
            """ Re-index all entities in the system, or those in a project. """
            if project is not None:
                project = Project.by_slug(project)
                if project is None:
                    raise ValueError("Project not found.")
            script_indexer.index_project(project=project)


        @manager.command
        def es_delete(project=None):
            """ Delete all entities from the index, or those in a project. """
            if project is not None:
                script_indexer.delete_project(project)
            else:
                script_indexer.delete_all()


