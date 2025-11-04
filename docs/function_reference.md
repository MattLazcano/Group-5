# Library Management System - Function Reference Guide

This document provides comprehensive reference information for all core functions in the `library_functions.py` file.  
These functions power the backend logic for catalog management, member handling, loans, and search operations.

---

## Table of Contents

1. [Book Management Functions](#book-management-functions)
2. [Member Management Functions](#member-management-functions)
3. [Search and Recommendation Functions](#search-and-recommendation-functions)
4. [Loan and Notification Functions](#loan-and-notification-functions)
5. [Utility and Validation Functions](#utility-and-validation-functions)

---

## Book Management Functions

### validate_code(code_input)

**Purpose:** Validate a book ID or ISBN (supports ISBN-10, ISBN-13, or custom alphanumeric IDs).  
**Parameters:**
- `code_input` (str): Input code to validate.  
**Returns:** `bool` — True if valid format, False otherwise.  
**Raises:** `TypeError` for non-string input.  

---

### update_catalog(book)

**Purpose:** Add or update a book entry in the global catalog.  
**Parameters:**
- `book` (Book): Book instance to register.  
**Returns:** `dict` — Updated catalog record.

---

### is_book_available(book_id)

**Purpose:** Check whether a book has available copies for borrowing.  
**Parameters:**
- `book_id` (str): Unique ID or ISBN.  
**Returns:** `bool` — True if copies are available.

---

### rate_book(member_id, book_id, rating)

**Purpose:** Record and average member ratings for a book.  
**Parameters:**
- `member_id` (str): ID of the reviewing member.  
- `book_id` (str): ID of the book being rated.  
- `rating` (int): Rating from 1–5.  
**Returns:** `float` — Updated average rating.

---

## Member Management Functions

### add_member(member_id, name, email)

**Purpose:** Add a new member to the system.  
**Returns:** `dict` — Member profile.  

---

### update_member_balance(member_id, amount)

**Purpose:** Increase or decrease a member’s account balance (e.g., late fees).  
**Parameters:**
- `member_id` (str)
- `amount` (float): Positive or negative adjustment.  
**Returns:** `float` — New balance.  

---

### pay_balance(member_id, payment_amount)

**Purpose:** Process balance payments for a member.  
**Returns:** `float` — Updated balance after payment.  

---

## Search and Recommendation Functions

### search_catalog(query)

**Purpose:** Find books by keyword, author, or genre.  
**Parameters:**
- `query` (str): Search string.  
**Returns:** `list[dict]` — Matching book records.

---

### reserve_book(member_id, book_id)

**Purpose:** Reserve a book for a member if available, otherwise add them to waitlist.  
**Returns:** `str` — Confirmation message.  

---

### waitlist_management(book_id, member_id, action)

**Purpose:** Add or remove a member from a book waitlist.  
**Returns:** `dict` — Updated waitlist information.  

---

### recommend_books(member_id)

**Purpose:** Suggest books to a user based on their preferences and prior ratings.  
**Returns:** `list[tuple]` — (Book ID, recommendation score).  

---

## Loan and Notification Functions

### calculate_due_date(borrow_date, days=14)

**Purpose:** Calculate the due date based on borrowing date and standard loan length.  
**Returns:** `datetime` — Due date.  

---

### generate_borrowing_report()

**Purpose:** Summarize current loan and member activity.  
**Returns:** `dict` — System-wide usage statistics.  

---

### automated_overdue_notifications()

**Purpose:** Identify overdue items and generate simulated notifications.  
**Returns:** `dict` — Overdue summary report.  

---

## Utility and Validation Functions

### format_search_query(query)

**Purpose:** Normalize and tokenize search input for consistency.  
**Returns:** `dict` — Normalized and tokenized query.  

---

### member_count()

**Purpose:** Return the total number of active members.  
**Returns:** `int`

---

### check_in_out_operations(book_id, member_id, action)

**Purpose:** Log and validate check-in/out transactions.  
**Returns:** `str` — Status message.  

---

### user_account(member_id)

**Purpose:** Retrieve account details for a given member.  
**Returns:** `dict` — Account data (balance, loans, history).  
