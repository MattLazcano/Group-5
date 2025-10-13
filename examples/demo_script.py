# Demonstrates key functions
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.library_name import LibraryClass
# Create an instance of Library
lib = LibraryClass()

lib.catalog = [
    {"id": "B1", "title": "Dune", "author": "Frank Herbert", "genre": "sci-fi",
     "copies_total": 3, "copies_available": 1},
    {"id": "B2", "title": "Clean Code", "author": "Robert C. Martin", "genre": "programming",
     "copies_total": 2, "copies_available": 0},
    {"id": "B3", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy",
     "copies_total": 4, "copies_available": 2},
    {"id": "B4", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "programming",
     "copies_total": 3, "copies_available": 1},
    {"id": "B5", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "fiction",
     "copies_total": 2, "copies_available": 2},
    {"id": "B6", "title": "1984", "author": "George Orwell", "genre": "fiction",
     "copies_total": 5, "copies_available": 3},
]

lib.members = {
    "M1": {"name": "Matthew"},
    "M2": {"name": "Rood"},
    "M3": {"name": "Eliza"},
    "M4": {"name": "Abi"},
    "M5": {"name": "Dempwolf"},
}

lib.loans = [
    # Active loans (not yet returned)
    {"member_id": "M1", "book_id": "B1",
     "borrow_date": "2025-10-05", "due_date": "2025-10-10",
     "return_date": None, "returned": False},  # Active, not overdue yet
    {"member_id": "M2", "book_id": "B2",
     "borrow_date": "2025-09-25", "due_date": "2025-09-30",
     "return_date": None, "returned": False},  # Active, overdue
    {"member_id": "M3", "book_id": "B3",
     "borrow_date": "2025-09-15", "due_date": "2025-09-25",
     "return_date": None, "returned": False},  # Active, long overdue

    # Returned on time
    {"member_id": "M4", "book_id": "B4",
     "borrow_date": "2025-09-10", "due_date": "2025-09-20",
     "return_date": "2025-09-19", "returned": True},
    {"member_id": "M5", "book_id": "B5",
     "borrow_date": "2025-09-15", "due_date": "2025-09-25",
     "return_date": "2025-09-25", "returned": True},

    # Returned late
    {"member_id": "M1", "book_id": "B6",
     "borrow_date": "2025-09-01", "due_date": "2025-09-10",
     "return_date": "2025-09-15", "returned": True},
    {"member_id": "M2", "book_id": "B3",
     "borrow_date": "2025-08-20", "due_date": "2025-09-01",
     "return_date": "2025-09-05", "returned": True},
]

lib.reservations = {
    "M4": ["B1"],  # Diana reserved Dune
    "M5": ["B2"],  # Evan reserved Clean Code
}

lib.waitlists = {
    "B2": ["M3", "M5"],  # Multiple people waiting for Clean Code
    "B1": ["M2"],        # Bob waiting for Dune
}

lib.ratings = {
    "B1": {"M1": 5, "M2": 4, "M3": 5},
    "B2": {"M1": 4, "M4": 3},
    "B3": {"M5": 5},
}
lib.average_ratings = {
    "B1": 4.67,
    "B2": 3.5,
    "B3": 5.0,
}

print("Library initialized")
print(f"Catalog size: {len(lib.catalog)} books")
print(f"Members: {len(lib.members)}")
print(f"Loans: {len(lib.loans)} active/returned")

# -------------------------
# Example usage / test code
# -------------------------

# Reserve Book Example
print("---- Reserve Book ----")
print(lib.reserve_book("M1", "B1"))   # should reserve since 1 copy left
print(lib.reserve_book("M2", "B2"))   # should add to waitlist (no copies)
print(lib.reserve_book("M2", "B2"))   # already on waitlist
print()

# Rate Book Example
print("---- Rate Book ----")
print(lib.rate_book("M1", "B1", 5))   # first rating
print(lib.rate_book("M2", "B1", 4))   # another rating
print(lib.rate_book("M1", "B1", 3))   # updates rating
print("Average ratings:", lib.average_ratings)
print()

# Validate ISBN Example
print("---- Validate ISBN ----")
print("Valid ISBN-10 (0-306-40615-2):", lib.validate_code("0-306-40615-2"))
print("Valid ISBN-13 (9780306406157):", lib.validate_code("9780306406157"))
print("Invalid ISBN (12345):", lib.validate_code("12345"))
print()

# Generate Borrowing Report Example
print("---- Borrowing Report ----")
report = lib.generate_borrowing_report()
for key, value in report.items():
    print(f"{key}: {value}")