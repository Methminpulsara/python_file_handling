# repository.py
from abc import ABC, abstractmethod
from typing import List, Dict, Type

from library_system.models import Member
from models import Book, Member, Loan


class BookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None: pass

    @abstractmethod
    def get_by_id(self, book_id) -> Book: pass

    @abstractmethod
    def update_book(self, book: Book) -> None: pass

    @abstractmethod
    def get_all_books(self) -> List[Book]: pass


class MemberRepository(ABC):
    @abstractmethod
    def add_member(self, member: Member) -> None: pass

    @abstractmethod
    def get_member_by_id(self, member_id) -> Member: pass

    @abstractmethod
    def get_member_list(self) -> List[Member]: pass


class LoanRepository(ABC):
    @abstractmethod
    def add_loan(self, loan: Loan) -> None: pass

    @abstractmethod
    def get_by_id(self, loan_id) -> Loan: pass

    @abstractmethod
    def update_loan(self, loan: Loan) -> None: pass

    @abstractmethod
    def get_all_loans(self) -> List[Loan]: pass


# In-memory implementations
class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.__books: Dict[str, Book] = {}

    def get_by_id(self, book_id) -> Book:
        return self.__books.get(book_id)

    def update_book(self, book: Book) -> None:
        self.__books[book.book_id] = book

    def get_all_books(self) -> List[Book]:
        return list(self.__books.values())

    def add_book(self, book: Book) -> None:
        self.__books[book.book_id] = book


class InMemoryMemberRepository(MemberRepository):
    def __init__(self):
        self.members: Dict[str, Member] = {}

    def add_member(self, member: Member) -> None:
        self.members[member.member_id] = member

    def get_member_by_id(self, member_id) -> Member:
        return self.members.get(member_id)

    def get_member_list(self) -> List[Member]:
        return list(self.members.values())


class InMemoryLoanRepository(LoanRepository):
    def __init__(self):
        self.loans: Dict[str, Loan] = {}

    def add_loan(self, loan: Loan) -> None:
        self.loans[loan.loan_id] = loan

    def get_by_id(self, loan_id) -> Loan:
        return self.loans.get(loan_id)

    def update_loan(self, loan: Loan) -> None:
        self.loans[loan.loan_id] = loan

    def get_all_loans(self) -> List[Loan]:
        return list(self.loans.values())


class FileSaveBookRepository(BookRepository):

    def __init__(self, filename: str = "book.txt"):
        self.file_name = filename

    def __save_books(self, books: Dict[str, Book]):
        with open(self.file_name, "w") as data:
            for key, book in books.items():
                data.write(f"{key} | {book.title} | {book.author} | {book.year}\n")

    def __load_books(self) -> Dict[str, Book]:
        books = Dict[str, Book]
        with open(self.file_name, "r") as book_file:
            for book in book_file:
                book = book.strip("")
                data = book.split("|")
                if len(data) == 5:
                    book_id, tittle, author, year, book_len_mem_id = data
                    books[book_id] = Book(
                        book_id=book_id,
                        author=author,
                        title=tittle,
                        year=year,
                        book_lend_mem_id=None if "None" in book_len_mem_id else book_len_mem_id,
                    )
        return books

    def add_book(self, book: Book) -> None:
        books: Dict[str, Book] = self.__load_books()
        books[book.book_id] = book
        self.__save_books()

    def get_by_id(self, book_id) -> Book:
        books = self.__load_books()
        return books.get(book_id)

    def update_book(self, book: Book) -> None:
        books: Dict[str, Book] = self.__load_books()
        books[book.book_id] = book
        self.__save_books()

    def get_all_books(self) -> List[Book]:
        books = Dict[str, Book] = self.__load_books()
        return list(books.values())


class FileSavaMemberRepository(MemberRepository):

    def __init__(self, filename: str = "member.txt"):
        self.filename = filename

    def _save_member(self, members: Dict[str:Member]):
        with open(self.filename, "w") as data:
            for key, member in members.items():
                data.write(f"{key} | {data.name}")

    def __load_member(self) -> Dict[str, Member]:
        members = Dict[str, Member]
        with open(self.filename, "r") as member_file:
            for member in member_file:
                member = member.strip("")
                data = member.split("|")
                if len(data) == 2:
                    member_id, name = data
                    members[member.me] = Member(
                        member_id=member_id,
                        name=name
                    )
        return members

    def add_member(self, member: Member) -> None:
        members: Dict[str:Member] = self.__load_member()
        members[member.member_id] = member
        self._save_member()

    def get_member_by_id(self, member_id) -> Member:
        members = self.__load_member()
        return members.get(member_id)

    def get_member_list(self) -> List[Member]:
        members = Dict[str, Book] = self.__load_member()
        return list(members.values())
