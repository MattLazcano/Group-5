# Main function library

class LibraryClass:
    def __init__(self):
        self.catalog = [] # list of {"id","title","author","genre","copies_total","copies_available"}
        self.members = {} # dict of member_id: {"name","email","phone"}
        self.reminders = [] # list of {"member_id","book_id","due_date", "message"}
        self.loans = [] # list of {"member_id","book_id","loan_date","due_date", "returneed": bool}


     # ----------------------------------------------------
     # SIMPLE function (5-10 lines) BOOK AVAILABILITY CHECK
     # ----------------------------------------------------
    def is_book_available(self, book_id):
        pass
        

