class Project:
    def __init__(self, ID, User_id, Project_Name, Description, Mb, CPU, GPU, MEM_RAM, SSD, Fonte, Compatibility):
        self.ID = ID
        self.User_id = User_id
        self.Project_Name = Project_Name
        self.Description = Description
        self.Mb = Mb
        self.CPU = CPU
        self.GPU = GPU
        self.MEM_RAM = MEM_RAM
        self.SSD = SSD
        self.Fonte = Fonte
        self.Compatibility = Compatibility

    def to_dict(self):
        """Transforma o objeto em dicionário para ser enviado como JSON"""
        return {
            "user_id": self.User_id,
            "components": {
                "cpu": self.CPU,
                "motherboard": self.Mb,
                "ram": self.MEM_RAM
            }
        }
    def __repr__(self):
        return f"<Project {self.User_id} ({self.Project_Name})>"