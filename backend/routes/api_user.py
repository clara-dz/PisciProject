from flask import Blueprint, render_template, request, redirect, url_for
from services.auth import autenticar_user, registrar_user

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/api/login', methods=['POST'])
def login():
    data = request.json # O JS envia dados em formato JSON
    res = autenticar_user(data.get('email'), data.get('senha'))
    '''
    if res['sucesso']:
        session['user_id'] = res['user_id']
    
    return jsonify(res)
    '''