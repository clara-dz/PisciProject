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
            'MEM_RAM': None, 'SSD': None, 'Power': None, 'Compatibility': True
        }
        
        flask_session['project_id'] = None
        flask_session['project_name'] = "Rascunho Novo"
        flask_session['project_description'] = ""

        # Avisa o Flask para gravar essa mudança no cookie do usuário
        flask_session.modified = True 
        
        return {
            "sucesso": True,
            "projeto": flask_session['novo_projeto']
        }

    def add_component(self, component_id, tipo, flask_session): # ------------------------------------------------------------------------

        # REGRAS DE NEGOCIO BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        
        if projeto_atual_dict[tipo]:
            return {"sucesso": True, "message": "Esse tipo de componente já existe no projeto"}
        
        # BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

        if 'novo_projeto' not in flask_session:
            self.start_new_project(flask_session)
        
        projeto_atual_dict = flask_session['novo_projeto']
        projeto_atual_dict[tipo] = component_id

        projeto_objeto= self._montar_objeto_projeto(projeto_atual_dict, flask_session)

        relatorio = self.comp_service.check_compatibility(projeto_objeto)

        projeto_atual_dict['Compatibility'] = projeto_objeto.Compatibility

        flask_session['novo_projeto'] = projeto_atual_dict
        flask_session.modified = True
        
        return {
            "sucesso": True, 
            "projeto": projeto_atual_dict, 
            "compatibilidade": relatorio
        }
    
    def remove_component(self, tipo, flask_session): # ----------------------------------------------------------------------------------

        if 'novo_projeto' not in flask_session:
            return {"sucesso": False, "mensagem": "Nenhum projeto ativo."}
            
        projeto_atual_dict = flask_session['novo_projeto']
        projeto_atual_dict[tipo] = None
        
        projeto_objeto = self._montar_objeto_projeto(projeto_atual_dict, flask_session)
        relatorio = self.comp_service.check_compatibility(projeto_objeto)
        
        projeto_atual_dict['Compatibility'] = projeto_objeto.Compatibility
        
        flask_session['novo_projeto'] = projeto_atual_dict
        flask_session.modified = True
        
        return {
            "sucesso": True,
            "projeto": projeto_atual_dict,
            "compatibilidade": relatorio
        }
    
    def save_project(self, flask_session, project_name, description): # -----------------------------------------------------------------
        """Executa a lógica de Upsert (Insert ou Update)."""

        user_id = flask_session.get('user_id')
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado. Faça login para salvar."}

        projeto_dict = flask_session.get('novo_projeto')
        if not projeto_dict:
            return {"sucesso": False, "mensagem": "Nenhum projeto ativo para salvar."}
        
        if not projeto_dict['CPU'] and not projeto_dict['GPU'] and not projeto_dict['MotherBoard'] and not projeto_dict['SSD'] and not projeto_dict['MEM_RAM'] and not projeto_dict['Power']:
            return {"sucesso": False, "mensagem": "Um projeto vazio não pode ser salvo"}

        project_id = flask_session.get('project_id') 

        if project_id:
            # Já existe: UPDATE
            self.repository.update_project(
                project_id=project_id,
                name=project_name,
                description=description,
                cpu_id=projeto_dict.get('CPU'),
                mb_id=projeto_dict.get('MotherBoard'),
                gpu_id=projeto_dict.get('GPU'),
                ram_id=projeto_dict.get('MEM_RAM'),
                ssd_id=projeto_dict.get('SSD'),
                power_id=projeto_dict.get('Power'),
                compatibility=projeto_dict.get('Compatibility')
            )
            mensagem = "Projeto atualizado com sucesso!"
        else:
            # É novo: INSERT
            novo_id = self.repository.insert_project(
                user_id=user_id,
                name=project_name,
                description=description,
                cpu_id=projeto_dict.get('CPU'),
                mb_id=projeto_dict.get('MotherBoard'),
                gpu_id=projeto_dict.get('GPU'),
                ram_id=projeto_dict.get('MEM_RAM'),
                ssd_id=projeto_dict.get('SSD'),
                power_id=projeto_dict.get('Power'),
                compatibility=projeto_dict.get('Compatibility')
            )
            flask_session['project_id'] = novo_id
            mensagem = "Novo projeto salvo com sucesso!"

        flask_session['project_name'] = project_name
        flask_session['project_description'] = description
        flask_session.modified = True

        return {"sucesso": True, "mensagem": mensagem, "project_id": flask_session['project_id']}

    def load_project(self, project_id, flask_session):
        """Carrega um projeto do banco de dados e o coloca na sessão atual."""
        user_id = flask_session.get('user_id')
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado."}

        projeto_db = self.repository.buscar_projeto(project_id, user_id)
        
        if not projeto_db:
            return {"sucesso": False, "mensagem": "Projeto não encontrado ou você não tem permissão para acessá-lo."}

        flask_session['project_id'] = projeto_db['ID']
        flask_session['project_name'] = projeto_db['Project_Name']
        flask_session['project_description'] = projeto_db['Description']
        
        flask_session['novo_projeto'] = {
            'CPU': projeto_db['CPU_ID'],
            'MotherBoard': projeto_db['MB_ID'],
            'GPU': projeto_db['GPU_ID'],
            'MEM_RAM': projeto_db['MEM_RAM_ID'],
            'SSD': projeto_db['SSD_ID'],
            'Power': projeto_db['POWER_ID'],
            # Converte o tinyint do MySQL de volta para booleano no Python
            'Compatibility': bool(projeto_db['Compatibility']) 
        }
        
        flask_session.modified = True

        return {
            "sucesso": True, 
            "mensagem": "Projeto carregado com sucesso!", 
            "projeto": flask_session['novo_projeto']
        }

    def get_user_projects(self, flask_session):

        user_id = flask_session.get('user_id')
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado."}

        projetos_db = self.repository.listar_projetos_usuario(user_id)
        
        projetos_formatados = []
        for proj in projetos_db:
            projetos_formatados.append({
                "id": proj["ID"],
                "name": proj["Project_Name"],
                "description": proj["Description"],
                "is_compatible": bool(proj["Compatibility"])
            })

        return {
            "sucesso": True, 
            "projetos": projetos_formatados
        }

    # ========================================================================
    # FUNÇÃO DE APOIO (Privada)
    # ========================================================================
    def _montar_objeto_projeto(self, projeto_dict,flask_session):
        
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
            ID=flask_session.get('project_id'), 
            User_id=flask_session.get('user_id'), 
            Project_Name=flask_session.get('project_name', 'Rascunho'), 
            Description=flask_session.get('project_description', ''),
            Mb=mb_obj,     
            CPU=cpu_obj,   
            GPU=gpu_obj, 
            MEM_RAM=ram_obj, 
            SSD=ssd_obj, 
            Power=power_obj, 
            Compatibility=projeto_dict.get('Compatibility', True)
        )

        return projeto_principal