class MEM_RAM:
    def __init__(self, MEM_RAM_ID, Name, Manufacturer, RAM_Type, Velocity, Capacity, Cas_Latency):
        self.MEM_RAM_ID = MEM_RAM_ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.RAM_Type = RAM_Type
        self.Velocity = Velocity
        self.Capacity = Capacity
        self.Cas_Latency = Cas_Latency
    def __repr__(self):
        return f"<RAM {self.Manufacturer} ({self.Velocity})>"