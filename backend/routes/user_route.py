from flask import Blueprint, render_template, request, redirect, url_for

user_bp = Blueprint('user', __name__)

@user_bp.route('/login')
def login():
    return render_template('login.html')

@user_bp.route('/registro')
def registro():
    return render_template('registro.html')

@user_bp.route('/forum')
def forum():
    return render_template('forum.html')