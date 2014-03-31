from flask import Blueprint, render_template, request
from flask import redirect, make_response, url_for

from grano.lib.serialisation import jsonify
from grano.lib.pager import Pager
from grano.core import app, url_for
from grano.logic import entities
from grano.model import Entity

from grano.es.searcher import Searcher


blueprint = Blueprint('es', __name__)


@blueprint.route('/api/1/entities/_search', methods=['GET'])
def search():
    searcher = Searcher(request.args)
    if 'project' in request.args:
        searcher.add_filter('project.slug', request.args.get('project'))
    pager = Pager(searcher)
    
    def convert(serp):
        ents = Entity.by_id_many([r['id'] for r in serp], request.account)
        results = [ents.get(r['id']) for r in serp]
        results = [entities.to_rest_index(r) for r in results]
        return results

    data = pager.to_dict(results_converter=convert)
    data['facets'] = searcher.facets()
    return jsonify(data)
