class person:
    def __init__(self,name,email):
        self.name = name
        self.email = email
        def __str__(self):
            return f"Name: {self.name}, Email:{self.email}"

class user(person):
    def __init__(self,name,email):
         super().__init__(name,email)
         self.projects = []


    def add_projects(self,projects):
        self.projects.append(projects)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "projects": [projects.to_dict()for projects in self.projects]

        }
    def __str__(self):
     return f"Name: {self.name}, Email:{self.email}, Projects: {len(self.projects)}"



                