class project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        def __str__(self):
            return f"Title:{self.title}, Description:{self.description}, Due_Date:{self.due_date}"
        