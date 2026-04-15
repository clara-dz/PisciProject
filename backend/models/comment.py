class Comment:
    def __init__(self, Username, Component_name, Comment):
        self.Username = Username
        self.Component_name = Component_name
        self.Comment = Comment
    def __repr__(self):
        return f"<Comment {self.Username} ({self.Comment})>"