from database.connection import DatabaseConnection

class ComponentRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def _executar_busca_simples(self, query, valor_id):
        """Função interna auxiliar para não repetirmos código em todo método."""
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
    # MÉTODOS DE BUSCA ESPECÍFICOS (Baseados no seu ER)
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