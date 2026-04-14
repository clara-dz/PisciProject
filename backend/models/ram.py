class RAM:
    def __init__(self, ID, Name, Manufacturer, Type, Velocity, Capacity, Cas_Latency):
        self.ID = ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Type = Type
        self.Velocity = Velocity
        self.Capacity = Capacity
        self.Cas_Latency = Cas_Latency
    def __repr__(self):
        return f"<RAM {self.Manufacturer} ({self.Velocity})>"