class Task:
    def __init__(self, title, assigned_to, status="Pending"):
        self.title = title
        self.assigned_to = assigned_to
        self.status = status

    def complete(self):
         self.status ="Completed"

    def to_dict(self):
            return {
                  "title":self.title,
                  "assigned_to":self.assigned_to,
                  "status":self.status
            }

    def __str__(self):
            return f"Title:{self.title}, Assigned_To: {self.assigned_to}, Status: {self.status}"


        