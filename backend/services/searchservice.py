from database.repository import ComponentRepository 

class SearchService:
    def __init__(self):
        self.repository = ComponentRepository()

    def buscar(self, termo_busca, categoria):
        if termo_busca:
            termo_limpo = termo_busca.strip()
            
            if len(termo_limpo) == 1:
                return {
                    "sucesso": True, # Mantemos True para o frontend não tratar como erro de servidor
                    "dados": [],
                    "total_encontrado": 0,
                    "mensagem": "Por favor, digite pelo menos 2 caracteres para pesquisar."
                }
            
            termo_busca = termo_limpo
        else:
            termo_busca = ""

        resultados = self.repository.buscar_componentes(termo_busca, categoria)

        if len(resultados) == 0:
            msg_erro = f"Nenhum componente encontrado para '{termo_busca}'." if termo_busca else "Nenhum componente cadastrado nesta categoria."
            
            return {
                "sucesso": True,
                "dados": [],
                "total_encontrado": 0,
                "mensagem": msg_erro
            }

        return {
            "sucesso": True,
            "dados": resultados,
            "total_encontrado": len(resultados),
            "mensagem": "Busca realizada com sucesso!"
        }