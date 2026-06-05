class CPU:
    def __init__(self, CPU_ID, Name, Manufacturer, CPU_Socket, CPU_TDP, Have_GPU):
        self.CPU_ID = CPU_ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.CPU_Socket = CPU_Socket
        self.CPU_TDP = CPU_TDP
        self.Have_GPU = Have_GPU

    def __repr__(self):
        return f"<CPU {self.Name} ({self.Socket})>"