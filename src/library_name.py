# Main function library
from datetime import datetime, timedelta
from collections import defaultdict, Counter


class LibraryClass:
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

    """
    import re, unicodedata
    def format_search_query(q: str) -> dict:
        s = (q or "").strip().lower()
        s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
        phrases = [m.strip('"') for m in re.findall(r'"([^"\\]|\\.)*"', s)]
        s = re.sub(r'"([^"\\]|\\.)*"', " ", s)
        s = re.sub(r"[^\w\-]+", " ", s).strip()
        stop = {"the","a","an","and","or","of","for","to","in","on","at","by","with","from"}
        toks = [t for t in s.split() if t and t not in stop]
        toks += [p for p in phrases if p]
        return {"original": q or "", "normalized": " ".join(toks), "tokens": toks}
    """

        

