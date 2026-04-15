from flask import Blueprint, render_template, request
#from database.connection import get_db_connection
# Aqui você importaria seus modelos conforme necessário
# from models.cpu import CPU 

pc_builder_bp = Blueprint('pc_builder', __name__)

@pc_builder_bp.route('/montar')
def montar():
    # Exemplo: Buscando peças para listar na página de montagem
    # db = get_db_connection()
    # cursor = db.cursor(dictionary=True)
    # cursor.execute("SELECT * FROM cpus")
    # cpus = cursor.fetchall()
    
    return render_template('montarprojeto.html')

@pc_builder_bp.route('/pesquisar')
def pesquisar():
    return render_template('pesquisar.html')