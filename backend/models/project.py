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
    def __repr__(self):
        return f"<Project {self.User_id} ({self.Project_Name})>"