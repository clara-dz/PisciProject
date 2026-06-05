from flask import Blueprint, request, jsonify, session
from services.projectservice import ProjectService

builder_bp = Blueprint('builder', __name__, url_prefix='/project')
project_service = ProjectService()

@builder_bp.route('/add-component', methods=['POST'])
def add_component(): # ------------------------------------------------------------------------------------------------------------------------
    # Recebe ID da peça, aciona o ProjectService (e CompatibilityService)
    # 1. Recebe os dados assumindo que o Frontend mandou corretamente
    dados = request.get_json()
    
    # 2. Validação de segurança (fail-fast)
    if not dados or 'component_id' not in dados or 'tipo' not in dados:
        return jsonify({"status": "erro", "message": "Dados incompletos enviados pelo frontend."}), 400

    component_id = dados.get('component_id')
    tipo = dados.get('tipo')

    # 3. Passa a bola para o Service processar a lógica de negócio
    resultado = project_service.add_component(component_id, tipo, session)

    # 4. Devolve a resposta estruturada para o JavaScript
    if resultado["sucesso"]:
        return jsonify({
            "status": "sucesso",
            "message": f"{tipo} adicionado ao projeto!",
            "projeto_atual": resultado["projeto"],
            "relatorio_compatibilidade": resultado["compatibilidade"]
        }), 200
    else:
        return jsonify({"status": "erro", "message": resultado["message"]}), 400


@builder_bp.route('/start', methods=['POST'])
def start_project(): # ---------------------------------------------------------------------------------------------------------------------
    # Chama o serviço para limpar/iniciar a sessão
    resultado = project_service.start_new_project(session)
    
    # Devolve o sinal verde para o Frontend
    return jsonify({
        "status": "sucesso",
        "message": "Novo projeto de PC iniciado com sucesso!",
        "projeto_vazio": resultado["projeto"]
    }), 200


@builder_bp.route('/remove-component', methods=['POST'])
def remove_component(): # --------------------------------------------------------------------------------------------------------------------
    # Recebe o tipo da peça e remove da sessão ou do banco
    pass

@builder_bp.route('/save', methods=['POST'])
def save_project():
    # Move o projeto da sessão para o banco (exige login)
    pass

@builder_bp.route('/<int:project_id>', methods=['GET'])
def load_project(project_id):
    # Carrega os dados de um projeto específico para a tela
    pass

@builder_bp.route('/my-projects', methods=['GET'])
def list_user_projects():
    # Traz a lista de todos os projetos salvos do usuário logado
    pass
