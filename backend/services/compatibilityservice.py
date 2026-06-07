class CompatibilityService:
    
    def check_compatibility(self, project_obj):


        project_obj.Compatibility = True
        all_warnings = []

        if project_obj.CPU:
            # Passa o próprio componente de dentro do projeto para a função analítica
            resultado_cpu = self._analisa_CPU(project_obj, project_obj.CPU)
            all_warnings.extend(resultado_cpu.get("warnings", []))

        if project_obj.Mb:
            resultado_mb = self._analisa_MB(project_obj, project_obj.Mb)
            all_warnings.extend(resultado_mb.get("warnings", []))

        if project_obj.GPU:
            resultado_gpu = self._analisa_GPU(project_obj, project_obj.GPU)
            all_warnings.extend(resultado_gpu.get("warnings", []))

        if project_obj.MEM_RAM:
            resultado_ram = self._analisa_RAM(project_obj, project_obj.MEM_RAM)
            all_warnings.extend(resultado_ram.get("warnings", []))

        if project_obj.Power:
            resultado_fonte = self._analisa_Fonte(project_obj, project_obj.Power)
            all_warnings.extend(resultado_fonte.get("warnings", []))
            
        is_compatible = project_obj.Compatibility

        return {
            "is_compatible": is_compatible,
            "warnings": all_warnings
        }
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

    def _analisa_GPU(self, projeto_completo, GPU_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass

    def _analisa_SSD(self, projeto_completo, SSD_novo):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass

    def _analisa_RAM(self, projeto_completo, MEM_RAM_nova):
        # Exemplo rápido de como seria outra análise isolada
        # total_watts = calcular_soma_de_watts(projeto_completo)
        # se fonte_nova.potencia < total_watts: compativel = False...
        pass