from database.connection import DatabaseConnection
import base64


class ComponentRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def _executar_busca_simples(self, query, valor_id):
        conexao = self.db.get_connection()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (valor_id,))
            return cursor.fetchone()
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ==========================================
    # MÉTODOS DE BUSCA DE COMPONENTES POR ID
    # ==========================================
    def buscar_cpu(self, cpu_id):
        return self._executar_busca_simples(
            "SELECT * FROM CPU WHERE CPU_ID = %s",
            cpu_id
        )

    def buscar_placa_mae(self, mb_id):
        return self._executar_busca_simples(
            "SELECT * FROM MotherBoard WHERE MB_ID = %s",
            mb_id
        )

    def buscar_gpu(self, gpu_id):
        return self._executar_busca_simples(
            "SELECT * FROM GPU WHERE GPU_ID = %s",
            gpu_id
        )

    def buscar_ram(self, ram_id):
        return self._executar_busca_simples(
            "SELECT * FROM MEM_RAM WHERE MEM_RAM_ID = %s",
            ram_id
        )

    def buscar_ssd(self, ssd_id):
        return self._executar_busca_simples(
            "SELECT * FROM SSD WHERE SSD_ID = %s",
            ssd_id
        )

    def buscar_fonte(self, power_id):
        return self._executar_busca_simples(
            "SELECT * FROM POWER WHERE POWER_ID = %s",
            power_id
        )

    # ===================================================
    # BUSCAR UM PROJETO ESPECÍFICO DO USUÁRIO
    # ===================================================
    def buscar_projeto(self, project_id, user_id):
        query = "SELECT * FROM Project WHERE ID = %s AND User_id = %s"

        conexao = self.db.get_connection()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (project_id, user_id))
            projeto = cursor.fetchone()
            return projeto
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ===================================================
    # LISTAR PROJETOS DO USUÁRIO
    # ===================================================
    def listar_projetos_usuario(self, user_id):
        query = """
            SELECT ID, Project_Name, Description, Compatibility
            FROM Project
            WHERE User_id = %s
        """

        conexao = self.db.get_connection()
        if not conexao:
            return []

        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            projetos = cursor.fetchall()
            return projetos
        except Exception as e:
            print(f"Erro ao listar projetos: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ===================================================
    # INSERIR PROJETO
    # ===================================================
    def insert_project(
        self,
        user_id,
        name,
        description,
        cpu_id,
        mb_id,
        gpu_id,
        ram_id,
        ssd_id,
        power_id,
        compatibility
    ):
        conexao = self.db.get_connection()
        if not conexao:
            return None

        query = """
            INSERT INTO Project (
                User_id,
                Project_Name,
                Description,
                CPU_ID,
                MB_ID,
                GPU_ID,
                MEM_RAM_ID,
                SSD_ID,
                POWER_ID,
                Compatibility
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            user_id,
            name,
            description,
            cpu_id,
            mb_id,
            gpu_id,
            ram_id,
            ssd_id,
            power_id,
            compatibility
        )

        try:
            cursor = conexao.cursor()
            cursor.execute(query, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ===================================================
    # ATUALIZAR PROJETO
    # ===================================================
    def update_project(
        self,
        project_id,
        name,
        description,
        cpu_id,
        mb_id,
        gpu_id,
        ram_id,
        ssd_id,
        power_id,
        compatibility
    ):
        conexao = self.db.get_connection()
        if not conexao:
            return False

        query = """
            UPDATE Project
            SET
                Project_Name = %s,
                Description = %s,
                CPU_ID = %s,
                MB_ID = %s,
                GPU_ID = %s,
                MEM_RAM_ID = %s,
                SSD_ID = %s,
                POWER_ID = %s,
                Compatibility = %s
            WHERE ID = %s
        """

        valores = (
            name,
            description,
            cpu_id,
            mb_id,
            gpu_id,
            ram_id,
            ssd_id,
            power_id,
            compatibility,
            project_id
        )

        try:
            cursor = conexao.cursor()
            cursor.execute(query, valores)
            conexao.commit()
            return True
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ===================================================
    # BUSCA GERAL DE COMPONENTES
    # ===================================================
    def buscar_componentes(self, termo, categoria=None):
        tabelas_validas = {
            'CPU': {
                'tabela': 'CPU',
                'id': 'CPU_ID',
                'categoria': 'CPU'
            },
            'GPU': {
                'tabela': 'GPU',
                'id': 'GPU_ID',
                'categoria': 'GPU'
            },
            'MOTHERBOARD': {
                'tabela': 'MotherBoard',
                'id': 'MB_ID',
                'categoria': 'MOTHERBOARD'
            },
            'PLACA_MAE': {
                'tabela': 'MotherBoard',
                'id': 'MB_ID',
                'categoria': 'MOTHERBOARD'
            },
            'PLACA-MAE': {
                'tabela': 'MotherBoard',
                'id': 'MB_ID',
                'categoria': 'MOTHERBOARD'
            },
            'RAM': {
                'tabela': 'MEM_RAM',
                'id': 'MEM_RAM_ID',
                'categoria': 'RAM'
            },
            'MEMORIA_RAM': {
                'tabela': 'MEM_RAM',
                'id': 'MEM_RAM_ID',
                'categoria': 'RAM'
            },
            'SSD': {
                'tabela': 'SSD',
                'id': 'SSD_ID',
                'categoria': 'SSD'
            },
            'ARMAZENAMENTO': {
                'tabela': 'SSD',
                'id': 'SSD_ID',
                'categoria': 'SSD'
            },
            'POWER': {
                'tabela': 'POWER',
                'id': 'POWER_ID',
                'categoria': 'POWER'
            },
            'FONTE': {
                'tabela': 'POWER',
                'id': 'POWER_ID',
                'categoria': 'POWER'
            }
        }

        resultados_finais = []
        termo_like = f"%{termo}%" if termo else "%"

        if categoria:
            chave = categoria.upper()
            tabelas_para_buscar = [tabelas_validas[chave]] if chave in tabelas_validas else []
        else:
            tabelas_para_buscar = [
                tabelas_validas['CPU'],
                tabelas_validas['GPU'],
                tabelas_validas['MOTHERBOARD'],
                tabelas_validas['RAM'],
                tabelas_validas['SSD'],
                tabelas_validas['POWER']
            ]

        conexao = self.db.get_connection()
        if not conexao:
            return []

        try:
            cursor = conexao.cursor(dictionary=True)

            for config in tabelas_para_buscar:
                tabela = config['tabela']
                coluna_id = config['id']
                categoria_nome = config['categoria']

                query = f"""
                    SELECT
                        {coluna_id} AS ID,
                        Name,
                        Manufacturer,
                        Image_Data AS Image,
                        '{categoria_nome}' AS Categoria
                    FROM {tabela}
                    WHERE Name LIKE %s
                    LIMIT 50
                """

                cursor.execute(query, (termo_like,))
                pecas_da_tabela = cursor.fetchall()

                for peca in pecas_da_tabela:
                    if peca['Image']:
                        try:
                            imagem_codificada = base64.b64encode(peca['Image']).decode('utf-8')
                            peca['Image'] = f"data:image/jpeg;base64,{imagem_codificada}"
                        except Exception as img_err:
                            print(f"Erro ao converter imagem da peça ID {peca['ID']}: {img_err}")
                            peca['Image'] = None
                    else:
                        peca['Image'] = None

                    resultados_finais.append(peca)

            return resultados_finais

        except Exception as e:
            print(f"Erro no banco de dados durante a busca: {e}")
            return []

        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()


class UserRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def buscar_usuario_por_email(self, email):
        query = "SELECT * FROM User WHERE Email = %s"

        conexao = self.db.get_connection()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (email,))
            return cursor.fetchone()
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def insert_user(self, name, email, password):
        query = "INSERT INTO User (Username, Email, Password) VALUES (%s, %s, %s)"

        conexao = self.db.get_connection()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            cursor.execute(query, (name, email, password))
            conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()


class ForumRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def buscar_ultimos_comentarios(self):
        conexao = self.db.get_connection()
        if not conexao:
            return []

        try:
            cursor = conexao.cursor(dictionary=True)

            query = """
                SELECT
                    c.ID,
                    c.Content,
                    u.Name AS AuthorName
                FROM Comments c
                JOIN Users u ON c.UserID = u.ID
                ORDER BY c.ID DESC
                LIMIT 15
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar comentários do fórum: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def salvar_comentario(self, user_id, conteudo, componente_id=None, componente_tipo=None):
        conexao = self.db.get_connection()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()

            query = """
                INSERT INTO Comments (UserID, Content, ComponentID, ComponentType)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (user_id, conteudo, componente_id, componente_tipo))
            conexao.commit()
            return True

        except Exception as e:
            if conexao.is_connected():
                conexao.rollback()

            print(f"Erro ao inserir comentário no banco: {e}")
            return False

        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
