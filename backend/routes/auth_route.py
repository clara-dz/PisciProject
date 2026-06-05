from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    # Recebe email/senha, valida e salva o user_id na sessão
    pass

@auth_bp.route('/register', methods=['POST'])
def register():
    # Recebe os dados, cria o usuário no banco
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Limpa a sessão (remove user_id e projetos temporários)
    pass