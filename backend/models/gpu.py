class GPU:
    def __init__(self, GPU_ID, Name, Manufacturer, Pcie_version, Pcie_lanes, Tgp, Pcie_8pin_Count, Lenght_mm, Ocupated_slots, Pcie_6pin_Count, Pcie_12vhpwr_Count):
        self.GPU_ID = GPU_ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Pcie_version = Pcie_version
        self.Pcie_lanes = Pcie_lanes
        self.Tgp = Tgp
        self.Lenght_mm = Lenght_mm
        self.Ocupated_slots = Ocupated_slots
        self.Pcie_8pin_Count = Pcie_8pin_Count
        self.Pcie_6pin_Count = Pcie_6pin_Count
        self.Pcie_12vhpwr_Count = Pcie_12vhpwr_Count
    def __repr__(self):
        return f"<GPU {self.Manufacturer} ({self.Name})>"
