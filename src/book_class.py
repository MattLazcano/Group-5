class Book:
    """
    Represents a book in the library system.
    """

    def __init__(self, book_id, title, author, code_input, available=True, rating=None):
        """
        Initialize a new Book object with validation.

        Args:
            book_id (str): Unique ID for the book.
            title (str): Book title.
            author (str): Author's name.
            code_input (str): ISBN or product code to validate.
            available (bool): True if the book is available.
            rating (float): Optional initial rating.
        """
        if not isinstance(book_id, str) or not book_id.strip():
            raise ValueError("Book ID must be a non-empty string.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title must be a non-empty string.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author name must be a non-empty string.")

        # Use your original validation logic
        if not self.validate_code(code_input):
            raise ValueError("Invalid ISBN or code format.")
        
        self._book_id = book_id.strip().upper()
        self._title = title.strip().title()
        self._author = author.strip().title()
        self._code = code_input.replace("-", "").replace(" ", "").upper()
        self._available = available
        self._rating = rating if rating is not None else 0.0
        self._rating_count = 0

    # ----------------------- Properties -----------------------
    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def code(self):
        return self._code

    @property
    def available(self):
        return self._available

    @property
    def rating(self):
        return round(self._rating, 2)

    # ----------------------- Instance Methods -----------------------

    def is_book_available(self):
        """Check if the book is currently available."""
        return self._available

    def checkout(self):
        """Mark the book as checked out if available."""
        if not self._available:
            raise RuntimeError(f"Book '{self._title}' is already checked out.")
        self._available = False
        return f"'{self._title}' checked out successfully."

    def return_book(self):
        """Mark the book as returned."""
        self._available = True
        return f"'{self._title}' returned and now available."

    def rate_book(self, rating):
        """Add a user rating between 0 and 5."""
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        total_score = self._rating * self._rating_count + rating
        self._rating_count += 1
        self._rating = total_score / self._rating_count
        return f"New rating added. Current average: {self._rating:.2f}"

    # ----------------------- Original Validation Functions -----------------------

    def validate_code(self, code_input):
        """Validate a book's ISBN or code using the same logic as in Project 1."""
        if not isinstance(code_input, str):
            raise TypeError("Code must be a string.")

        cleaned_code = code_input.replace("-", "").replace(" ", "").upper()
        code_length = len(cleaned_code)

        if code_length == 10:
            first_nine = cleaned_code[:-1]
            last_char = cleaned_code[-1]
            if first_nine.isdigit() and (last_char.isdigit() or last_char == 'X'):
                return self.validate_isbn10_format(cleaned_code)

        elif code_length == 13 and cleaned_code.isdigit():
            return self.validate_isbn13_format(cleaned_code)

        elif 6 <= code_length <= 20:
            return cleaned_code.isalnum()
        else:
            return False

    def validate_isbn10_format(self, isbn_code):
        """Validate ISBN-10 using checksum algorithm."""
        checksum = 0
        position = 10
        for char in isbn_code:
            digit_value = 10 if char == 'X' else int(char)
            checksum += digit_value * position
            position -= 1
        return checksum % 11 == 0

    def validate_isbn13_format(self, isbn_code):
        """Validate ISBN-13 using checksum algorithm."""
        total_sum = 0
        for index in range(len(isbn_code)):
            current_digit = int(isbn_code[index])
            weight = 1 if index % 2 == 0 else 3
            total_sum += current_digit * weight
        return total_sum % 10 == 0

    # ----------------------- Representation Methods -----------------------

    def __str__(self):
        status = "Available" if self._available else "Checked out"
        return f"[{self._book_id}] {self._title} by {self._author} | Rating: {self._rating:.1f} | {status}"

    def __repr__(self):
        return f"Book({self._book_id}, {self._title}, {self._author}, {self._code})"


