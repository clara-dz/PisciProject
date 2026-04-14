class GPU:
    def __init__(self, ID, Name, Manufacturer, Pcie_version, Pcie_lanes, Tgp, Power_Connectors, Lenght_mm, Ocupated_slots):
        self.ID = ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Pcie_version = Pcie_version
        self.Pcie_lanes = Pcie_lanes
        self.Tgp = Tgp
        self.Power_Connectors = Power_Connectors
        self.Lenght_mm = Lenght_mm
        self.Ocupated_slots = Ocupated_slots
    def __repr__(self):
        return f"<GPU {self.Manufacturer} ({self.Name})>"
