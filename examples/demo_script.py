# Demonstrates key functions

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.library_name import LibraryClass
from datetime import datetime
# Create an instance of Library
# Create the library instance
lib = LibraryClass()

# -----------------------------
# Catalog (with tags + per-book waitlists)
# -----------------------------
lib.catalog = [
    {"id": "B1", "title": "Dune", "author": "Frank Herbert", "genre": "sci-fi",
    "tags": {"sci-fi", "classic", "space"}, "copies_total": 3, "copies_available": 1,
    "waitlist": ["M2"]},  # Bob waiting for Dune
    {"id": "B2", "title": "Clean Code", "author": "Robert C. Martin", "genre": "programming",
    "tags": {"programming", "software", "best-practices"}, "copies_total": 2, "copies_available": 0,
    "waitlist": ["M3", "M5"]},  # Multiple people waiting for Clean Code
    {"id": "B3", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy",
    "tags": {"fantasy", "adventure", "classic"}, "copies_total": 4, "copies_available": 2},
    {"id": "B4", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "programming",
    "tags": {"programming", "craft", "career"}, "copies_total": 3, "copies_available": 1},
    {"id": "B5", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "fiction",
    "tags": {"fiction", "classic", "literature"}, "copies_total": 2, "copies_available": 2},
    {"id": "B6", "title": "1984", "author": "George Orwell", "genre": "fiction",
    "tags": {"dystopia", "classic", "political"}, "copies_total": 5, "copies_available": 3},
]

# -----------------------------
# Members (with email/active/balance + optional preferences for recs)
# -----------------------------
lib.members = {
    "M1": {"name": "Matthew",  "email": "matthew@example.com", "active": True, "balance": 0.0,
        "preferences_tags": {"sci-fi", "fantasy"},
        "preferences_authors": {"Frank Herbert"}},
    "M2": {"name": "Rood",     "email": "rood@example.com",    "active": True, "balance": 0.0},
    "M3": {"name": "Eliza",    "email": "eliza@example.com",   "active": True, "balance": 0.0},
    "M4": {"name": "Abi",      "email": "abi@example.com",     "active": True, "balance": 0.0},
    "M5": {"name": "Dempwolf", "email": "dempwolf@example.com","active": True, "balance": 0.0},
}

# -----------------------------
# Loans (mix of active/returned/overdue)
# -----------------------------
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

# -----------------------------
# Reservations + Global Waitlists (compatible with earlier methods)
# -----------------------------
lib.reservations = {
    "M4": ["B1"],  # Abi reserved Dune
    "M5": ["B2"],  # Dempwolf reserved Clean Code
}

lib.waitlists = {
    "B2": ["M3", "M5"],  # Multiple people waiting for Clean Code
    "B1": ["M2"],        # Rood waiting for Dune
}

# -----------------------------
# Ratings (per book) + precomputed averages
# -----------------------------
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
print()

# Calculate a due date
print("---- Calculate Due Date ----")
borrowed_on = datetime(2025, 10, 13)
print("Due date:", lib.calculate_due_date(borrowed_on, loan_days=14, skip_weekends=True))
print()

# Count members
print("---- Member Count ----")
print("Total members:", lib.member_count())  # counts all
print("Active members only:", lib.member_count(active_only=True))
print()

# Borrow a book
print("---- Borrow Book ----")
print(lib.check_in_out_operations("M1", "B3", action="borrow", loan_days=14))
print()

# Return the same book
print("---- Return Book ----")
print(lib.check_in_out_operations("M1", "B3", action="return"))
print()

# Add to waitlist (when no copies available)
print("---- Waitlist Management ----")
print(lib.waitlist_management("B2", "M3", action="add"))
print()

# Notify next on waitlist
print("---- Notify Waitlist ----")
print(lib.waitlist_management("B2", action="notify", user_id="M1"))  # user_id ignored for notify
print()

print("\n--- TESTING format_search_query ---")
print(lib.format_search_query(' "Data Science" and AI in libraries '))


print("\n--- TESTING user_account (validate / borrow / return / pay) ---")
# validate
print("Validate:", lib.user_account(action="validate", user_id="M1"))

# borrow a book
borrow = lib.user_account(action="borrow", user_id="M1", isbn="B3")
print("Borrow:", borrow)

# return the same book
returned = lib.user_account(action="return", user_id="M1", isbn="B3", grace_days=1)
print("Return:", returned)

# pay a small fine
payment = lib.user_account(action="pay", user_id="M1", pay_amount="1.25")
print("Pay:", payment)


print("\n--- TESTING recommend_books ---")
# give Matthew (M1) some preferences
lib.members["M1"]["preferences_tags"] = {"sci-fi", "fantasy"}
lib.members["M1"]["preferences_authors"] = {"Frank Herbert"}

# run recommendation system
recs = lib.recommend_books(member_id="M1", limit=5)
print("Recommendations:")
for book_id, score in recs:
    print(f"  {book_id}: {score}")

