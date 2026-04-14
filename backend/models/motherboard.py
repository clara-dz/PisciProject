class MotherBoard:
    def __init__(self, ID, Name, Manufacturer, Socket, Chipset, form_factor, dimensions_mm, Slots_Ram, Ram_type, Ram_max_vel, Ram_max_cap, Pcie_version, Pcie_x16_slots, m2_slots, M2_pcie_version, Sata_ports):
        self.ID = ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Socket = Socket
        self.Chipset = Chipset
        self.form_factor = form_factor
        self.dimensions_mm = dimensions_mm
        self.Slots_Ram = Slots_Ram
        self.Ram_type = Ram_type
        self.Ram_max_vel = Ram_max_vel
        self.Ram_max_cap = Ram_max_cap
        self.Pcie_version = Pcie_version
        self.Pcie_x16_slots = Pcie_x16_slots
        self.m2_slots = m2_slots
        self.M2_pcie_version = M2_pcie_version
        self.Sata_ports = Sata_ports
    def __repr__(self):
        return f"<MotherBoard {self.Name} ({self.Manufacturer})>"