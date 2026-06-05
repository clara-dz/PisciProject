class SSD:
    def __init__(self, SSD_ID, Name, Manufacturer, Interface, Format, Capacity):
        self.SSD_ID = SSD_ID
        self.Name = Name
        self.Manufacturer = Manufacturer
        self.Interface = Interface
        self.Format = Format
        self.Capacity = Capacity
    def __repr__(self):
        return f"<SSD {self.Name} ({self.Capacity})>"