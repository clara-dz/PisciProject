class CompatibilityService:
    
    def check_compatibility(self, project_obj, novo_componente_obj, tipo):

        # Se não enviou objeto válido, aprova direto para não quebrar
        if not novo_componente_obj:
            return {"is_compatible": True, "warnings": []}

        # O seu sistema de roteamento!
        if tipo == 'CPU':
            return self._analisa_CPU(project_obj, novo_componente_obj)
            
        elif tipo == 'MotherBoard':
            return self._analisa_MB(project_obj, novo_componente_obj)
            
        elif tipo == 'Power':
            return self._analisa_Fonte(project_obj, novo_componente_obj)
        
        elif tipo == 'GPU':
            return self._analisa_GPU(project_obj, novo_componente_obj)
        
        elif tipo == 'SSD':
            return self._analisa_SSD(project_obj, novo_componente_obj)

        elif tipo == 'MEM_RAM':
            return self._analisa_RAM(project_obj, novo_componente_obj)
            
        # Se for um componente que ainda não tem regra (ex: SSD), passa direto
        return {"is_compatible": True, "warnings": []}

    # ========================================================================
    # AS FUNÇÕES ESPECIALISTAS (Privadas)
    # ========================================================================
    
    def _analisa_CPU(self, projeto_completo, cpu_nova):
        avisos = []
        compativel = True

        # A CPU nova precisa conversar com a Placa-Mãe (se a placa já estiver no projeto)
        if projeto_completo.Mb:
            if cpu_nova.socket != projeto_completo.Mb.socket:
                compativel = False
                avisos.append(f"Incompatível: A CPU usa {cpu_nova.socket} e a Placa-Mãe usa {projeto_completo.Mb.socket}.")

        # Futuro: A CPU também pode ser analisada contra a memória RAM, etc.

        return {"is_compatible": compativel, "warnings": avisos}

    def _analisa_MB(self, projeto_completo, mb_nova):
        avisos = []
        compativel = True

        # A Placa-Mãe nova precisa conversar com a CPU (se a CPU já estiver no projeto)
        if projeto_completo.CPU:
            if mb_nova.socket != projeto_completo.CPU.socket:
                compativel = False
                avisos.append(f"Atenção: Essa Placa-Mãe ({mb_nova.socket}) não suporta a CPU escolhida ({projeto_completo.CPU.socket}).")

        return {"is_compatible": compativel, "warnings": avisos}

    def _analisa_Fonte(self, projeto_completo, fonte_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass

    def _analisa_GPU(self, projeto_completo, fonte_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass

    def _analisa_SSD(self, projeto_completo, fonte_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass

    def _analisa_RAM(self, projeto_completo, fonte_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass