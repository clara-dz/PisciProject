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
        categorias_validas = {
            "CPU",
            "Placa Mãe",
            "Memória RAM",
            "GPU",
            "SSD",
            "Fonte",
            "Site"
        }

        if not user_id:
            return {
                "sucesso": False,
                "mensagem": "Você precisa estar logado para comentar."
            }

        if not conteudo or len(conteudo.strip()) == 0:
            return {
                "sucesso": False,
                "mensagem": "O texto do comentário não pode estar vazio."
            }

        if not componente_tipo or len(str(componente_tipo).strip()) == 0:
            return {
                "sucesso": False,
                "mensagem": "Selecione uma categoria para o comentário."
            }

        componente_tipo = str(componente_tipo).strip()

        if componente_tipo not in categorias_validas:
            return {
                "sucesso": False,
                "mensagem": "Categoria de comentário inválida."
            }

        comp_id = componente_id if componente_id else None

        gravou_com_sucesso = self.repository.salvar_comentario(
            user_id=user_id,
            conteudo=conteudo.strip(),
            componente_id=comp_id,
            componente_tipo=componente_tipo
        )

        if gravou_com_sucesso:
            return {
                "sucesso": True,
                "mensagem": "Comentário publicado com sucesso!"
            }

        return {
            "sucesso": False,
            "mensagem": "Não foi possível publicar seu comentário. Tente novamente mais tarde."
        }