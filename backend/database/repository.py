from database.connection import DatabaseConnection

class ComponentRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def _executar_busca_simples(self, query, valor_id):
        conexao = self.db.get_connection()
        if not conexao: return None
        
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (valor_id,))
            return cursor.fetchone()
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ==========================================
    # MÉTODOS DE BUSCA DE COMPONENTES
    # ==========================================
    def buscar_cpu(self, cpu_id):
        return self._executar_busca_simples("SELECT * FROM CPU WHERE CPU_ID = %s", cpu_id)

    def buscar_placa_mae(self, mb_id):
        return self._executar_busca_simples("SELECT * FROM `Mother Board` WHERE MB_ID = %s", mb_id)

    def buscar_gpu(self, gpu_id):
        return self._executar_busca_simples("SELECT * FROM GPU WHERE GPU_ID = %s", gpu_id)

    def buscar_ram(self, ram_id):
        return self._executar_busca_simples("SELECT * FROM MEM_RAM WHERE MEM_RAM_ID = %s", ram_id)

    def buscar_ssd(self, ssd_id):
        return self._executar_busca_simples("SELECT * FROM SSD WHERE SSD_ID = %s", ssd_id)

    def buscar_fonte(self, power_id):
        return self._executar_busca_simples("SELECT * FROM POWER WHERE POWER_ID = %s", power_id)
    
    # ===================================================
    # MÉTODO DE BUSCAR UM PROJETO ESPECÍFICO DO USUÁRIO
    # ===================================================
    def buscar_projeto(self, project_id, user_id):
        query = "SELECT * FROM Project WHERE ID = %s AND User_id = %s"
        
        conexao = self.db.get_connection()
        if not conexao: return None
        
        try:
            cursor = conexao.cursor(dictionary=True) 
            cursor.execute(query, (project_id, user_id))
            projeto = cursor.fetchone()
            return projeto
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ==========================================
    # MÉTODOS DE MANIPULAÇÃO DE PROJETOS (UPSERT)
    # ==========================================
    def listar_projetos_usuario(self, user_id):
        
        query = "SELECT ID, Project_Name, Description, Compatibility FROM Project WHERE User_id = %s"
        
        conexao = self.db.get_connection()
        if not conexao: return []
        
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            
            # fetchall() retorna uma lista de dicionários com todos os resultados
            projetos = cursor.fetchall()
            return projetos
        except Exception as e:
            print(f"Erro ao listar projetos: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    # ==========================================
    # MÉTODOS DE MANIPULAÇÃO DE PROJETOS (UPSERT)
    # ==========================================
    def insert_project(self, user_id, name, description, cpu_id, mb_id, gpu_id, ram_id, ssd_id, power_id, compatibility):

        conexao = self.db.get_connection()
        if not conexao: return None

        query = """
            INSERT INTO Project (
                User_id, Project_Name, Description, 
                CPU_ID, MB_ID, GPU_ID, MEM_RAM_ID, SSD_ID, POWER_ID, 
                Compatibility
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (user_id, name, description, cpu_id, mb_id, gpu_id, ram_id, ssd_id, power_id, compatibility)

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

    def update_project(self, project_id, name, description, cpu_id, mb_id, gpu_id, ram_id, ssd_id, power_id, compatibility):

        conexao = self.db.get_connection()
        if not conexao: return False

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

        valores = (name, description, cpu_id, mb_id, gpu_id, ram_id, ssd_id, power_id, compatibility, project_id)

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