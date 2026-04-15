# from database.connection import get_db_connection

def registrar_user(name, email, senha):

    #db = get_db_cursor()
    #cursor = db_cursor()
    '''
    try:
        # Verifica se o e-mail já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "E-mail já cadastrado."

        # Gera o hash da senha
        senha_hash = generate_password_hash(senha)
        
        # Insere o novo usuário
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, senha_hash))
        db.commit() # Salva as alterações no banco
        return True, "Usuário registrado com sucesso!"
    
    except Exception as e:
        return False, f"Erro no banco: {str(e)}"
    finally:
        close_connection(db, cursor)
    '''
    return True
def autenticar_user(email, senha_digitada):
    '''
    db = get_db_connection()
    cursor = db.cursor(dictionary=True) # Retorna como dicionário para facilitar
    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['senha'], senha_digitada):
            return True, usuario # Retorna o dicionário completo do usuário
        return False, None
    finally:
        close_connection(db, cursor)
    '''
    return True