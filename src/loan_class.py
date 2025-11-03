from datetime import datetime, timedelta
from typing import List, Dict

class Loan:
    """
    Represents a book loan in the library system.
    Handles due date calculation, overdue notifications, and loan reports.
    """

    def __init__(self, loan_id: str, user: str, book: str, borrow_date: str, loan_days: int = 14):
        """
        Initialize a Loan instance with validation.

        Args:
            loan_id (str): Unique loan identifier.
            user (str): The member who borrowed the book.
            book (str): The title of the borrowed book.
            borrow_date (str): Date borrowed ("YYYY-MM-DD").
            loan_days (int): Loan period (default 14 days).
        """
        if not loan_id.strip():
            raise ValueError("Loan ID cannot be empty.")
        if not user.strip() or not book.strip():
            raise ValueError("User and book information must be provided.")
        if not self._is_valid_date(borrow_date):
            raise ValueError("Invalid borrow_date format. Use YYYY-MM-DD.")
        if loan_days <= 0:
            raise ValueError("Loan days must be positive.")

        self._loan_id = loan_id.strip().upper()
        self._user = user.strip().title()
        self._book = book.strip().title()
        self._borrow_date = borrow_date
        self._loan_days = loan_days
        self._returned_date = None

    # ----------------------- Properties -----------------------
    @property
    def loan_id(self):
        return self._loan_id

    @property
    def user(self):
        return self._user

    @property
    def book(self):
        return self._book

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def loan_days(self):
        return self._loan_days

    @property
    def returned_date(self):
        return self._returned_date

    # ----------------------- Helper Methods -----------------------

    def _to_date(self, date_str: str) -> datetime.date:
        """Convert string 'YYYY-MM-DD' to datetime.date."""
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def _to_str(self, date_obj: datetime.date) -> str:
        """Convert datetime.date to 'YYYY-MM-DD' string."""
        return date_obj.strftime("%Y-%m-%d")

    def _is_valid_date(self, date_str: str) -> bool:
        """Check if a string is a valid date in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ----------------------- Core Methods -----------------------

    def calculate_due_date(self) -> str:
        """
        Figure out the due date for this loan based on borrow_date and loan_days.
        Returns the due date as 'YYYY-MM-DD'.
        """
        start = self._to_date(self._borrow_date)
        due = start + timedelta(days=self._loan_days)
        return self._to_str(due)

    def mark_returned(self, return_date: str):
        """
        Mark this loan as returned.

        Args:
            return_date (str): Date the book was returned.
        """
        if not self._is_valid_date(return_date):
            raise ValueError("Invalid return_date format. Use YYYY-MM-DD.")
        self._returned_date = return_date
        return f"Book '{self._book}' returned by {self._user} on {return_date}."

    # ----------------------- Static Utility Methods -----------------------

    @staticmethod
    def automated_overdue_notifications(loans: List[Dict], today: str) -> List[str]:
        """
        Create overdue messages for all unreturned loans past their due date.

        Args:
            loans (List[Dict]): List of loan records.
            today (str): Today's date ("YYYY-MM-DD").

        Returns:
            List[str]: Messages for overdue users.
        """
        messages = []
        today_date = datetime.strptime(today, "%Y-%m-%d").date()

        for loan in loans:
            if loan.get("returned_date"):
                continue

            borrow_date = datetime.strptime(loan["borrow_date"], "%Y-%m-%d").date()
            loan_days = int(loan.get("loan_days", 14))
            due = borrow_date + timedelta(days=loan_days)

            if today_date > due:
                days_late = (today_date - due).days
                msg = (
                    f"[OVERDUE] Hi {loan['user']}, your book '{loan['book']}' "
                    f"was due on {due.strftime('%Y-%m-%d')} and is {days_late} day(s) late. "
                    f"Please return it as soon as possible. (Loan ID: {loan['loan_id']})"
                )
                messages.append(msg)

        return messages

    @staticmethod
    def generate_borrowing_report(loans: List[Dict], today: str) -> Dict:
        """
        Summarize all loan activity as of today.

        Args:
            loans (List[Dict]): List of loan dictionaries.
            today (str): Today's date ("YYYY-MM-DD").

        Returns:
            Dict: Summary with counts and text.
        """
        today_date = datetime.strptime(today, "%Y-%m-%d").date()
        total = len(loans)
        returned = 0
        active = 0
        overdue = 0

        for loan in loans:
            if loan.get("returned_date"):
                returned += 1
                continue

            active += 1
            borrow_date = datetime.strptime(loan["borrow_date"], "%Y-%m-%d").date()
            loan_days = int(loan.get("loan_days", 14))
            due = borrow_date + timedelta(days=loan_days)

            if today_date > due:
                overdue += 1

        summary = (
            f"Total loans: {total}\n"
            f"Active (not returned): {active}\n"
            f"Returned: {returned}\n"
            f"Overdue: {overdue}\n"
            f"Report date: {today}"
        )

        return {
            "total_loans": total,
            "active_loans": active,
            "returned_loans": returned,
            "overdue_loans": overdue,
            "summary_text": summary
        }

    # ----------------------- Representation Methods -----------------------

    def __str__(self):
        due = self.calculate_due_date()
        status = "Returned" if self._returned_date else "Active"
        return f"[{self._loan_id}] {self._book} borrowed by {self._user} | Due: {due} | Status: {status}"

    def __repr__(self):
        return f"Loan(loan_id='{self._loan_id}', user='{self._user}', book='{self._book}', borrow_date='{self._borrow_date}', loan_days={self._loan_days})"
