from services.compatibilityservice import CompatibilityService
from database.repository import ComponentRepository
from models.cpu import CPU
from models.gpu import GPU
from models.motherboard import MotherBoard
from models.power import Power
from models.project import Project
from models.ram import MEM_RAM
from models.ssd import SSD

class ProjectService:
    def __init__(self):
        self.comp_service = CompatibilityService()
        self.repository = ComponentRepository()

    def start_new_project(self, flask_session): #-------------------------------------------------------------------------------------------
        """
        Zera qualquer projeto anterior da sessão e inicia um rascunho limpo.
        """
        flask_session['novo_projeto'] = {
            'MotherBoard': None, 'CPU': None, 'GPU': None, 
            'MEM_RAM': None, 'SSD': None, 'Power': None
        }
        
        # Avisa o Flask para gravar essa mudança no cookie do usuário
        flask_session.modified = True 
        
        return {
            "sucesso": True,
            "projeto": flask_session['novo_projeto']
        }

    def add_component(self, component_id, tipo, flask_session): # ------------------------------------------------------------------------

        if 'novo_projeto' not in flask_session:
            flask_session['novo_projeto'] = {
                'MotherBoard': None, 'CPU': None, 'GPU': None, 
                'MEM_RAM': None, 'SSD': None, 'Power': None
            }
        
        projeto_atual_dict = flask_session['novo_projeto']
        projeto_atual_dict[tipo] = component_id
        
        flask_session['novo_projeto'] = projeto_atual_dict
        flask_session.modified = True

        projeto_objeto, novo_componente_obj = self._montar_objeto_projeto(
            projeto_atual_dict, 
            flask_session.get('user_id'), 
            tipo
        )

        # 3. Envia para análise de compatibilidade
        relatorio = self.comp_service.check_compatibility(projeto_objeto, novo_componente_obj, tipo)
        
        return {
            "sucesso": True, 
            "projeto": projeto_atual_dict, 
            "compatibilidade": relatorio
        }

    # ========================================================================
    # FUNÇÃO DE APOIO (Privada)
    # ========================================================================
def _montar_objeto_projeto(self, projeto_dict, user_id, tipo_adicionado):
        
        cpu_obj, mb_obj, gpu_obj = None, None, None
        ram_obj, ssd_obj, power_obj = None, None, None

        if projeto_dict.get('CPU'):
            dados = self.repository.buscar_cpu(projeto_dict['CPU'])
            if dados: 
                cpu_obj = CPU(
                    id=dados['CPU_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    socket=dados['CPU_Socket'], 
                    tdp=dados['CPU_TDP'], 
                    have_gpu=dados['Have_GPU']
                )

        if projeto_dict.get('MotherBoard'):
            dados = self.repository.buscar_placa_mae(projeto_dict['MotherBoard'])
            if dados: 
                mb_obj = MotherBoard(
                    id=dados['MB_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    socket=dados['MB_Socket'], 
                    chipset=dados['Chipset'], 
                    form_factor=dados['form_factor'], 
                    dimensions=dados['dimensions_mm'], 
                    slots_ram=dados['Slots_Ram'], 
                    ram_type=dados['Ram_type'], 
                    ram_max_vel=dados['Ram_max_vel'], 
                    ram_max_cap=dados['Ram_max_cap'], 
                    pcie_version=dados['Pcie_Version'], 
                    pcie_x16_slots=dados['Pcie_x16_slots'], 
                    m2_slots=dados['m2_slots'], 
                    m2_pcie_version=dados['m2_pcie_version'], 
                    sata_ports=dados['Sata_ports']
                )

        if projeto_dict.get('GPU'):
            dados = self.repository.buscar_gpu(projeto_dict['GPU'])
            if dados:
                gpu_obj = GPU(
                    id=dados['GPU_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    pcie_version=dados['Pcie_version'], 
                    pcie_lanes=dados['Pcie_lanes'], 
                    tgp=dados['Tgp'], 
                    length=dados['Length_mm'], 
                    occupied_slots=dados['Ocupated_slots'], 
                    pcie_8pin=dados['Pcie_8pin_Count'], 
                    pcie_6pin=dados['Pcie_6pin_Count'], 
                    pcie_12vhpwr=dados['Pcie_12vhpwr_Count']
                )

        if projeto_dict.get('MEM_RAM'):
            dados = self.repository.buscar_ram(projeto_dict['MEM_RAM'])
            if dados:
                ram_obj = MEM_RAM(
                    id=dados['MEM_RAM_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    ram_type=dados['RAM_type'], 
                    velocity=dados['Velocity'], 
                    capacity=dados['Capacity'], 
                    cas_latency=dados['Cas_Latency']
                )

        if projeto_dict.get('SSD'):
            dados = self.repository.buscar_ssd(projeto_dict['SSD'])
            if dados:
                ssd_obj = SSD(
                    id=dados['SSD_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    interface=dados['Interface'], 
                    format_type=dados['Format'], 
                    capacity=dados['Capacity']
                )

        if projeto_dict.get('Power'):
            dados = self.repository.buscar_fonte(projeto_dict['Power'])
            if dados:
                power_obj = Power(
                    id=dados['POWER_ID'], 
                    name=dados['Name'], 
                    manufacturer=dados['Manufacturer'], 
                    watts=dados['Pot_Watts'], 
                    efficiency=dados['Efficiency'], 
                    modular=dados['Modular'], 
                    cpu_8pin=dados['Cpu_8pin_Count'], 
                    pcie_8pin=dados['Pcie_8pin_Count'], 
                    pcie_6pin=dados['Pcie_6pin_Count'], 
                    pcie_12vhpwr=dados['Pcie_12vhpwr_Count'], 
                    sata_power=dados['sata_power_count']
                )

        projeto_principal = Project(
            ID=None, 
            User_id=user_id, 
            Project_Name="Rascunho", 
            Description="Projeto em andamento",
            Mb=mb_obj,     
            CPU=cpu_obj,   
            GPU=gpu_obj, 
            MEM_RAM=ram_obj, 
            SSD=ssd_obj, 
            Fonte=power_obj, 
            Compatibility=None
        )

        # 4. Descobre qual foi a peça que acabou de ser adicionada (para o Padrão de Delegação)
        componente_destaque = None
        if tipo_adicionado == 'CPU': componente_destaque = cpu_obj
        elif tipo_adicionado == 'MotherBoard': componente_destaque = mb_obj
        elif tipo_adicionado == 'GPU': componente_destaque = gpu_obj
        elif tipo_adicionado == 'MEM_RAM': componente_destaque = ram_obj
        elif tipo_adicionado == 'SSD': componente_destaque = ssd_obj
        elif tipo_adicionado == 'Power': componente_destaque = power_obj

        # Retorna o projeto completo E o componente isolado para análise técnica
        return projeto_principal, componente_destaque