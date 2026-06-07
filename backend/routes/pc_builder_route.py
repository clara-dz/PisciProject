from flask import Blueprint, request, jsonify, session
from services.projectservice import ProjectService

builder_bp = Blueprint('builder', __name__, url_prefix='/project')
project_service = ProjectService()

@builder_bp.route('/add-component', methods=['POST'])
def add_component(): # ------------------------------------------------------------------------------------------------------------------------
    
    dados = request.get_json()
    
    if not dados or 'component_id' not in dados or 'tipo' not in dados:
        return jsonify({"status": "erro", "message": "Dados incompletos enviados pelo frontend."}), 400

    component_id = dados.get('component_id')
    tipo = dados.get('tipo')

    resultado = project_service.add_component(component_id, tipo, session)

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
    
    return jsonify({
        "status": "sucesso",
        "message": "Novo projeto de PC iniciado com sucesso!",
        "projeto_vazio": resultado["projeto"]
    }), 200

@builder_bp.route('/remove-component', methods=['POST'])
def remove_component(): # --------------------------------------------------------------------------------------------------------------------

    dados = request.get_json()
    tipo = dados.get('tipo') # O frontend vai enviar qual slot quer limpar (ex: 'GPU', 'CPU')
    
    if not tipo:
        return jsonify({"status": "erro", "message": "O tipo do componente não foi informado."}), 400
        
    resultado = project_service.remove_component(tipo, session)
    
    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400
        
    return jsonify({
        "status": "sucesso",
        "message": f"Componente do tipo {tipo} removido com sucesso!",
        "projeto": resultado["projeto"],
        "compatibilidade": resultado["compatibilidade"]
    }), 200

@builder_bp.route('/save', methods=['POST'])
def save_project(): # ---------------------------------------------------------------------------------------------------------------------
    # 1. Verifica autenticação
    if 'user_id' not in session:
        return jsonify({"status": "erro", "message": "Você precisa estar logado para salvar."}), 401

    dados = request.get_json() or {}
    nome = dados.get('name')
    descricao = dados.get('description')

    resultado = project_service.save_project(session, nome, descricao)
    
    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400
        
    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"],
        "project_id": resultado["project_id"]
    }), 200

@builder_bp.route('/load-project/<int:project_id>', methods=['GET'])
def load_project_route(project_id): # -----------------------------------------------------------------------------------------------------
    # Trava de segurança: usuário precisa estar logado
    if 'user_id' not in session:
        return jsonify({"status": "erro", "message": "Você precisa estar logado para carregar um projeto."}), 401

    resultado = project_service.load_project(project_id, session)
    
    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400
        
    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"],
        "projeto": resultado["projeto"]
    }), 200

@builder_bp.route('/my-projects', methods=['GET'])
def list_user_projects():

    if 'user_id' not in session:
        return jsonify({"status": "erro", "message": "Você precisa estar logado para listar seus projetos."}), 401

    resultado = project_service.get_user_projects(session)
    
    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400
        
    return jsonify({
        "status": "sucesso",
        "projetos": resultado["projetos"]
    }), 200
