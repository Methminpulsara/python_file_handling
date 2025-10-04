# library_service.py
from dataclasses import dataclass
from repository import BookRepository, MemberRepository, LoanRepository
from models import Book, Member

class LibraryException(Exception):
    pass

@dataclass
class LibraryService:
    books: BookRepository
    member: MemberRepository
    loan: LoanRepository

    def add_book(self, book_id: str, title: str, author: str, year: str) -> Book:
        if self.books.get_by_id(book_id) is not None:
            raise LibraryException("Book already exists")
        book = Book(book_id, title, author, year)
        self.books.add_book(book)
        return book

    def add_member(self, member_id: str, name: str) -> Member:
        if self.member.get_member_by_id(member_id) is not None:
            raise LibraryException("Member already exists")
        user = Member(member_id, name)
        self.member.add_member(user)
        return user

    def list_all_books(self):
        return self.books.get_all_books()
