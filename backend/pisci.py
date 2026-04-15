from flask import Flask, render_template
import os
#from dotenv import load_dotenv (parte do banco de dados)


from routes.api_pc_builder import pc_builder_bp
from routes.api_user import user_bp

#load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder="../frontend", 
                static_folder="../frontend")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # conecta os arquivos da pasta routes ao servidor principal
    app.register_blueprint(pc_builder_bp)
    app.register_blueprint(user_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)