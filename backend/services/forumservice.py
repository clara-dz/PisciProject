from database.repository import ForumRepository 

class ForumService:
    def __init__(self):
        self.repository = ForumRepository()

    def listar_comentarios_recentes(self):
        comentarios = self.repository.buscar_ultimos_comentarios()

        return {
            "sucesso": True,
            "dados": comentarios,
            "total": len(comentarios)
        }
    
    def criar_comentario(self, user_id, conteudo, componente_id=None, componente_tipo=None):

        if not user_id:
            return {"sucesso": False, "mensagem": "Você precisa estar logado para comentar."}
            
        if not conteudo or len(conteudo.strip()) == 0:
            return {"sucesso": False, "mensagem": "O texto do comentário não pode estar vazio."}

        # TRATAMENTO DOS PARÂMETROS OPCIONAIS
        # Se o frontend mandou uma string vazia ("") ou um zero (0) no lugar do ID do componente,
        # nós forçamos isso a virar 'None' para que o banco de dados salve como 'NULL'.
        comp_id = componente_id if componente_id else None
        comp_tipo = componente_tipo if componente_tipo else None

        gravou_com_sucesso = self.repository.salvar_comentario(
            user_id=user_id, 
            conteudo=conteudo.strip(), 
            componente_id=comp_id, 
            componente_tipo=comp_tipo
        )

        if gravou_com_sucesso:
            return {"sucesso": True, "mensagem": "Comentário publicado com sucesso!"}
        
        return {"sucesso": False, "mensagem": "Não foi possível publicar seu comentário. Tente novamente mais tarde."}