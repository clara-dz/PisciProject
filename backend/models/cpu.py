class CPU:
    def __init__(self, ID, Name, Manufacturer, Socket, Tdp, Have_Integrated_GPU):
        self.id = ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Socket = Socket
        self.Tdp = Tdp
        self.Have_Integrated_GPU = Have_Integrated_GPU

    def __repr__(self):
        return f"<CPU {self.Name} ({self.Socket})>"