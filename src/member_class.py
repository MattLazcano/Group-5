from datetime import datetime, timezone
from decimal import Decimal

class Member:
    """
    Represents a library member responsible for borrowing and returning books.
    Integrates Project 1 functions for account validation and loan management.
    """

    def __init__(self, member_id: str, name: str, email: str, active: bool = True):
        """
        Initialize a Member object with validation.

        Args:
            member_id (str): Unique member ID.
            name (str): Member's full name.
            email (str): Email address.
            active (bool): Whether the account is active (default True).

        Raises:
            ValueError: If any input is invalid.
        """
        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError("Member ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name cannot be empty.")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")

        self._member_id = member_id.strip().upper()
        self._name = name.strip().title()
        self._email = email.strip().lower()
        self._active = active
        self._loans = {}        # Active and past book loans keyed by ISBN or Book ID
        self._balance = Decimal("0.00")

    # -------------------- Properties --------------------
    @property
    def member_id(self):
        """Return the member's unique ID."""
        return self._member_id

    @property
    def name(self):
        """Return the member's name."""
        return self._name

    @property
    def email(self):
        """Return the member's email."""
        return self._email

    @property
    def active(self):
        """Return whether the account is active."""
        return self._active

    @property
    def balance(self):
        """Return the member's outstanding balance."""
        return self._balance

    # -------------------- Core Methods --------------------
    def validate_member(self):
        """
        Validate that the member's account is active and information is complete.
        """
        if not self._active:
            raise ValueError(f"Member {self._member_id} account is inactive.")
        if not self._name or not self._email:
            raise ValueError("Incomplete member information.")
        return True

    def borrow_book(self, catalog: dict, isbn: str):
        """
        Borrow a book and update member loans.
        Placeholder for Project 1 function: check_in_out_operations().

        Args:
            catalog (dict): Current library catalog.
            isbn (str): Book ISBN or code.

        Returns:
            str: Confirmation message.
        """
        self.validate_member()

        # Temporary placeholder (you can uncomment once integrated)
        # result = check_in_out_operations(
        #     catalog=catalog,
        #     users={self._member_id: {"loans": self._loans, "active": self._active}},
        #     user_id=self._member_id,
        #     isbn=isbn,
        #     action="borrow"
        # )

        now = datetime.now(timezone.utc)
        due_date = now.replace(hour=23, minute=59)  # simple placeholder due date
        result = {"borrowed_at": now, "due_at": due_date, "returned_at": None}

        self._loans[isbn] = result
        return f"{self._name} borrowed {isbn}, due on {due_date.date()}"

    def return_book(self, catalog: dict, isbn: str):
        """
        Return a borrowed book and mark it as returned.

        Args:
            catalog (dict): Library catalog.
            isbn (str): Book ISBN or code.

        Returns:
            str: Confirmation message.
        """
        if isbn not in self._loans or self._loans[isbn].get("returned_at"):
            raise ValueError("This book is not currently borrowed or already returned.")

        # Placeholder for Project 1 integration
        now = datetime.now(timezone.utc)
        self._loans[isbn]["returned_at"] = now

        return f"{self._name} returned {isbn} on {now.date()}"

    def pay_balance(self, amount: Decimal):
        """Pay part or all of the member’s outstanding balance."""
        if amount <= 0:
            raise ValueError("Payment must be positive.")
        if amount > self._balance:
            amount = self._balance
        self._balance -= amount
        return f"Payment of ${amount} received. New balance: ${self._balance}"

    def add_fee(self, amount: Decimal):
        """Add a fine or overdue fee to the member’s balance."""
        if amount <= 0:
            raise ValueError("Fee must be positive.")
        self._balance += amount
        return f"Added ${amount} fee. Current balance: ${self._balance}"

    def get_loan_count(self):
        """Return the number of books currently borrowed by this member."""
        return sum(1 for record in self._loans.values() if record.get("returned_at") is None)

    # -------------------- Representations --------------------
    def __str__(self):
        status = "Active" if self._active else "Inactive"
        return f"Member: {self._name} ({self._member_id}) — {status}, Loans: {self.get_loan_count()}"

    def __repr__(self):
        return f"Member(member_id='{self._member_id}', name='{self._name}', email='{self._email}', active={self._active})"
