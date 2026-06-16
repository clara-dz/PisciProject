from flask import Blueprint, request, jsonify, session
from services.projectservice import ProjectService

builder_bp = Blueprint('builder', __name__, url_prefix='/project')
project_service = ProjectService()


@builder_bp.route('/current', methods=['GET'])
def current_project():
    resultado = project_service.get_current_project(session)
    return jsonify({
        "status": "sucesso",
        "projeto": resultado["projeto"],
        "detalhes": resultado["detalhes"],
        "compatibilidade": resultado["compatibilidade"],
        "project_id": resultado["project_id"],
        "project_name": resultado["project_name"],
        "project_description": resultado["project_description"],
    }), 200


@builder_bp.route('/start', methods=['POST'])
def start_project():
    resultado = project_service.start_new_project(session)
    return jsonify({
        "status": "sucesso",
        "message": "Novo projeto iniciado com sucesso!",
        "projeto": resultado["projeto"],
        "detalhes": resultado["detalhes"],
    }), 200


@builder_bp.route('/add-component', methods=['POST'])
def add_component():
    dados = request.get_json() or {}

    if 'component_id' not in dados or 'tipo' not in dados:
        return jsonify({"status": "erro", "message": "Dados incompletos enviados pelo frontend."}), 400

    resultado = project_service.add_component(
        component_id=dados.get('component_id'),
        tipo=dados.get('tipo'),
        flask_session=session,
    )

    if not resultado["sucesso"]:
        return jsonify({
            "status": "erro",
            "message": resultado.get("mensagem", "Erro ao adicionar componente."),
            "projeto": resultado.get("projeto"),
            "detalhes": resultado.get("detalhes"),
            "compatibilidade": resultado.get("compatibilidade"),
        }), 400

    return jsonify({
        "status": "sucesso",
        "message": f"{dados.get('tipo')} adicionado ao projeto!",
        "projeto": resultado["projeto"],
        "detalhes": resultado["detalhes"],
        "compatibilidade": resultado["compatibilidade"],
    }), 200


@builder_bp.route('/remove-component', methods=['POST'])
def remove_component():
    dados = request.get_json() or {}
    tipo = dados.get('tipo')

    if not tipo:
        return jsonify({"status": "erro", "message": "O tipo do componente não foi informado."}), 400

    resultado = project_service.remove_component(tipo, session)

    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({
        "status": "sucesso",
        "message": f"Componente {tipo} removido com sucesso!",
        "projeto": resultado["projeto"],
        "detalhes": resultado["detalhes"],
        "compatibilidade": resultado["compatibilidade"],
    }), 200


@builder_bp.route('/save', methods=['POST'])
def save_project():
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
        "project_id": resultado["project_id"],
    }), 200


@builder_bp.route('/load-project/<int:project_id>', methods=['GET'])
def load_project_route(project_id):
    if 'user_id' not in session:
        return jsonify({"status": "erro", "message": "Você precisa estar logado para carregar um projeto."}), 401

    resultado = project_service.load_project(project_id, session)

    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"],
        "projeto": resultado["projeto"],
        "detalhes": resultado["detalhes"],
        "compatibilidade": resultado["compatibilidade"],
    }), 200


@builder_bp.route('/my-projects', methods=['GET'])
def list_user_projects():
    if 'user_id' not in session:
        return jsonify({"status": "erro", "message": "Você precisa estar logado para listar seus projetos."}), 401

    resultado = project_service.get_user_projects(session)

    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({"status": "sucesso", "projetos": resultado["projetos"]}), 200
