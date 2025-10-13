# Main function library
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
import re, unicodedata
from decimal import Decimal, ROUND_HALF_UP


class LibraryClass:
    from datetime import datetime, timedelta
    from collections import defaultdict, Counter
    def __init__(self):
        self.catalog = [] # list of {"id","title","author","genre","copies_total","copies_available"}
        self.members = {} # dict of member_id: {"name","email","phone"}
        self.reminders = [] # list of {"member_id","book_id","due_date", "message"}
        self.loans = [] # list of {"member_id","book_id","loan_date","due_date", "returneed": bool}
        self.reservations = {}  # member_id -> list of book_ids
        self.waitlists = {}     # book_id   -> list of member_ids
        self.ratings = {}           # book_id -> {member_id: rating}
        self.average_ratings = {}   # book_id -> average_rating


     # ----------------------------------------------------
     # SIMPLE function (5-10 lines) BOOK AVAILABILITY CHECK (Matthew)
     # ----------------------------------------------------
    def is_book_available(self, title):
        t = title.strip().lower()
        for item in self.catalog:
            if item["title"].strip().lower() == t:
                return item["copies_available"] > 0
            return False
    
    # ----------------------------------------------------
     # SIMPLE function (5-10 lines) Reminder Scheduling (Matthew)
     # ----------------------------------------------------
    def schedule_reminder(self, member_id, book_id, due_date):
        if member_id in self.members and any(b["id"] == book_id for b in self.catalog):
            message = f"Reminder: Book ID {book_id} is due on {due_date}."
            self.reminders.append({"member_id": member_id, "book_id": book_id, "due_date": due_date, "message": message})
            return True
        return False
    
    # ----------------------------------------------------
    # MEDIUM (15–25 lines) Search and Filter Catalog (Matthew)
    # ----------------------------------------------------
    def search_catalog(self, query: str = "", authoer: str = "", genre: str = "", available: bool = None):
        results = []
        q = query.strip().lower()
        a = authoer.strip().lower()
        g = genre.strip().lower()
        
        for item in self.catalog:
            title_match = (q in item["title"].strip().lower()) or (q in item["author"].strip().lower()) if q else True
            author_match = a in item["author"].strip().lower() if a else True
            genre_match = (g == item["genre"].strip().lower()) if g else True
            availability_match = (item["copies_available"] > 0) if available is True else (item["copies_available"] == 0) if available is False else True

            if title_match and author_match and genre_match and availability_match:
                results.append(item)
        return results
    
    # ----------------------------------------------------
    # COMPLEX (30+ lines) Automated Overdue Notifications (Matthew)
    # ----------------------------------------------------
    def automated_overdue_notifications(self, today: datetime | None = None, daily_fee: float = 0.25, grace_days: int = 0):
        if today is None:
            today = datetime.now().date()
        cutoff_date = today - timedelta(days=grace_days)

        messages = [] # list of {"member_id", "message", "fee"}  
        total_overdue_items = 0
        notified_member_ids = set()

        for loan in self.loans:
            if loan["returned"]:
                continue
            due_date = loan["due_date"]
            if not isinstance(due_date, datetime):
                continue
            if due_date >= cutoff_date:
                continue

            # Look up book and member (fall back to ids if missing)
            book = None
            for b in self.catalog:
                if b["id"] == loan["book_id"]:
                    book = b
                    break
            title = book.get("title","Unknown Title") if book else str(loan["book_id"])

            member = self.members.get(loan["member_id"], {"name": "Member"})
            member_id = loan["member_id"]

            # Simple fee calc: days overdue * daily_fee
            days_overdue = (today - due_date).days
            fee = max(0, days_overdue) * daily_fee
            total_overdue_items += 1
            notified_member_ids.add(member_id)

            text = (
                f"Hello {member.get('name','Member')}, "
                f"'{title}' is overdue by {days_overdue} day(s). "
                f"Estimated fee so far: ${fee:.2f}. "
                f"Due date was {due_date.date()}. Please return or renew."
            )
            messages.append({"member_id": member_id, "text": text, "fee": round(fee, 2)})

        return {
            "total_overdue_items": total_overdue_items,
            "notified_member_count": len(notified_member_ids),
            "messages": messages
        }

    # ----------------------------------------------------
    # SIMPLE function (5-10 lines) RESERVE BOOK (ABI)
    # This is a simple function as well.
    # This allow u to reserve a book if it avaible if it not then it add the user to a waitlist
    # ----------------------------------------------------
    def reserve_book(self, member_id: str, book_id: str) -> str:
        book = None
         # First things first - does this book even exist?
        for item in self.catalog:
            if item["id"] == book_id:
                book = item
                break
        if book is None:
            return f"Book '{book_id}' not found in catalog."

        # Set up user in reservations if they're new
        if member_id not in self.reservations:
            self.reservations[member_id] = []

        # Don't let people double-book the same book
        if book_id in self.reservations[member_id]:
            return f"You have already reserved book '{book_id}'."

        # it check if any copies of book are available
        copies_left = int(book.get("copies_available", 0))
        # if copies is available then it also reserve the book as well.
        if copies_left > 0:
            self.reservations[member_id].append(book_id) # Add to their list
            book["copies_available"] = copies_left - 1 # Decrement available count
            return f"Book '{book_id}' reserved for member '{member_id}'."

        # Bummer, no copies left. Time for the waitlist...
        if book_id not in self.waitlists:
            self.waitlists[book_id] = []
        # Already waiting? No need to add again
        if member_id in self.waitlists[book_id]:
            return f"You are already on the waitlist for book '{book_id}'."

        # Add them to the back of the line
        self.waitlists[book_id].append(member_id)
        return f"No copies available. Member '{member_id}' added to the waitlist for '{book_id}'."
    
    # ----------------------------------------------------
    # SIMPLE function (5-10 lines) Book Rating System (ABI)
    # This allow u to rate a book between 1 and 5 stars, and updates the average rating for that book
    # ----------------------------------------------------
    def rate_book(self, member_id, book_id, rating):
    
        # First let's check if the rating is valid
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5 stars.")
    
        # Initialize book entry if it doesn't exist yet
        if book_id not in self.ratings:
            self.ratings[book_id] = {}
    
        # Check if this user has rated this book before
        has_previous_rating = False
        if member_id in self.ratings[book_id]:
            has_previous_rating = True
    
        # Store the new rating
        self.ratings[book_id][member_id] = rating
    
        # Now we need to recalculate the average for this book
        book_ratings = self.ratings[book_id]
        rating_values = []
        for user, user_rating in book_ratings.items():
            rating_values.append(user_rating)
    
        # Calculate average and round to 2 decimal places
        total_ratings = len(rating_values)
        sum_of_ratings = sum(rating_values)
        new_average = sum_of_ratings / total_ratings
        new_average = round(new_average, 2)
    
        # Update the average ratings dictionary
        self.average_ratings[book_id] = new_average
    
        # Return appropriate message based on whether this was an update or new rating
        if has_previous_rating:
            message = f"Updated rating for book '{book_id}' to {rating} stars. New average: {new_average}"
        else:
            message = f"Rated book '{book_id}' with {rating} stars. Average now: {new_average}"
    
        return message
    
    # ----------------------------------------------------
    # MEDIUM (15–25 lines) Validate ISBN (ABI)
    # This function validate both ISBN-10 and ISBN-13 formats
    # ----------------------------------------------------
    # Medium complexity
    def validate_code(self, code_input):
        # Check if input is actually a string - this caught me before!
        if not isinstance(code_input, str):
            raise TypeError("Code must be a string.")

        # Clean up the code by removing dashes and spaces, then uppercase it
        cleaned_code = code_input.replace("-", "").replace(" ", "").upper()
        code_length = len(cleaned_code)

        # Check for ISBN-10 format first
        if code_length == 10:
            # Make sure first 9 are digits and last one is digit or X
            first_nine = cleaned_code[:-1]
            last_char = cleaned_code[-1]
            if first_nine.isdigit() and (last_char.isdigit() or last_char == 'X'):
                return self.validate_isbn10_format(cleaned_code)

        # Then check ISBN-13
        elif code_length == 13 and cleaned_code.isdigit():
            return self.validate_isbn13_format(cleaned_code)

        # For other codes, just check if they're reasonable length and alphanumeric
        elif code_length >= 6 and code_length <= 20:
            if cleaned_code.isalnum():
                return True  # Assuming other product codes are valid if alphanumeric
            else:
                return False
        else:
            return False


    #  Validates ISBN-10 using the checksum algorithm
    def validate_isbn10_format(self, isbn_code):
        checksum = 0
        position = 10  # Start from position 10, decrement for each digit

        for char in isbn_code:
            if char == 'X':
                digit_value = 10
            else:
                digit_value = int(char)

            checksum += digit_value * position
            position -= 1  # Move to next position

        # Valid if checksum is divisible by 11
        return checksum % 11 == 0


    def validate_isbn13_format(self, isbn_code):
        total_sum = 0
        for index in range(len(isbn_code)):
            current_digit = int(isbn_code[index])
            # Even positions (0,2,4...) get weight 1, odd positions get weight 3
            if index % 2 == 0:
                weight = 1
            else:
                weight = 3

            total_sum += current_digit * weight
        # Check if total is divisible by 10
        is_valid = (total_sum % 10 == 0)
        return is_valid
    
    # ----------------------------------------------------
    # COMPLEX (30+ lines) Generating Borrowing Report (ABI)
    # This function generate a report of borrowing activity
    # ----------------------------------------------------
    #Creates a report showing borrowing stats, overdue books, and fines owed
    def generate_borrowing_report(self, fine_per_day=0.5):
        # Let's start with some basic counts
        total_borrowed = len(self.loans)
        overdue_count = 0
        total_fines = 0.0
    
        # Track user activity - using defaultdict to avoid key errors
        users = defaultdict(lambda: {
            "borrowed": 0,
            "overdue": 0,
            "fines": 0.0
        })
    
        # Count how many times each book was borrowed
        book_counts = Counter()
    
        # Get today's date for comparison
        current_date = datetime.today()
    
        # Go through each borrowing record
        for record in self.loans:
            user_id = record.get("user_id") or record.get("member_id")
            book_id = record.get("book_id")
            if not user_id or not book_id:
                continue
        
            # Parse the dates from strings
            borrowed_on = None
            if isinstance(record.get("borrow_date"), str):
                borrowed_on = datetime.strptime(record["borrow_date"], "%Y-%m-%d")

            # due_date may be a datetime (your format) or a string (teammate’s format)
            due_field = record.get("due_date")
            if isinstance(due_field, datetime):
                due_on = due_field
            elif isinstance(due_field, str):
                due_on = datetime.strptime(due_field, "%Y-%m-%d")
            else:
                continue  # skip malformed
        
            returned_on_str = record.get("return_date")
        
            # Update user stats
            users[user_id]["borrowed"] += 1
            book_counts[book_id] += 1
        
            # Figure out the return date
            if returned_on_str is not None:
                if isinstance(returned_on_str, datetime):
                    returned_on = returned_on_str
                else:
                    returned_on = datetime.strptime(returned_on_str, "%Y-%m-%d")
            else:
                # If your data marks returned=True but lacks a date, treat as returned on due date (no fee)
                if record.get("returned") is True:
                    returned_on = due_on
                else:
                    # Book hasn't been returned yet, so use today's date
                    returned_on = current_date
        
            # Check if it's overdue
            if returned_on > due_on:
                days_late = (returned_on - due_on).days
                fine_amount = days_late * fine_per_day
            
                # Update counters
                users[user_id]["overdue"] += 1
                users[user_id]["fines"] += fine_amount
                overdue_count += 1
                total_fines += fine_amount
    
        # Find the most active user (borrowed the most books)
        most_active = None
        if users:
            # Sort by number of books borrowed
            sorted_users = sorted(users.items(), key=lambda item: item[1]["borrowed"], reverse=True)
            most_active = sorted_users[0][0]
    
        # Find the most popular book
        top_book = None
        if book_counts:
            most_common = book_counts.most_common(1)
            top_book = most_common[0][0]
    
        # Build the final report
        report = {
            "total_books_borrowed": total_borrowed,
            "total_overdue_books": overdue_count,
            "total_fines_collected": round(total_fines, 2),
            "user_activity": dict(users),  # Convert defaultdict back to regular dict
            "most_active_user": most_active,
            "most_borrowed_book": top_book
        }
    
        return report
    
    # ----------------------------------------------------
    # Simple Function (5-10 lines) Calculate Due Date (Eliza)
    # Calculate the due date for a borrowed library item.
    # ----------------------------------------------------
    def calculate_due_date(self, borrow_date: datetime, loan_days: int = 14, skip_weekends: bool = True) -> datetime:
        """Calculate the due date for a borrowed library item."""

        if not isinstance(borrow_date, datetime):
            raise TypeError("borrow_date must be a datetime object")
        # checks that the borrow_date is actually a datetime object, not a string or number
        
        if loan_days <= 0:
            raise ValueError("loan_days must be greater than 0")
        # makes sure the number of loan days is positive (you can’t borrow for 0 or negative days)
        
        due_date = borrow_date
        # start counting from the date the book was borrowed

        days_added = 0
        # keeps track of how many valid days have been counted so far

        while days_added < loan_days:
            due_date += timedelta(days=1)
            # move forward by one day

            if skip_weekends and due_date.weekday() in (5, 6):
                continue
            # if skip_weekends is True, skip Saturdays (5) and Sundays (6)

            days_added += 1
            # only count this day if it’s not a weekend

        return due_date
        # once we’ve added all valid loan days, return the due date

    # ----------------------------------------------------
    # SIMPLE Function (5-10 lines) Member Count (Eliza)
    # Return the total number of registered library members.
    # ----------------------------------------------------
    def member_count(self, active_only: bool = True) -> int:
        """Count how many library members exist in the system."""
        
        users = self.members
        # use the class’s member dictionary as the data source

        if not isinstance(users, dict):
            raise TypeError("users must be a dictionary")
        # ensures that the input is a dictionary like {user_id: {info}}

        count = 0
        # start a counter at zero to count members

        for udata in users.values():
            # loop through every user’s information inside the dictionary
            
            if not active_only or udata.get("active", True):
                count += 1
            # if we’re counting everyone, add all users
            # if we’re counting only active ones, check if “active” is True

        return count
        # return the total number of users found

    # ----------------------------------------------------
    # MEDIUM (15–25 lines) check in/ check out operations (Eliza)
    # Used to track exact borrow and return times
    # ----------------------------------------------------
    def check_in_out_operations(self, user_id: str, isbn: str, action: str = "borrow", loan_days: int = 14) -> dict:
        """Manage check-in and check-out operations for library books."""
        
        users = self.members
        catalog_list = self.catalog

        if user_id not in users:
            raise KeyError(f"User {user_id} not found")
        # makes sure the user exists in the system

        # find book by id inside self.catalog (list of dicts)
        book = None
        for item in catalog_list:
            if item.get("id") == isbn:
                book = item
                break
        if book is None:
            raise KeyError(f"Book {isbn} not found")
        # makes sure the book exists in the catalog

        user = users[user_id]
        # get that specific user’s data

        if action == "borrow":
            # if the action is borrowing a book

            if book.get("copies_available", 0) <= 0:
                raise ValueError(f"No available copies of {book.get('title', 'Unknown')}")
            # if there are no copies left, stop and show an error

            book["copies_available"] -= 1
            # reduce the available quantity by one

            loans = user.setdefault("loans", {})
            # get the user’s loan record or make one if it doesn’t exist yet

            if isbn in loans and loans[isbn].get("returned_at") is None:
                raise ValueError("This book is already borrowed and not yet returned.")
            # prevent the same user from borrowing the same book twice

            borrowed_at = datetime.now(timezone.utc)
            # record the current time as the borrow time

            due_at = self.calculate_due_date(borrowed_at, loan_days)
            # use your other function to figure out when it’s due

            loans[isbn] = {"borrowed_at": borrowed_at, "due_at": due_at, "returned_at": None}
            # save the borrowing record inside the user’s loan list

            return {
                "user": user_id,
                "book": isbn,
                "status": "borrowed",
                "due_at": due_at
            }
            # return a summary of what just happened

        elif action == "return":
            # if the action is returning a book

            loans = user.get("loans", {})
            # get the user’s list of borrowed books

            if isbn not in loans or loans[isbn].get("returned_at"):
                raise ValueError("Book not currently borrowed or already returned.")
            # make sure the book was actually borrowed and not already marked as returned

            book["copies_available"] = book.get("copies_available", 0) + 1
            # add one copy back to the catalog

            loans[isbn]["returned_at"] = datetime.now(timezone.utc)
            # mark the return time for this book

            return {
                "user": user_id,
                "book": isbn,
                "status": "returned",
                "returned_at": loans[isbn]["returned_at"]
            }
            # return a summary of the return process

        else:
            raise ValueError("Invalid action. Use 'borrow' or 'return'.")
        # if the user types something other than borrow/return, show an error

    # ----------------------------------------------------
    # MEDIUM (15–25 lines) Waitlist Management (Eliza)
    # Add users to waitlist when a book is unavailable and notify them when available
    # ----------------------------------------------------
    def waitlist_management(self, isbn: str, user_id: str, action: str = "add") -> dict:
        """Manage a book's waitlist for unavailable items."""
        
        # locate book in self.catalog (list) by id
        book = None
        for item in self.catalog:
            if item.get("id") == isbn:
                book = item
                break
        if book is None:
            raise KeyError(f"Book {isbn} not found in catalog.")
        # makes sure the book exists before doing anything

        if user_id not in self.members:
            raise KeyError(f"User {user_id} not found.")
        # makes sure the user exists in the system

        # get that specific book’s details
        # make sure there’s a “waitlist” key in the book data, or create one if not
        waitlist = book.setdefault("waitlist", [])

        if action == "add":
            # if we’re adding a user to the waitlist

            if book.get("copies_available", 0) > 0:
                return {"message": f"Book '{book.get('title', 'Unknown')}' is available; no need for waitlist."}
            # if copies are available, tell the user they can borrow right away

            if user_id in waitlist:
                return {"message": f"User {user_id} is already on the waitlist for {isbn}."}
            # if the user is already waiting for this book, don’t add them twice

            waitlist.append(user_id)
            # add the user to the end of the waitlist

            return {"isbn": isbn, "waitlist": waitlist}
            # return the updated waitlist

        elif action == "notify":
            # if we’re notifying the next person on the waitlist

            if not waitlist:
                return {"message": f"No users on the waitlist for {isbn}."}
            # if there’s no one waiting, show a message

            next_user = waitlist.pop(0)
            # remove the first user (the one waiting longest)

            return {
                "isbn": isbn,
                "notify_user": next_user,
                "message": f"Notify {next_user}: '{book.get('title', 'Unknown')}' is now available."
            }
            # return a message telling who to notify

        else:
            raise ValueError("Invalid action. Use 'add' or 'notify'.")
        # if the action isn’t one of those two, stop with an error

    # ----------------------------------------------------
    # SIMPLE Function (5-10 lines)  Format Search Query (Rood)
    # ----------------------------------------------------
    def format_search_query(self, q):
        """
        Clean up a search query and return:
            - original text
            - normalized text (cleaned)
            - list of tokens (words/phrases)
        """
        # Make sure we have a string; trim spaces; lower-case it
        s = (q or "").strip().lower()
        # Remove accents: "café" -> "cafe"
        s = "".join(
            c for c in unicodedata.normalize("NFKD", s)
            if not unicodedata.combining(c)
        )
        # Pull out quoted phrases like "data science"
        phrases = [m.strip('"') for m in re.findall(r'"([^"]*)"', s)]
        # Remove quoted parts from the main text
        s = re.sub(r'"[^"]*"', " ", s)
        # Keep letters, numbers, and hyphens; turn everything else into spaces
        s = re.sub(r"[^\w\-]+", " ", s).strip()
        # Very common words to ignore
        stop = {"the","a","an","and","or","of","for","to","in","on","at","by","with","from"}
        # Split into words and drop common ones
        toks = []
        for t in s.split():
            if t and t not in stop:
                toks.append(t)
        # Add the quoted phrases at the end (as single tokens)
        for p in phrases:
            if p:
                toks.append(p)
        # Make a nice normalized string from tokens
        return {"original": q or "", "normalized": " ".join(toks), "tokens": toks}
    
    # ----------------------------------------------------
    # MEDIUM (15–25 lines)  User Account Management (Rood)
    # ----------------------------------------------------
    def user_account(
        self,
        *,
        action,
        user_id=None,
        isbn=None,
        loan_days=14,
        daily_rate=Decimal("0.25"),
        grace_days=0,
        pay_amount=None,
        user_obj=None,
        ):
        """
        Manage basic account actions.
        catalog example (adapted from your list):
            self.catalog = [{"id": "B1", "title": "...", "author": "...", "tags": {"fantasy"}, "copies_available": 3}, ...]
        users example:
            self.members = {"u1": {"name": "Alex", "email": "a@b.com", "active": True, "loans": {}, "balance": Decimal("0.00")}}
        """
        # Always keep money at 2 decimal places
        def money(x):
            return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Build a quick lookup for catalog by id (maps isbn->book dict)
        catalog = {b.get("id"): b for b in self.catalog}
        users = self.members

        # ---- validate ----
        if action == "validate":
            u = user_obj or (users.get(user_id) if user_id else None)
            if not u or not u.get("active", True):
                raise ValueError("Account disabled/missing")
            if not (u.get("name") or "").strip():
                raise ValueError("Name required")
            # Simple email check (beginner-friendly)
            email = (u.get("email") or "").strip()
            if "@" not in email or "." not in email.split("@")[-1]:
                raise ValueError("Invalid email")
            return True

        # ---- borrow ----
        if action == "borrow":
            u = users.get(user_id)
            b = catalog.get(isbn)
            if not u or not b:
                raise KeyError("User or book not found")
            # Make sure user looks valid
            self.user_account(
                action="validate",
                user_obj=u
            )
            # Check stock (copies_available)
            if b.get("copies_available", 0) <= 0:
                raise ValueError("No copies")
            # Don’t allow borrowing twice
            loans = u.setdefault("loans", {})
            if isbn in loans and loans[isbn].get("returned_at") is None:
                raise ValueError("Already borrowed")
            # Create the loan
            now = datetime.now(timezone.utc)
            due = now + timedelta(days=loan_days)
            b["copies_available"] = int(b.get("copies_available", 0)) - 1
            loans[isbn] = {"borrowed_at": now, "due_at": due, "returned_at": None}
            return loans[isbn]

        # ---- return ----
        if action == "return":
            u = users.get(user_id)
            b = catalog.get(isbn)
            if not u:
                raise KeyError("User not found")
            loans = u.setdefault("loans", {})
            loan = loans.get(isbn)
            if not loan or loan.get("returned_at") is not None:
                raise KeyError("No active loan")
            now = datetime.now(timezone.utc)
            loan["returned_at"] = now
            # Days late (if any)
            due_date = loan["due_at"].date()
            days_late = (now.date() - due_date).days
            # You can be late by "grace_days" without a fine
            effective_late = max(0, days_late - max(0, grace_days))
            # Fine = days late * daily_rate
            fine = Decimal("0.00")
            if effective_late > 0:
                fine = money(Decimal(effective_late) * money(daily_rate))
                u["balance"] = money(Decimal(u.get("balance", "0.00")) + fine)
            # Put the book back on the shelf
            if b is not None:
                b["copies_available"] = int(b.get("copies_available", 0)) + 1
            return {
                "isbn": isbn,
                "returned_at": now,
                "days_late": max(0, days_late),
                "effective_late": effective_late,
                "fine": money(fine),
                "balance": money(Decimal(u.get("balance", "0.00"))),
            }

        # ---- pay ----
        if action == "pay":
            u = users.get(user_id)
            if not u:
                raise KeyError("User not found")
            amt = money(pay_amount or 0)
            if amt <= 0:
                raise ValueError("Payment must be > 0")
            current = money(Decimal(u.get("balance", "0.00")))
            new_balance = current - amt
            if new_balance < 0:
                new_balance = Decimal("0.00")
            u["balance"] = money(new_balance)
            return {"paid": amt, "balance": money(new_balance)}

        # Unknown action
        raise ValueError(f"Unknown action: {action!r}")
    
    # ----------------------------------------------------
    # COMPLEX (30+ lines)  Recommendation System (Rood)
    # ----------------------------------------------------
    def recommend_books(self, *, member_id, limit=10):
        """
        Recommend books based on:
            - Tags the user likes
            - Authors the user likes
            - Tags from books the user borrowed before
            - Prefer books that are in stock
        Returns a list of (isbn, score), highest score first.
        """
        # Build dict catalog keyed by book id (isbn-like)
        catalog = {b.get("id"): b for b in self.catalog}
        user = self.members.get(member_id, {})

        # Read user preferences and history
        prefs_tags = set(user.get("preferences_tags", set()))
        prefs_authors = set(user.get("preferences_authors", set()))
        member_loans_dict = user.get("loans", {}) or {}

        # Borrowed isbns from member's personal loan dict; if empty, fall back to global loans
        borrowed_isbns = set(member_loans_dict.keys())
        if not borrowed_isbns:
            borrowed_isbns = {ln["book_id"] for ln in self.loans if ln.get("member_id") == member_id}

        # Count tags from user's past loans (simple dict, no Counter)
        history_tag_counts = {}
        for isbn in borrowed_isbns:
            b = catalog.get(isbn)
            if not b:
                continue
            for t in set(b.get("tags", set())):
                history_tag_counts[t] = history_tag_counts.get(t, 0) + 1

        # How to score a single book (keep it very simple)
        def score_book(b):
            tags = set(b.get("tags", set()))
            author = b.get("author", "")
            qty = b.get("copies_available", 0)  # prefer in-stock

            # Tag matches with either the user's likes or history
            tag_matches = 0
            for t in tags:
                if t in prefs_tags or t in history_tag_counts:
                    tag_matches += 1

            # Start with tag score
            score = float(tag_matches)

            # Bonus if author is liked (either by preference or by history)
            if author in prefs_authors:
                score += 1.5

            # Small bonus if the author appeared in the user's history
            if author and any((catalog.get(i) or {}).get("author") == author for i in borrowed_isbns):
                score += 0.5

            # Prefer in-stock books
            if qty and qty > 0:
                score += 0.3
            else:
                score -= 1.0

            return score

        # Score every book the user hasn't already borrowed
        scored = []
        for isbn, b in catalog.items():
            if isbn in borrowed_isbns:
                continue
            s = score_book(b)
            if s > 0:
                scored.append((isbn, s))

        # Sort by score (highest first); simple tie-break using title then isbn
        scored.sort(
            key=lambda item: (item[1], (catalog[item[0]].get("title") or ""), item[0]),
            reverse=True
        )
        # Return the top N
        return scored[:limit]

        

