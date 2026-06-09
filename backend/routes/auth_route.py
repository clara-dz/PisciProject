from flask import Blueprint, request, jsonify, session
from services.authservice import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json() or {}
    email = dados.get('email')
    senha = dados.get('password')

    resultado = auth_service.login(email, senha, session)

    if not resultado["sucesso"]:
        # 401 é o código HTTP correto para "Não Autorizado / Falha de Login"
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 401

    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"]
    }), 200    


@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json() or {}
    nome = dados.get('name')
    email = dados.get('email')
    senha = dados.get('password')
    confirma_senha = dados.get('confirm_password')

    resultado = auth_service.register(nome, email, senha, confirma_senha, session)

    if not resultado["sucesso"]:
        # 400 é o código para "Bad Request" (dados inválidos ou duplicados)
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"]
    }), 201 # 201 é o código HTTP oficial para "Criado com sucesso"

@auth_bp.route('/logout', methods=['POST'])
def logout():
    resultado = auth_service.logout(session)

    if not resultado["sucesso"]:
        return jsonify({"status": "erro", "message": resultado["mensagem"]}), 400

    return jsonify({
        "status": "sucesso",
        "message": resultado["mensagem"]
    }), 200
    pass