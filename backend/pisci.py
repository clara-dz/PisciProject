from flask import Flask, render_template
import os
##rom dotenv import load_dotenv

# Importando os Blueprints que acabamos de criar
from routes.pc_builder import pc_builder_bp
from routes.user import user_bp

#load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder="../frontend", 
                static_folder="../frontend")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # --- REGISTRO DOS BLUEPRINTS ---
    # Isso conecta os arquivos da pasta routes ao servidor principal
    app.register_blueprint(pc_builder_bp)
    app.register_blueprint(user_bp)

    # Rota da página inicial (Home)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)