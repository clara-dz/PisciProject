class Power:
    def __init__(self, POWER_ID, Name, Manufacturer, Pot_Watts, Efficiency, Modular, Cpu_8pin_Count, Pcie_8pin_Count, Pcie_12vhpwr_Count, sata_power_count, Pcie_6pin_Count):
        self.POWER_ID = POWER_ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Pot_Watts = Pot_Watts
        self.Efficiency  = Efficiency
        self.Modular = Modular
        self.Cpu_8pin_Count = Cpu_8pin_Count
        self.Pcie_8pin_Count = Pcie_8pin_Count
        self.Pcie_12vhpwr_Count = Pcie_12vhpwr_Count
        self.sata_power_count = sata_power_count
        self.Pcie_6pin_Count = Pcie_6pin_Count
    def __repr__(self):
        return f"<Power {self.Name} ({self.Pot_Watts})>"