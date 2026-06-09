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
            
        if project_obj.SSD:
            resultado_fonte = self._analisa_SSD(project_obj, project_obj.SSD)
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

        # A CPU nova precisa conversar com a Placa-Mãe (se a placa já estiver no projeto)
        if projeto_completo.Mb:
            if cpu_nova.CPU_Socket != projeto_completo.Mb.MB_Socket:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A CPU usa {cpu_nova.socket} e a Placa-Mãe usa {projeto_completo.Mb.socket}.")
        
        if not projeto_completo.Gpu:
            if not cpu_nova.have_gpu:
                projeto_completo.Compatibility = False
                avisos.append("Incompatível: A CPU escolhida não possui vídeo integrado e o projeto não tem uma Placa de Vídeo dedicada.")

        return { "warnings": avisos}

    def _analisa_MB(self, projeto_completo, mb_nova):
        avisos = []

        # 1. Validação Reversa: CPU (Soquete)
        if projeto_completo.Cpu:
            if mb_nova.socket != projeto_completo.Cpu.socket:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A Placa-Mãe usa soquete {mb_nova.socket}, mas a CPU já escolhida exige {projeto_completo.Cpu.socket}.")

        # 2. Validação Reversa: Memória RAM
        if projeto_completo.Ram:
            # Checa Geração (DDR4, DDR5, etc)
            if mb_nova.ram_type.strip().upper() != projeto_completo.Ram.ram_type.strip().upper():
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A Placa-Mãe suporta {mb_nova.ram_type}, mas a RAM escolhida é {projeto_completo.Ram.ram_type}.")
            
            # Checa Capacidade Máxima
            if projeto_completo.Ram.capacity > mb_nova.ram_max_cap:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A Placa-Mãe suporta no máximo {mb_nova.ram_max_cap}GB de RAM, mas a memória escolhida tem {projeto_completo.Ram.capacity}GB.")
            
            # Checa Velocidade (Gera apenas aviso de underclock)
            if projeto_completo.Ram.velocity > mb_nova.ram_max_vel:
                avisos.append(f"Aviso de Otimização: A Placa-Mãe limitará a velocidade da sua RAM de {projeto_completo.Ram.velocity}MHz para o máximo suportado de {mb_nova.ram_max_vel}MHz.")

        # 3. Validação Reversa: Placa de Vídeo (PCIe)
        if projeto_completo.Gpu:
            if mb_nova.pcie_version != projeto_completo.Gpu.pcie_version:
                avisos.append(f"Aviso de Performance: A Placa-Mãe possui slot PCIe {mb_nova.pcie_version}, mas a GPU é projetada para {projeto_completo.Gpu.pcie_version}.")

        # 4. Validação Reversa: Armazenamento (SSD)
        if projeto_completo.Ssd:
            formato_ssd = projeto_completo.Ssd.format.strip().upper()
            interface_ssd = projeto_completo.Ssd.interface.strip().upper()

            if formato_ssd == "M.2" and mb_nova.m2_slots < 1:
                projeto_completo.Compatibility = False
                avisos.append("Incompatível: O SSD escolhido é M.2, mas esta Placa-Mãe não possui slots M.2.")
            
            elif interface_ssd == "SATA" and mb_nova.sata_ports < 1:
                projeto_completo.Compatibility = False
                avisos.append("Incompatível: O SSD escolhido é SATA, mas esta Placa-Mãe não possui portas SATA disponíveis.")

        return {"warnings": avisos}

    def _analisa_Fonte(self, projeto_completo, fonte_nova):
        avisos = []

        # 1. Cálculo de Consumo Energético Coletivo (Watts)
        # Começamos com uma margem base de 100W para alimentar Placa-Mãe, RAM, Ventoinhas e Armazenamento
        consumo_estimado = 100 

        # Se a CPU já estiver no projeto, soma o seu TDP
        if projeto_completo.CPU:
            consumo_estimado += projeto_completo.CPU.CPU_TDP
            
        # Se a GPU já estiver no projeto, soma o seu TGP
        if projeto_completo.GPU:
            consumo_estimado += projeto_completo.GPU.Tgp

        # Validação da Potência Total
        if fonte_nova.pot_watts < consumo_estimado:
            projeto_completo.Compatibility = False
            cpu_watts = projeto_completo.CPU.CPU_TDP if projeto_completo.CPU else 0
            gpu_watts = projeto_completo.GPU.Tgp if projeto_completo.GPU else 0
            avisos.append(
                f"Incompatível: A Fonte oferece {fonte_nova.Pot_Watts}W, mas o consumo estimado "
                f"com margem de segurança é de {consumo_estimado}W (CPU: {cpu_watts}W + GPU: {gpu_watts}W + 100W base)."
            )

        # 2. Validação Reversa de Cabos para a GPU (Se ela já existir no projeto)
        if projeto_completo.Gpu:
            if fonte_nova.pcie_8pin_count < projeto_completo.Gpu.pcie_8pin_count:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A Fonte possui {fonte_nova.pcie_8pin_count} conectores PCIe de 8 pinos, mas a GPU selecionada exige {projeto_completo.Gpu.pcie_8pin_count}.")
                
            if fonte_nova.pcie_6pin_count < projeto_completo.Gpu.pcie_6pin_count:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A Fonte possui {fonte_nova.pcie_6pin_count} conectores PCIe de 6 pinos, mas a GPU selecionada exige {projeto_completo.Gpu.pcie_6pin_count}.")
                
            if fonte_nova.pcie_12vhpwr_count < projeto_completo.Gpu.pcie_12vhpwr_count:
                projeto_completo.Compatibility = False
                avisos.append("Incompatível: A Fonte não possui o conector moderno 12VHPWR exigido pela GPU do projeto.")

        # 3. Validação Reversa de Cabos para o SSD (Se ele já existir e for SATA)
        if projeto_completo.Ssd:
            if projeto_completo.Ssd.interface.strip().upper() == "SATA":
                if fonte_nova.sata_power_count < 1:
                    projeto_completo.Compatibility = False
                    avisos.append("Incompatível: A Fonte não possui conectores de energia SATA disponíveis para alimentar o SSD do projeto.")

        return {"warnings": avisos}

    def _analisa_GPU(self, projeto_completo, gpu_nova):
        avisos = []

        # 1. Dependência da Placa-Mãe (Versão do PCIe)
        if projeto_completo.Mb:
            if gpu_nova.pcie_version != projeto_completo.Mb.pcie_version:
                # O PCIe é retrocompatível, então NÃO muda compativel para False. Apenas gera aviso.
                avisos.append(f"Aviso de Performance: A GPU exige {gpu_nova.pcie_version} mas a Placa-Mãe possui slot {projeto_completo.Mb.pcie_version}. Haverá gargalo de banda.")

        # 2. Dependência da Fonte de Alimentação (Contagem de Cabos Elétricos)
        if projeto_completo.Power:
            # Checagem de conectores de 8 pinos
            if projeto_completo.Power.pcie_8pin_count < gpu_nova.pcie_8pin_count:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A GPU exige {gpu_nova.pcie_8pin_count} cabos PCIe de 8 pinos, mas a Fonte possui apenas {projeto_completo.Power.pcie_8pin_count}.")
            
            # Checagem de conectores de 6 pinos
            if projeto_completo.Power.pcie_6pin_count < gpu_nova.pcie_6pin_count:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A GPU exige {gpu_nova.pcie_6pin_count} cabos PCIe de 6 pinos, mas a Fonte possui apenas {projeto_completo.Power.pcie_6pin_count}.")
            
            # Checagem do conector 12VHPWR (Placas modernas como RTX 4000)
            if projeto_completo.Power.pcie_12vhpwr_count < gpu_nova.pcie_12vhpwr_count:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A GPU exige o conector moderno 12VHPWR, mas a Fonte escolhida não possui esse cabo.")

        return {"warnings": avisos}

    def _analisa_SSD(self, projeto_completo, ssd_novo):
        avisos = []

        # Padronizando as strings para evitar erros de digitação no banco (ex: "m.2" vs "M.2")
        formato_ssd = ssd_novo.format.strip().upper()
        interface_ssd = ssd_novo.interface.strip().upper()

        # 1. Dependência da Placa-Mãe (Slots e Portas)
        if projeto_completo.Mb:
            
            # Se for um SSD M.2 (aquele formato "chiclete" que vai direto na placa)
            if formato_ssd == "M.2":
                if projeto_completo.Mb.m2_slots < 1:
                    projeto_completo.Compatibility = False
                    avisos.append("Incompatível: O SSD escolhido é do formato M.2, mas a Placa-Mãe não possui slots M.2 disponíveis.")
            
            # Se for um SSD SATA (aquele formato de caixinha 2.5")
            elif interface_ssd == "SATA":
                if projeto_completo.Mb.sata_ports < 1:
                    projeto_completo.Compatibility = False
                    avisos.append("Incompatível: O SSD utiliza interface SATA, mas a Placa-Mãe não possui portas SATA disponíveis.")

        # 2. Dependência da Fonte de Alimentação (Energia)
        if projeto_completo.Power:
            
            # Apenas SSDs SATA precisam de cabo de energia da fonte (M.2 puxa energia direto da placa-mãe)
            if interface_ssd == "SATA":
                if projeto_completo.Power.sata_power_count < 1:
                    projeto_completo.Compatibility = False
                    avisos.append("Incompatível: O SSD SATA requer um cabo de energia, mas a Fonte escolhida não possui conectores SATA disponíveis.")

        return {"warnings": avisos}

    def _analisa_RAM(self, projeto_completo, ram_nova):
        avisos = []


        if projeto_completo.Mb:
            # Nota: Usamos .lower() ou tratamento direto dependendo de como os dados vêm do banco (ex: DDR4 vs ddr4)
            if ram_nova.ram_type.strip().upper() != projeto_completo.Mb.ram_type.strip().upper():
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: A memória escolhida é {ram_nova.ram_type}, mas a Placa-Mãe suporta apenas slots {projeto_completo.Mb.ram_type}.")

            # 2. Restrição de Capacidade Máxima (GB)
            if ram_nova.capacity > projeto_completo.Mb.ram_max_cap:
                projeto_completo.Compatibility = False
                avisos.append(f"Incompatível: O módulo de RAM possui {ram_nova.capacity}GB, ultrapassando o limite máximo de {projeto_completo.Mb.ram_max_cap}GB suportado por esta Placa-Mãe.")

            # 3. Restrição de Velocidade/Frequência (MHz)
            if ram_nova.velocity > projeto_completo.Mb.ram_max_vel:
                # O PC funciona! Portanto, NÃO mudamos 'compativel' para False. Apenas alertamos o usuário.
                avisos.append(f"Aviso de Otimização: A RAM opera a {ram_nova.velocity}MHz, mas a Placa-Mãe limita a velocidade em até {projeto_completo.Mb.ram_max_vel}MHz. A memória sofrerá sobrefrequência reduzida (underclock) automática.")

        return {"warnings": avisos}