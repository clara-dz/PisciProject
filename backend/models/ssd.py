class SSD:
    def __init__(self, ID, Name, Manufacturer, Interface, Format, Capacity):
        self.ID = ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Interface = Interface
        self.Format = Format
        self.Capacity = Capacity
    def __repr__(self):
        return f"<SSD {self.Name} ({self.Capacity})>"