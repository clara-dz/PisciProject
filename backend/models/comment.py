class Comment:
    def __init__(self, User_ID, Component_ID, Comment, Component_TYPE):
        self.User_ID = User_ID
        self.Component_ID = Component_ID
        self.Component_TYPE = Component_TYPE
        self.Comment = Comment
    def __repr__(self):
        return f"<Comment {self.Username} ({self.Comment})>"