# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    book_id: str
    title: str
    author: str
    year: str
    book_lend_mem_id: Optional[str] = None

    def is_available(self):
        return self.book_lend_mem_id is None


@dataclass
class Member:
    member_id: str
    name: str


@dataclass
class Loan:
    loan_id: str
    member_id: str
    book_id: str
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    def is_active(self):
        return self.returned_at is None
