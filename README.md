# Library Management System - Function Library

**Team:** Group 5  
**Domain:** Library and Information Management  
**Course:** INST326 - Object-Oriented Programming for Information Science  

---

## Project Overview

This project implements a **Library Management System Function Library** that provides core functionality for managing a small digital library.  
The system supports operations such as **book cataloging, member management, search and recommendations, loan tracking, and rating systems**.

These functions and classes work together to simulate a full backend library system, serving as the foundation for more advanced object-oriented development and future web or database integration.

---

## Problem Statement

Libraries face common challenges with:

- Tracking books, members, and active loans in a consistent way  
- Managing availability and waitlists for popular titles  
- Recommending books based on user preferences and history  
- Processing checkouts, returns, and overdue notifications  
- Organizing a consistent catalog of metadata and ratings  

Our system addresses these by maintaining **global shared data structures** that all classes interact with — ensuring that catalog, member, and loan information stay synchronized throughout every operation.

---

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
No external dependencies required — the project uses only the Python Standard Library.

Import classes or functions in your code:

```python
from src.book_class import Book
from src.member_class import Member
from src.search_class import Search
from src.loan_class import Loan
from src import library_functions as lib
```

## Quick Usage Examples
### 📘 Book and Member Creation
``` python
from src.book_class import Book
from src.member_class import Member
from src import library_functions as lib

new_book = Book("1000000010", "Artificial Intelligence: A Modern Approach", "Russell & Norvig", "Computer Science", copies_total=5)
new_member = Member("M100", "Jane Doe", "jane@example.com")

print(new_book)
print(new_member)
```

### 🔍 Searching the Catalog
```python
from src.search_class import Search

s = Search()
results = s.find_books(query="code")
for r in results:
    print(r["title"], "-", r["author"])
```

### 📚 Reserving and Waitlisting
```python
print(s.reserve("M1", "1000000002"))
print(s.manage_waitlist("1000000001", "M4", "add"))
```

### 📆 Loan Management
```python
from src.loan_class import Loan
from datetime import datetime

loan = Loan("M1", "1000000003", borrow_date=datetime.now())
print(loan)
print("Overdue:", loan.is_overdue())
```

### ⭐ Ratings
```python
print(lib.rate_book("M1", "1000000001", 5))
print(lib.rate_book("M3", "1000000001", 4))
print(lib.average_ratings)
```

## Function Library Overview
The function library contains over 20 integrated utilities, organized across four main domains:

### 📚 Book Management
- `validate_code()` — Ensures valid book ID or ISBN format

- `is_book_available()` — Checks catalog for availability

- `rate_book()` — Adds and averages user ratings

- `update_catalog()` — Adds new book records to the global catalog

### 👤 Member Management
- `add_member()` — Adds new library members

- `update_member_balance()` — Adjusts user account balances

- `get_active_members()` — Lists all currently active members

- `pay_balance()` — Simulates payment processing

### 🔍 Search and Recommendation
- search_catalog() — Keyword, author, and genre search

- reserve_book() — Places a member on a waitlist or reserves a copy

- waitlist_management() — Adds/removes users from waitlists

- recommend_books() — Recommends titles based on preferences and tags

### 📆 Loan and Reporting
- calculate_due_date() — Generates loan due dates

- generate_borrowing_report() — Summarizes borrowing statistics

- automated_overdue_notifications() — Simulates overdue alerts

## Object-Oriented Design
The system includes four main classes that encapsulate these functions and maintain consistent state across all operations:

| Class | Responsibility | Connected Global Structures |
|:------|:----------------|:-----------------------------|
| **Book** | Represents a single library item and its availability, ratings, and metadata | `catalog`, `average_ratings` |
| **Member** | Represents an individual user, tracks balance, preferences, and loans | `members` |
| **Search** | Handles catalog search, reservations, and recommendation features | `catalog`, `members`, `waitlists` |
| **Loan** | Tracks borrowing, due dates, and overdue status | `loans` |

Each class interacts directly with shared global data structures imported from library_functions, ensuring all updates are reflected system-wide.

## Team Member Contributions
### Matthew Lazcano — Lead Developer & Project Integrator
- Led the overall development, integration, and debugging of the system
- Managed GitHub repository, version control, and final code implementation
- Designed and implemented the Book, Member, Search, and Loan classes
- Oversaw function integration, testing, and demo script creation
- Coordinated bug fixes, code validation, and system synchronization

### Abi [Last Name] — Project Coordinator & Function Developer
- Ensured team coordination by organizing meetings, managing deadlines, and maintaining communication
- Contributed to the development of the Search class and core functions including:
reserve_book, rate_book, validate_code, validate_isbn10_format, validate_isbn13_format, and generate_borrowing_report
- Provided leadership and accountability throughout the project timeline

### Kaliza [Last Name] — Member System Developer
- Developed the Member class with well-structured methods and reliable functionality
- Authored key supporting functions: calculate_due_date, member_count, check_in_out_operations, and waitlist_management
- Consistently delivered accurate and on-time code submissions with minimal revision needed

### Rood [Last Name] — Function Contributor
- Contributed in making the Loan class and several functional components
- Authored functions including: format_search_query, user_account, and recommend_books
- Assisted in conceptual discussions and provided testing support during development phases