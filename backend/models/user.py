class User:
    def __init__(self, User_ID, Name, Email, Password, ProjectNumber):
        self.User_ID = User_ID
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.ProjectNumber = ProjectNumber
    def __repr__(self):
        return f"<User {self.Name} ({self.Email})>"