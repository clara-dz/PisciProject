from database.repository import UserRepository 

class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def login(self, email, password, flask_session):
        # REGRAS DE NEGOCIO BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        
        if not email or not password:
            return {"sucesso": False, "mensagem": "E-mail e senha são obrigatórios."}
        
        # BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        user_db = self.repository.buscar_usuario_por_email(email)

        if not user_db:
            return {"sucesso": False, "mensagem": "Usuário não encontrado."}

        if user_db['Password'] != password:
            return {"sucesso": False, "mensagem": "Senha incorreta."}


        backup_temporaria = flask_session.get('novo_projeto')

        flask_session.clear() 

        if backup_temporaria:
            flask_session['novo_projeto'] = backup_temporaria
        
        flask_session['user_id'] = user_db['User_ID']
        flask_session['user_name'] = user_db['Username'] 
        
        flask_session.modified = True

        return {
            "sucesso": True, 
            "mensagem": f"Bem-vindo(a), {user_db['Username']}!"
        }
    
    def logout(self, flask_session):
        
        if 'user_id' not in flask_session:
            return {"sucesso": False, "mensagem": "Nenhum usuário logado no momento."}

        flask_session.clear()

        return {
            "sucesso": True,
            "mensagem": "Você saiu da sua conta com sucesso."
        }
    
    def register(self, name, email, password, confirma_senha, flask_session):
        # REGRAS DE NEGOCIO BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        if not name or not email or not password:
            return {"sucesso": False, "mensagem": "Nome, e-mail e senha são obrigatórios."}

        if password != confirma_senha:
            return {"sucesso": False, "mensagem": "As senhas não batem"}
        
        if len(password) < 6:
            return {"sucesso": False, "mensagem": "A senha deve ter pelo menos 6 caracteres"}

        usuario_existente = self.repository.buscar_usuario_por_email(email)
        if usuario_existente:
            return {"sucesso": False, "mensagem": "Este e-mail já está em uso. Tente fazer login."}

        # BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        novo_id = self.repository.insert_user(name, email, password)

        if not novo_id:
            return {"sucesso": False, "mensagem": "Erro interno ao criar conta. Tente novamente."}

        backup_temporario = flask_session.get('novo_projeto')
        
        flask_session.clear() 
        
        if backup_temporario:
            flask_session['novo_projeto'] = backup_temporario
            
        flask_session['user_id'] = novo_id
        flask_session['user_name'] = name 
        
        flask_session.modified = True

        return {
            "sucesso": True, 
            "mensagem": f"Conta criada com sucesso! Bem-vindo(a), {name}!"
        }
