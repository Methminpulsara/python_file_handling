# main.py
from library_service import LibraryService
from repository import InMemoryBookRepository, InMemoryMemberRepository, InMemoryLoanRepository , FileSaveBookRepository
from models import Book, Member, Loan
from typing import List
from datetime import datetime

# Service with in-memory repositories
library_service = LibraryService(
    books=FileSaveBookRepository(),
    member=InMemoryMemberRepository(),
    loan=InMemoryLoanRepository()
)


# ---------- Utility Printers ----------
def print_header(title: str):
    print("\n" + "=" * 50)
    print(f"📚 {title}")
    print("=" * 50)


def print_error(message: str):
    print(f"❌ {message}")


def print_success(message: str):
    print(f"✅ {message}")


# ---------- Library Operations ----------
def list_books():
    print_header("All Books")
    books: List[Book] = library_service.list_all_books()
    if not books:
        print("No books available.")
        return

    for book in books:
        status = "🟢 Available" if book.is_available() else f"🔴 Borrowed by {book.book_lend_mem_id}"
        print(f"[{book.book_id}] {book.title} by {book.author} ({book.year}) - {status}")


def add_book():
    print_header("Add a New Book")
    book_id = input("Enter Book ID: ").strip()
    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    year = input("Enter Year: ").strip()

    try:
        library_service.add_book(book_id=book_id, title=title, author=author, year=year)
        print_success("Book added successfully!")
    except Exception as e:
        print_error(str(e))


def add_member():
    print_header("Add a New Member")
    member_id = input("Enter Member ID: ").strip()
    name = input("Enter Member Name: ").strip()

    try:
        library_service.add_member(member_id, name)
        print_success("Member added successfully!")
    except Exception as e:
        print_error(str(e))


def list_members():
    print_header("All Members")
    members: List[Member] = library_service.member.get_member_list()
    if not members:
        print("No members registered.")
        return

    for member in members:
        print(f"[{member.member_id}] {member.name}")


def borrow_book():
    print_header("Borrow a Book")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()

    member = library_service.member.get_member_by_id(member_id)
    book = library_service.books.get_by_id(book_id)

    if member is None:
        return print_error("Member not found!")
    if book is None:
        return print_error("Book not found!")
    if not book.is_available():
        return print_error("Book is already borrowed!")

    loan_id = f"{member_id}-{book_id}-{int(datetime.now().timestamp())}"
    loan = Loan(loan_id, member_id, book_id, datetime.now())
    library_service.loan.add_loan(loan)

    book.book_lend_mem_id = member_id
    library_service.books.update_book(book)

    print_success(f"Book '{book.title}' borrowed by {member.name}. Loan ID: {loan_id}")


def return_book():
    print_header("Return a Book")
    loan_id = input("Enter Loan ID: ").strip()

    loan = library_service.loan.get_by_id(loan_id)
    if loan is None:
        return print_error("Loan not found!")
    if not loan.is_active():
        return print_error("This book has already been returned!")

    loan.returned_at = datetime.now()
    library_service.loan.update_loan(loan)

    book = library_service.books.get_by_id(loan.book_id)
    if book:
        book.book_lend_mem_id = None
        library_service.books.update_book(book)

    print_success(f"Book '{book.title}' returned successfully!")


def list_loans():
    print_header("All Loans")
    loans: List[Loan] = library_service.loan.get_all_loans()
    if not loans:
        print("No loans found.")
        return

    for loan in loans:
        status = "⏳ Active" if loan.is_active() else f"✅ Returned at {loan.returned_at}"
        print(f"[{loan.loan_id}] Book: {loan.book_id}, Member: {loan.member_id}, Borrowed: {loan.borrowed_at}, Status: {status}")


# ---------- Menu Loop ----------
while True:
    print_header("Library Management System")
    print("1. 📖 List all books")
    print("2. ➕ Add a book")
    print("3. 🧑 Add a member")
    print("4. 👥 List members")
    print("5. 📚 Borrow a book")
    print("6. 🔄 Return a book")
    print("7. 📝 List all loans")
    print("0. 🚪 Exit")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        list_books()
    elif choice == "2":
        add_book()
    elif choice == "3":
        add_member()
    elif choice == "4":
        list_members()
    elif choice == "5":
        borrow_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        list_loans()
    elif choice == "0":
        print("\n👋 Goodbye! See you again!")
        break
    else:
        print_error("Invalid choice, try again.")
