import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.book_class import Book
from src.member_class import Member
from src.loan_class import Loan
from src.search_class import Search
from library_functions import catalog, members, loans


from datetime import datetime

# ------------------------------
# 1️⃣ Setup Sample Data
# ------------------------------
catalog[:] = [
    {"id": "BK001", "title": "Dune", "author": "Frank Herbert", "genre": "sci-fi",
    "tags": {"sci-fi", "classic", "space"}, "copies_total": 3, "copies_available": 1,
    "waitlist": ["M2"]},  # Rood waiting for Dune
    {"id": "BK002", "title": "Clean Code", "author": "Robert C. Martin", "genre": "programming",
    "tags": {"programming", "software", "best-practices"}, "copies_total": 2, "copies_available": 0,
    "waitlist": ["M3", "M5"]},  # Eliza and Dempwolf waiting
    {"id": "BK003", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy",
    "tags": {"fantasy", "adventure", "classic"}, "copies_total": 4, "copies_available": 2},
    {"id": "BK004", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "programming",
    "tags": {"programming", "craft", "career"}, "copies_total": 3, "copies_available": 1},
    {"id": "BK005", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "fiction",
    "tags": {"fiction", "classic", "literature"}, "copies_total": 2, "copies_available": 2},
    {"id": "BK006", "title": "1984", "author": "George Orwell", "genre": "fiction",
    "tags": {"dystopia", "classic", "political"}, "copies_total": 5, "copies_available": 3},
]

members.clear()
members.update({
    "M1": {"name": "Matthew",  "email": "matthew@example.com", "active": True, "balance": 0.0,
        "preferences_tags": {"sci-fi", "fantasy"},
        "preferences_authors": {"Frank Herbert"}, "loans": {}},
    "M2": {"name": "Rood",     "email": "rood@example.com",    "active": True, "balance": 0.0, "loans": {}},
    "M3": {"name": "Eliza",    "email": "eliza@example.com",   "active": True, "balance": 0.0, "loans": {}},
    "M4": {"name": "Abi",      "email": "abi@example.com",     "active": True, "balance": 0.0, "loans": {}},
    "M5": {"name": "Dempwolf", "email": "dempwolf@example.com","active": True, "balance": 0.0, "loans": {}},
})

print("Custom dataset initialized with books and team members.\n")

# ------------------------------
# 2 Book Tests
# ------------------------------
print("Testing Book class:")
book = Book("BK001", "Dune", "Frank Herbert", "sci-fi", 3)
print(book)
print("Available?", book.check_availability())
print(book.add_rating("M1", 5))
print()

# ------------------------------
# 3 Member Tests
# ------------------------------
print("Testing Member class:")
matthew = Member("M1", "Matthew", "matthew@example.com")
print(matthew)

# Borrow and return
print(matthew.borrow_book("BK001"))
print(matthew.return_book("BK001"))
print(matthew.pay_balance(10.00))
print()

# ------------------------------
# 4 Loan Tests
# ------------------------------
print("Testing Loan class:")
loan = Loan("M1", "BK003", datetime.now())
print(loan)
print("Is overdue?", loan.is_overdue())

# Generate reports
report = Loan.generate_reports()
print("\nBorrowing Report Summary:")
for k, v in report.items():
    print(f"{k}: {v}")

notif = Loan.overdue_notifications()
print("\n Overdue Notifications:")
print(notif)
print()

# ------------------------------
# 5 Search Tests
# ------------------------------
print("Testing Search class:")
search = Search()

results = search.find_books(query="programming")
print("Search results for 'programming':")
for r in results:
    print(f" - {r['title']} by {r['author']}")

# Reserve and waitlist
reserve_msg = search.reserve("M4", "BK003")
print("\nReservation result:", reserve_msg)

waitlist_msg = search.manage_waitlist("BK002", "M2", "add")
print("Waitlist result:", waitlist_msg)

# Recommend
recommendations = search.recommend_for_member("M1")
print("\nRecommended books for Matthew:")
for isbn, score in recommendations:
    print(f" - {isbn} (score {score:.2f})")

# Query cleanup
query_info = search.normalize_query('"clean code" by Martin')
print("\nQuery normalization:")
print(query_info)
print()

print("Demo complete — all classes tested successfully with new data.")