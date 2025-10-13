# Main function library
from datetime import datetime, timedelta

class LibraryClass:
    def __init__(self):
        self.catalog = [] # list of {"id","title","author","genre","copies_total","copies_available"}
        self.members = {} # dict of member_id: {"name","email","phone"}
        self.reminders = [] # list of {"member_id","book_id","due_date", "message"}
        self.loans = [] # list of {"member_id","book_id","loan_date","due_date", "returneed": bool}


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

        

