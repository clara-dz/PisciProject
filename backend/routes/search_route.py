from flask import Blueprint

search_bp = Blueprint('search', __name__, url_prefix='/catalog')

@search_bp.route('/components', methods=['GET'])
def list_components():
    # Pega parâmetros da URL (ex: /catalog/components?type=CPU&brand=Intel)
    # Aciona o SearchService para filtrar no banco de dados
    pass