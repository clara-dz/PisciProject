from flask import Blueprint

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')

@forum_bp.route('/comments/<int:component_id>', methods=['GET'])
def get_comments(component_id):
    # Busca todos os comentários vinculados a uma peça específica
    pass

@forum_bp.route('/comments', methods=['POST'])
def post_comment():
    # Recebe texto e ID do componente, salva no banco (exige login)
    pass