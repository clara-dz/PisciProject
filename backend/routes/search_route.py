from flask import Blueprint, request, jsonify
# Importe o seu SearchService de onde ele estiver salvo
from services.searchservice import SearchService 

search_bp = Blueprint('search', __name__, url_prefix='/catalog')
search_service = SearchService()

@search_bp.route('/components', methods=['GET'])
def list_components():
    # 1. Pega os parâmetros da URL.
    # Baseado no seu exemplo (/catalog/components?type=CPU&q=RTX)
    # Trocamos 'category' por 'type' para ficar igual ao seu comentário, e mantemos 'q' para o texto.
    categoria_solicitada = request.args.get('type', '') 
    termo_buscado = request.args.get('q', '')

    # 2. Aciona o SearchService
    # O Service vai repassar para o Repositório, que vai abrir a conexão que ele mesmo criou.
    resultado = search_service.buscar(termo_busca=termo_buscado, categoria=categoria_solicitada)

    # 3. Retorna a resposta para o Frontend
    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"],
        "total": resultado["total_encontrado"],
        "data": resultado["dados"]
    }), 200