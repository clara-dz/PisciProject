from decimal import Decimal
from datetime import date, datetime
from database.repository import ComponentRepository


class ProjectService:
    """Serviço responsável pelo rascunho do projeto salvo na sessão Flask."""

    SLOT_KEYS = {
        "CPU": "CPU",
        "GPU": "GPU",
        "MOTHERBOARD": "MotherBoard",
        "PLACA_MAE": "MotherBoard",
        "PLACA-MAE": "MotherBoard",
        "RAM": "MEM_RAM",
        "MEM_RAM": "MEM_RAM",
        "MEMORIA_RAM": "MEM_RAM",
        "SSD": "SSD",
        "ARMAZENAMENTO": "SSD",
        "POWER": "Power",
        "FONTE": "Power",
        "Power": "Power",
        "MotherBoard": "MotherBoard",
    }

    EMPTY_PROJECT = {
        "MotherBoard": None,
        "CPU": None,
        "GPU": None,
        "MEM_RAM": None,
        "SSD": None,
        "Power": None,
        "Compatibility": True,
    }

    def __init__(self):
        self.repository = ComponentRepository()

    def _normalize_tipo(self, tipo):
        if not tipo:
            return None
        return self.SLOT_KEYS.get(str(tipo).upper()) or self.SLOT_KEYS.get(str(tipo))

    def _ensure_project(self, flask_session):
        if "novo_projeto" not in flask_session:
            self.start_new_project(flask_session)
        return flask_session["novo_projeto"]

    def start_new_project(self, flask_session):
        flask_session["novo_projeto"] = self.EMPTY_PROJECT.copy()
        flask_session["project_id"] = None
        flask_session["project_name"] = "Rascunho Novo"
        flask_session["project_description"] = ""
        flask_session.modified = True

        return {
            "sucesso": True,
            "projeto": flask_session["novo_projeto"],
            "detalhes": self.get_current_project(flask_session)["detalhes"],
        }

    def add_component(self, component_id, tipo, flask_session):
        slot = self._normalize_tipo(tipo)
        if not slot:
            return {"sucesso": False, "mensagem": f"Tipo de componente inválido: {tipo}"}

        projeto = self._ensure_project(flask_session)

        try:
            component_id = int(component_id)
        except (TypeError, ValueError):
            return {"sucesso": False, "mensagem": "ID do componente inválido."}

        if projeto.get(slot) is not None:
            return {
                "sucesso": False,
                "mensagem": f"O projeto já possui um componente no slot {slot}. Remova o atual antes de adicionar outro.",
                "projeto": projeto,
                "compatibilidade": self._check_compatibility(projeto),
                "detalhes": self._get_project_details(projeto),
            }

        projeto[slot] = component_id
        relatorio = self._check_compatibility(projeto)
        projeto["Compatibility"] = relatorio["is_compatible"]

        flask_session["novo_projeto"] = projeto
        flask_session.modified = True

        return {
            "sucesso": True,
            "projeto": projeto,
            "compatibilidade": relatorio,
            "detalhes": self._get_project_details(projeto),
        }

    def remove_component(self, tipo, flask_session):
        if "novo_projeto" not in flask_session:
            return {"sucesso": False, "mensagem": "Nenhum projeto ativo."}

        slot = self._normalize_tipo(tipo)
        if not slot:
            return {"sucesso": False, "mensagem": f"Tipo de componente inválido: {tipo}"}

        projeto = flask_session["novo_projeto"]
        projeto[slot] = None

        relatorio = self._check_compatibility(projeto)
        projeto["Compatibility"] = relatorio["is_compatible"]

        flask_session["novo_projeto"] = projeto
        flask_session.modified = True

        return {
            "sucesso": True,
            "projeto": projeto,
            "compatibilidade": relatorio,
            "detalhes": self._get_project_details(projeto),
        }

    def save_project(self, flask_session, project_name, description):
        user_id = flask_session.get("user_id")
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado. Faça login para salvar."}

        projeto = flask_session.get("novo_projeto")
        if not projeto:
            return {"sucesso": False, "mensagem": "Nenhum projeto ativo para salvar."}

        if not any(projeto.get(slot) for slot in ["CPU", "GPU", "MotherBoard", "SSD", "MEM_RAM", "Power"]):
            return {"sucesso": False, "mensagem": "Um projeto vazio não pode ser salvo."}

        project_name = project_name or flask_session.get("project_name") or "Projeto sem nome"
        description = description or ""

        relatorio = self._check_compatibility(projeto)
        projeto["Compatibility"] = relatorio["is_compatible"]

        project_id = flask_session.get("project_id")

        if project_id:
            self.repository.update_project(
                project_id=project_id,
                name=project_name,
                description=description,
                cpu_id=projeto.get("CPU"),
                mb_id=projeto.get("MotherBoard"),
                gpu_id=projeto.get("GPU"),
                ram_id=projeto.get("MEM_RAM"),
                ssd_id=projeto.get("SSD"),
                power_id=projeto.get("Power"),
                compatibility=projeto.get("Compatibility"),
            )
            mensagem = "Projeto atualizado com sucesso!"
        else:
            novo_id = self.repository.insert_project(
                user_id=user_id,
                name=project_name,
                description=description,
                cpu_id=projeto.get("CPU"),
                mb_id=projeto.get("MotherBoard"),
                gpu_id=projeto.get("GPU"),
                ram_id=projeto.get("MEM_RAM"),
                ssd_id=projeto.get("SSD"),
                power_id=projeto.get("Power"),
                compatibility=projeto.get("Compatibility"),
            )
            flask_session["project_id"] = novo_id
            mensagem = "Novo projeto salvo com sucesso!"

        flask_session["project_name"] = project_name
        flask_session["project_description"] = description
        flask_session["novo_projeto"] = projeto
        flask_session.modified = True

        return {"sucesso": True, "mensagem": mensagem, "project_id": flask_session["project_id"]}

    def load_project(self, project_id, flask_session):
        user_id = flask_session.get("user_id")
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado."}

        projeto_db = self.repository.buscar_projeto(project_id, user_id)
        if not projeto_db:
            return {"sucesso": False, "mensagem": "Projeto não encontrado ou sem permissão."}

        flask_session["project_id"] = projeto_db["ID"]
        flask_session["project_name"] = projeto_db["Project_Name"]
        flask_session["project_description"] = projeto_db["Description"]
        flask_session["novo_projeto"] = {
            "CPU": projeto_db["CPU_ID"],
            "MotherBoard": projeto_db["MB_ID"],
            "GPU": projeto_db["GPU_ID"],
            "MEM_RAM": projeto_db["MEM_RAM_ID"],
            "SSD": projeto_db["SSD_ID"],
            "Power": projeto_db["POWER_ID"],
            "Compatibility": bool(projeto_db["Compatibility"]),
        }
        flask_session.modified = True

        return {
            "sucesso": True,
            "mensagem": "Projeto carregado com sucesso!",
            "projeto": flask_session["novo_projeto"],
            "detalhes": self._get_project_details(flask_session["novo_projeto"]),
            "compatibilidade": self._check_compatibility(flask_session["novo_projeto"]),
        }

    def get_user_projects(self, flask_session):
        user_id = flask_session.get("user_id")
        if not user_id:
            return {"sucesso": False, "mensagem": "Usuário não autenticado."}

        projetos_db = self.repository.listar_projetos_usuario(user_id)
        projetos_formatados = []

        for proj in projetos_db:
            projetos_formatados.append({
                "id": proj["ID"],
                "name": proj["Project_Name"],
                "description": proj["Description"],
                "is_compatible": bool(proj["Compatibility"]),
            })

        return {"sucesso": True, "projetos": projetos_formatados}

    def get_current_project(self, flask_session):
        projeto = self._ensure_project(flask_session)
        relatorio = self._check_compatibility(projeto)
        projeto["Compatibility"] = relatorio["is_compatible"]
        flask_session["novo_projeto"] = projeto
        flask_session.modified = True

        return {
            "sucesso": True,
            "projeto": projeto,
            "detalhes": self._get_project_details(projeto),
            "compatibilidade": relatorio,
            "project_id": flask_session.get("project_id"),
            "project_name": flask_session.get("project_name", "Rascunho Novo"),
            "project_description": flask_session.get("project_description", ""),
        }

    def _get_project_details(self, projeto):
        return {
            "CPU": self._compact(self.repository.buscar_cpu(projeto.get("CPU"))) if projeto.get("CPU") is not None else None,
            "MotherBoard": self._compact(self.repository.buscar_placa_mae(projeto.get("MotherBoard"))) if projeto.get("MotherBoard") is not None else None,
            "GPU": self._compact(self.repository.buscar_gpu(projeto.get("GPU"))) if projeto.get("GPU") is not None else None,
            "MEM_RAM": self._compact(self.repository.buscar_ram(projeto.get("MEM_RAM"))) if projeto.get("MEM_RAM") is not None else None,
            "SSD": self._compact(self.repository.buscar_ssd(projeto.get("SSD"))) if projeto.get("SSD") is not None else None,
            "Power": self._compact(self.repository.buscar_fonte(projeto.get("Power"))) if projeto.get("Power") is not None else None,
        }

    def _json_safe_value(self, valor):
        """Converte valores vindos do MySQL para tipos aceitos pelo jsonify/session."""
        if isinstance(valor, Decimal):
            return float(valor)
        if isinstance(valor, (date, datetime)):
            return valor.isoformat()
        if isinstance(valor, bytes):
            return valor.decode("utf-8", errors="ignore")
        if isinstance(valor, dict):
            return {chave: self._json_safe_value(item) for chave, item in valor.items()}
        if isinstance(valor, (list, tuple)):
            return [self._json_safe_value(item) for item in valor]
        return valor

    def _compact(self, dados):
        if not dados:
            return None

        dados = dict(dados)
        dados.pop("Image_Data", None)

        return {
            chave: self._json_safe_value(valor)
            for chave, valor in dados.items()
        }
    
    def discard_current_project(self, flask_session):
        flask_session.pop("novo_projeto", None)
        flask_session.pop("project_id", None)
        flask_session.pop("project_name", None)
        flask_session.pop("project_description", None)
        flask_session.modified = True

        return {
            "sucesso": True,
            "mensagem": "Rascunho do projeto descartado."
        }

    def _check_compatibility(self, projeto):
        warnings = []
        is_compatible = True

        cpu = self.repository.buscar_cpu(projeto.get("CPU")) if projeto.get("CPU") is not None else None
        mb = self.repository.buscar_placa_mae(projeto.get("MotherBoard")) if projeto.get("MotherBoard") is not None else None
        gpu = self.repository.buscar_gpu(projeto.get("GPU")) if projeto.get("GPU") is not None else None
        ram = self.repository.buscar_ram(projeto.get("MEM_RAM")) if projeto.get("MEM_RAM") is not None else None
        ssd = self.repository.buscar_ssd(projeto.get("SSD")) if projeto.get("SSD") is not None else None
        power = self.repository.buscar_fonte(projeto.get("Power")) if projeto.get("Power") is not None else None

        if cpu and mb and cpu.get("CPU_Socket") != mb.get("MB_Socket"):
            is_compatible = False
            warnings.append(f"CPU e placa-mãe incompatíveis: CPU usa soquete {cpu.get('CPU_Socket')} e placa-mãe usa {mb.get('MB_Socket')}.")

        if cpu and not gpu and not bool(cpu.get("Have_GPU")):
            is_compatible = False
            warnings.append("A CPU escolhida não possui vídeo integrado e o projeto ainda não tem GPU dedicada.")

        if ram and mb:
            if str(ram.get("RAM_type", "")).upper() != str(mb.get("Ram_type", "")).upper():
                is_compatible = False
                warnings.append(f"RAM incompatível: memória é {ram.get('RAM_type')} e placa-mãe suporta {mb.get('Ram_type')}.")
            if ram.get("Capacity") and mb.get("Ram_max_cap") and ram["Capacity"] > mb["Ram_max_cap"]:
                is_compatible = False
                warnings.append(f"RAM ultrapassa a capacidade máxima da placa-mãe: {ram['Capacity']}GB > {mb['Ram_max_cap']}GB.")
            if ram.get("Velocity") and mb.get("Ram_max_vel") and ram["Velocity"] > mb["Ram_max_vel"]:
                warnings.append(f"A RAM funciona, mas será limitada a {mb['Ram_max_vel']}MHz pela placa-mãe.")

        if ssd and mb:
            formato = str(ssd.get("Format", "")).upper()
            interface = str(ssd.get("Interface", "")).upper()
            if formato == "M.2" and (mb.get("m2_slots") or 0) < 1:
                is_compatible = False
                warnings.append("SSD M.2 incompatível: placa-mãe não possui slot M.2.")
            if interface == "SATA" and (mb.get("Sata_ports") or 0) < 1:
                is_compatible = False
                warnings.append("SSD SATA incompatível: placa-mãe não possui portas SATA disponíveis.")

        if power:
            consumo = 100
            if cpu:
                consumo += cpu.get("CPU_TDP") or 0
            if gpu:
                consumo += gpu.get("Tgp") or 0
            if power.get("Pot_Watts") and power["Pot_Watts"] < consumo:
                is_compatible = False
                warnings.append(f"Fonte fraca: oferece {power['Pot_Watts']}W, mas o consumo estimado é {consumo}W.")

            if gpu:
                for campo, nome in [
                    ("Pcie_8pin_Count", "PCIe 8 pinos"),
                    ("Pcie_6pin_Count", "PCIe 6 pinos"),
                    ("Pcie_12vhpwr_Count", "12VHPWR"),
                ]:
                    if (power.get(campo) or 0) < (gpu.get(campo) or 0):
                        is_compatible = False
                        warnings.append(f"Fonte incompatível: conectores {nome} insuficientes para a GPU.")

            if ssd and str(ssd.get("Interface", "")).upper() == "SATA" and (power.get("sata_power_count") or 0) < 1:
                is_compatible = False
                warnings.append("Fonte incompatível: não possui conector de energia SATA para o SSD.")

        return {"is_compatible": is_compatible, "warnings": warnings}
