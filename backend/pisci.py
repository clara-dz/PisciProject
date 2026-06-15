from flask import Flask, render_template
import os
# from dotenv import load_dotenv

# Importando os 4 Blueprints que mapeamos na arquitetura
from routes.auth_route import auth_bp
from routes.pc_builder_route import builder_bp
from routes.search_route import search_bp
from routes.forum_route import forum_bp

# load_dotenv()

def create_app():
    # Mantendo a sua excelente configuração de separação do Frontend
    app = Flask(__name__, 
                template_folder="../frontend", 
                static_folder="../frontend",
                static_url_path="")

    # Configuração da chave secreta (usada pelas sessions)
    # Dica: adicionei um fallback caso o .env ainda não esteja ativo, 
    # assim o app não "quebra" enquanto você desenvolve localmente.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_provisoria_piscis')

    # Registrando todas as "portas de entrada" no servidor
    app.register_blueprint(auth_bp)
    app.register_blueprint(builder_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(forum_bp)

    # Rota raiz: O primeiro contato do usuário com o sistema
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/<path:page>')
    def frontend_page(page):
        return render_template(page)

    return app

if __name__ == '__main__':
    # O bloco __main__ garante que o servidor só suba se o arquivo for executado diretamente
    app = create_app()
    app.run(debug=True, port=5000)