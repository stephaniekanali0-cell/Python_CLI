class person:
    def __init__(self,name,email):
        self.name = name
        self.email = email
        def __str__(self):
            return f"Name: {self.name}, Email:{self.email}"

        class user(person):
            def __init__(self,name,email):
                super().__init__(name,email)
                def __str__(self):
                    return f"Name: {self.name}, Email:{self.email}"



                