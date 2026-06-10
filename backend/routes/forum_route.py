from flask import Blueprint, jsonify, session, request
from services.forumservice import ForumService

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')
forum_service = ForumService()

@forum_bp.route('/comments', methods=['GET'])
def get_comments():
    resultado = forum_service.listar_comentarios_recentes()

    return jsonify({
        "status": "sucesso",
        "total": resultado["total"],
        "data": resultado["dados"]
    }), 200

@forum_bp.route('/comments', methods=['POST'])
def post_comment():

    dados_do_front = request.get_json() or {}
    
    texto = dados_do_front.get('content', '')
    comp_id = dados_do_front.get('componentId', None)
    comp_tipo = dados_do_front.get('componentType', None)

    user_id = session.get('user_id') 

    resultado = forum_service.criar_comentario(
        user_id=user_id, 
        conteudo=texto, 
        componente_id=comp_id, 
        componente_tipo=comp_tipo
    )

    if not resultado["sucesso"]:
        # Status 400 (Bad Request): Significa que o cliente mandou algo errado 
        # (ex: tentou comentar vazio ou não está logado)
        return jsonify({
            "status": "erro", 
            "message": resultado["mensagem"]
        }), 400

    # Status 201 (Created): É o status HTTP padrão e profissional para indicar 
    # que um novo recurso (o comentário) foi CRIADO com sucesso no servidor!
    return jsonify({
        "status": "sucesso", 
        "message": resultado["mensagem"]
    }), 201