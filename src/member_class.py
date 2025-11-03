from library_functions import user_account, check_in_out_operations, member_count

class Member:
    """Represents a library member and account actions."""
    
    def __init__(self, member_id: str, name: str, email: str, active: bool = True):
        """Initialize a Member."""
        if not member_id.strip():
            raise ValueError("Member ID cannot be empty.")
        if not name.strip():
            raise ValueError("Member name cannot be empty.")
        if "@" not in email:
            raise ValueError("Invalid email address.")
        
        self._member_id = member_id
        self._name = name
        self._email = email
        self._active = active
    
    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def active(self):
        return self._active

    # -------------------------------
    # Methods (Integrated)
    # -------------------------------
    def validate_account(self):
        """Validate member account using user_account()."""
        return user_account(action="validate", user_id=self._member_id)

    def borrow_book(self, isbn: str):
        """Borrow a book."""
        result = check_in_out_operations(self._member_id, isbn, action="borrow")
        return f"{self._name} borrowed {isbn}, due {result['due_at'].date()}"

    def return_book(self, isbn: str):
        """Return a borrowed book."""
        result = check_in_out_operations(self._member_id, isbn, action="return")
        return f"{self._name} returned {isbn} on {result['returned_at'].date()}"

    def pay_balance(self, amount):
        """Pay a fine or balance using user_account()."""
        return user_account(action="pay", user_id=self._member_id, pay_amount=amount)

    @staticmethod
    def total_active_members():
        """Return total count of active members."""
        return member_count(active_only=True)
    
    def __str__(self):
        return f"{self._name} ({self._email}) - Active: {self._active}"
