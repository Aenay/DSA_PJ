import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import string
import datetime

# Data structure 1: Binary Search Tree for books
class BookNode:
    def __init__(self, book_id, title, author, genre, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        self.checkout_user = None
        self.due_date = None
        self.left = None
        self.right = None

class BookBST:
    def __init__(self):
        self.root = None
        self.books_list = []  # For easy traversal
    
    def insert(self, book_id, title, author, genre):
        # Best Case O(log n)
        # Worst Case o(n)
        if self.root is None:
            self.root = BookNode(book_id, title, author, genre)
            self.books_list.append(self.root)
            return
        
        self._insert_recursive(self.root, book_id, title, author, genre)
    
    def _insert_recursive(self, node, book_id, title, author, genre):
        if book_id < node.book_id:
            if node.left is None:
                node.left = BookNode(book_id, title, author, genre)
                self.books_list.append(node.left)
            else:
                self._insert_recursive(node.left, book_id, title, author, genre)
        else:
            if node.right is None:
                node.right = BookNode(book_id, title, author, genre)
                self.books_list.append(node.right)
            else:
                self._insert_recursive(node.right, book_id, title, author, genre)
    
    def search(self, book_id):
        # Best Case O(log n)
        # Worst Case o(n)
        return self._search_recursive(self.root, book_id)
    
    def _search_recursive(self, node, book_id):
        if node is None:
            return None
        
        if node.book_id == book_id:
            return node
        
        if book_id < node.book_id:
            return self._search_recursive(node.left, book_id)
        else:
            return self._search_recursive(node.right, book_id)
    
    def search_by_title(self, title):
        # O(n)
        results = []
        for book in self.books_list:
            if title.lower() in book.title.lower():
                results.append(book)
        return results
    
    def get_all_books(self):
        return self.books_list

# Data structure 2: Hash Table for users
class UserHashTable:
    # Best Case O(1)
    # Worst Case O(n)
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.num_users = 0
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, user_id, name, email):
        index = self._hash(user_id)
        for i, (id, _, _) in enumerate(self.table[index]):
            if id == user_id:
                self.table[index][i] = (user_id, name, email)
                return
    
        self.table[index].append((user_id, name, email))
        self.num_users += 1
        
        # Resize if load factor exceeds 0.7
        if self.num_users > 0.7 * self.size:
            self._resize(self.size * 2)
    
    def get(self, user_id):
        index = self._hash(user_id)
        for id, name, email in self.table[index]:
            if id == user_id:
                return (id, name, email)
        return None
    
    def remove(self, user_id):
        index = self._hash(user_id)
        for i, (id, _, _) in enumerate(self.table[index]):
            if id == user_id:
                del self.table[index][i]
                self.num_users -= 1
                return True
        return False
    
    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        self.num_users = 0
        
        for bucket in old_table:
            for user_id, name, email in bucket:
                self.insert(user_id, name, email)
    
    def get_all_users(self):
        all_users = []
        for bucket in self.table:
            for user in bucket:
                all_users.append(user)
        return all_users

# Algorithm 1: Quick Sort for book sorting
def quick_sort_books(books, key_func):
    # O(n log n) Best Case
    # O(n**2) Worst Case
    if len(books) <= 1:
        return books
    
    pivot = books[len(books) // 2]
    pivot_key = key_func(pivot)
    
    left = [book for book in books if key_func(book) < pivot_key]
    middle = [book for book in books if key_func(book) == pivot_key]
    right = [book for book in books if key_func(book) > pivot_key]
    
    return quick_sort_books(left, key_func) + middle + quick_sort_books(right, key_func)

# Algorithm 2: Binary Search for finding books
def binary_search_books(sorted_books, target, key_func):
    # Best Case O(log n)
    # Worst Case O(n)
    if not sorted_books:
        return []
    
    left, right = 0, len(sorted_books) - 1
    
    # Find leftmost occurrence
    first_occurrence = -1
    while left <= right:
        mid = (left + right) // 2
        mid_key = key_func(sorted_books[mid])
        
        if mid_key == target:
            first_occurrence = mid
            right = mid - 1
        elif mid_key < target:
            left = mid + 1
        else:
            right = mid - 1
    
    if first_occurrence == -1:
        return []
    
    # Find all matching books (since we might have multiple books with same key)
    results = []
    for i in range(first_occurrence, len(sorted_books)):
        if key_func(sorted_books[i]) == target:
            results.append(sorted_books[i])
        else:
            break
    
    return results

# Generate book data
def generate_books(num_books=100):
    books_bst = BookBST()
    
    genres = ["Fiction", "Science Fiction", "Mystery", "Romance", "Fantasy", 
              "Biography", "History", "Self-Help", "Technology", "Philosophy"]
    
    # List of 100 common book titles and authors
    book_titles = [
        "The Great Gatsby", "To Kill a Mockingbird", "1984", "Pride and Prejudice",
        "The Catcher in the Rye", "Animal Farm", "Lord of the Flies", "The Hobbit",
        "Brave New World", "The Alchemist", "The Odyssey", "Moby Dick",
        "War and Peace", "Crime and Punishment", "The Brothers Karamazov",
        "The Divine Comedy", "Don Quixote", "Madame Bovary", "Lolita",
        "Anna Karenina", "The Iliad", "Les Misérables", "One Hundred Years of Solitude",
        "The Road", "The Sound and the Fury", "Ulysses", "Wuthering Heights",
        "Jane Eyre", "Great Expectations", "David Copperfield", "Oliver Twist",
        "A Tale of Two Cities", "The Picture of Dorian Gray", "Dracula",
        "Frankenstein", "The Time Machine", "Heart of Darkness", "The Jungle Book",
        "The Call of the Wild", "The Old Man and the Sea", "For Whom the Bell Tolls",
        "The Sun Also Rises", "A Farewell to Arms", "The Count of Monte Cristo",
        "The Three Musketeers", "The Scarlet Letter", "Moby-Dick", "The Adventures of Tom Sawyer",
        "The Adventures of Huckleberry Finn", "The Red Badge of Courage", "Invisible Man",
        "Beloved", "Catch-22", "Slaughterhouse-Five", "The Grapes of Wrath",
        "East of Eden", "Of Mice and Men", "The Bell Jar", "The Color Purple",
        "Their Eyes Were Watching God", "The Handmaid's Tale", "The Lord of the Rings",
        "Harry Potter and the Philosopher's Stone", "Dune", "Foundation",
        "Neuromancer", "The Hitchhiker's Guide to the Galaxy", "Ender's Game",
        "The Chronicles of Narnia", "A Game of Thrones", "The Hunger Games",
        "Fahrenheit 451", "The Little Prince", "Charlotte's Web", "Alice's Adventures in Wonderland",
        "The Wind in the Willows", "Charlie and the Chocolate Factory", "Matilda",
        "The Very Hungry Caterpillar", "Where the Wild Things Are", "Green Eggs and Ham",
        "The Cat in the Hat", "Goodnight Moon", "The Giving Tree", "Oh, the Places You'll Go!",
        "The Tale of Peter Rabbit", "The Velveteen Rabbit", "Winnie-the-Pooh",
        "Anne of Green Gables", "Little Women", "The Secret Garden", "The Wonderful Wizard of Oz",
        "Peter Pan", "A Wrinkle in Time", "Bridge to Terabithia", "The Giver"
    ]
    
    authors = [
        "F. Scott Fitzgerald", "Harper Lee", "George Orwell", "Jane Austen",
        "J.D. Salinger", "George Orwell", "William Golding", "J.R.R. Tolkien",
        "Aldous Huxley", "Paulo Coelho", "Homer", "Herman Melville",
        "Leo Tolstoy", "Fyodor Dostoevsky", "Fyodor Dostoevsky",
        "Dante Alighieri", "Miguel de Cervantes", "Gustave Flaubert", "Vladimir Nabokov",
        "Leo Tolstoy", "Homer", "Victor Hugo", "Gabriel García Márquez",
        "Cormac McCarthy", "William Faulkner", "James Joyce", "Emily Brontë",
        "Charlotte Brontë", "Charles Dickens", "Charles Dickens", "Charles Dickens",
        "Charles Dickens", "Oscar Wilde", "Bram Stoker",
        "Mary Shelley", "H.G. Wells", "Joseph Conrad", "Rudyard Kipling",
        "Jack London", "Ernest Hemingway", "Ernest Hemingway",
        "Ernest Hemingway", "Ernest Hemingway", "Alexandre Dumas",
        "Alexandre Dumas", "Nathaniel Hawthorne", "Herman Melville", "Mark Twain",
        "Mark Twain", "Stephen Crane", "Ralph Ellison",
        "Toni Morrison", "Joseph Heller", "Kurt Vonnegut", "John Steinbeck",
        "John Steinbeck", "John Steinbeck", "Sylvia Plath", "Alice Walker",
        "Zora Neale Hurston", "Margaret Atwood", "J.R.R. Tolkien",
        "J.K. Rowling", "Frank Herbert", "Isaac Asimov",
        "William Gibson", "Douglas Adams", "Orson Scott Card",
        "C.S. Lewis", "George R.R. Martin", "Suzanne Collins",
        "Ray Bradbury", "Antoine de Saint-Exupéry", "E.B. White", "Lewis Carroll",
        "Kenneth Grahame", "Roald Dahl", "Roald Dahl",
        "Eric Carle", "Maurice Sendak", "Dr. Seuss",
        "Dr. Seuss", "Margaret Wise Brown", "Shel Silverstein", "Dr. Seuss",
        "Beatrix Potter", "Margery Williams", "A.A. Milne",
        "L.M. Montgomery", "Louisa May Alcott", "Frances Hodgson Burnett", "L. Frank Baum",
        "J.M. Barrie", "Madeleine L'Engle", "Katherine Paterson", "Lois Lowry"
    ]
    
    # Generating a mix of predefined and random books
    for i in range(min(num_books, len(book_titles))):
        books_bst.insert(
            i + 1,
            book_titles[i],
            authors[i],
            random.choice(genres)
        )
    
    # If more than 100 books are requested, generate random ones
    for i in range(len(book_titles), num_books):
        random_title = "Book " + ''.join(random.choices(string.ascii_uppercase, k=3)) + "-" + str(i)
        random_author = "Author " + ''.join(random.choices(string.ascii_uppercase, k=2))
        books_bst.insert(
            i + 1,
            random_title,
            random_author,
            random.choice(genres)
        )
    
    return books_bst

# User data generator
def generate_users(num_users=20):
    users = UserHashTable()
    
    first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Jessica", "William", "Jennifer"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    
    for i in range(1, num_users + 1):
        if i <= 10:
            name = f"{first_names[i-1]} {last_names[i-1]}"
        else:
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        email = f"{name.lower().replace(' ', '.')}@email.com"
        users.insert(i, name, email)
    
    return users

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Initialize data structures
        self.books = generate_books(120)  # Generate 120 books
        self.users = generate_users(20)   # Generate 20 users
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.books_tab = ttk.Frame(self.notebook)
        self.users_tab = ttk.Frame(self.notebook)
        self.checkout_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.books_tab, text='Books Management')
        self.notebook.add(self.users_tab, text='Users Management')
        self.notebook.add(self.checkout_tab, text='Checkout/Return')
        
        # Setup each tab
        self.setup_books_tab()
        self.setup_users_tab()
        self.setup_checkout_tab()
    
    def setup_books_tab(self):
        # Left frame for book list
        list_frame = ttk.Frame(self.books_tab)
        list_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Search frame at the top
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.book_search_var = tk.StringVar()
        self.book_search_entry = ttk.Entry(search_frame, textvariable=self.book_search_var)
        self.book_search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side='left', padx=5)
        
        # Sorting options
        sort_frame = ttk.Frame(list_frame)
        sort_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side='left', padx=5)
        self.sort_by_var = tk.StringVar(value="ID")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_by_var, 
                                  values=["ID", "Title", "Author", "Genre"])
        sort_combo.pack(side='left', padx=5)
        sort_combo.bind("<<ComboboxSelected>>", lambda e: self.sort_books())
        
        # Book treeview
        self.book_tree = ttk.Treeview(list_frame, columns=("ID", "Title", "Author", "Genre", "Status"))
        self.book_tree.heading("ID", text="ID")
        self.book_tree.heading("Title", text="Title")
        self.book_tree.heading("Author", text="Author")
        self.book_tree.heading("Genre", text="Genre")
        self.book_tree.heading("Status", text="Status")
        
        self.book_tree.column("#0", width=0, stretch=tk.NO)
        self.book_tree.column("ID", width=50)
        self.book_tree.column("Title", width=200)
        self.book_tree.column("Author", width=150)
        self.book_tree.column("Genre", width=100)
        self.book_tree.column("Status", width=100)
        
        self.book_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.book_tree.bind("<Double-1>", self.view_book_details)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        # Right frame for actions
        action_frame = ttk.Frame(self.books_tab, width=200)
        action_frame.pack(side='right', fill='y', padx=5, pady=5)
        
        ttk.Label(action_frame, text="Book Management", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Button(action_frame, text="Add New Book", command=self.add_book_dialog).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="View Selected Book", command=lambda: self.view_book_details(None)).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="Delete Selected Book", command=self.delete_book).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="Refresh List", command=self.refresh_books_list).pack(fill='x', pady=5)
        
        # Load initial data
        self.refresh_books_list()
    
    def setup_users_tab(self):
        # Left frame for user list
        list_frame = ttk.Frame(self.users_tab)
        list_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # User treeview
        self.user_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Email"))
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Name", text="Name")
        self.user_tree.heading("Email", text="Email")
        
        self.user_tree.column("#0", width=0, stretch=tk.NO)
        self.user_tree.column("ID", width=50)
        self.user_tree.column("Name", width=150)
        self.user_tree.column("Email", width=200)
        
        self.user_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.user_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        # Right frame for actions
        action_frame = ttk.Frame(self.users_tab, width=200)
        action_frame.pack(side='right', fill='y', padx=5, pady=5)
        
        ttk.Label(action_frame, text="User Management", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Button(action_frame, text="Add New User", command=self.add_user_dialog).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="View User Books", command=self.view_user_books).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="Delete Selected User", command=self.delete_user).pack(fill='x', pady=5)
        ttk.Button(action_frame, text="Refresh List", command=self.refresh_users_list).pack(fill='x', pady=5)
        
        # Load initial data
        self.refresh_users_list()
    
    def setup_checkout_tab(self):
        main_frame = ttk.Frame(self.checkout_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Book selection
        book_frame = ttk.LabelFrame(main_frame, text="Book Selection")
        book_frame.pack(fill='x', pady=10)
        
        ttk.Label(book_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.checkout_book_id = tk.StringVar()
        ttk.Entry(book_frame, textvariable=self.checkout_book_id).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        ttk.Button(book_frame, text="Find Book", command=self.find_book_for_checkout).grid(row=0, column=2, padx=5, pady=5)
        
        self.book_info_label = ttk.Label(book_frame, text="No book selected")
        self.book_info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        # User selection
        user_frame = ttk.LabelFrame(main_frame, text="User Selection")
        user_frame.pack(fill='x', pady=10)
        
        ttk.Label(user_frame, text="User ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.checkout_user_id = tk.StringVar()
        ttk.Entry(user_frame, textvariable=self.checkout_user_id).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        ttk.Button(user_frame, text="Find User", command=self.find_user_for_checkout).grid(row=0, column=2, padx=5, pady=5)
        
        self.user_info_label = ttk.Label(user_frame, text="No user selected")
        self.user_info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=20)
        
        ttk.Button(action_frame, text="Checkout Book", command=self.checkout_book).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Return Book", command=self.return_book).pack(side='left', padx=10)
        
        # Currently checked out books
        checkout_frame = ttk.LabelFrame(main_frame, text="Currently Checked Out Books")
        checkout_frame.pack(fill='both', expand=True, pady=10)
        
        self.checkout_tree = ttk.Treeview(checkout_frame, 
                                         columns=("Book ID", "Title", "User", "Due Date"))
        self.checkout_tree.heading("Book ID", text="Book ID")
        self.checkout_tree.heading("Title", text="Title")
        self.checkout_tree.heading("User", text="Checked Out By")
        self.checkout_tree.heading("Due Date", text="Due Date")
        
        self.checkout_tree.column("#0", width=0, stretch=tk.NO)
        self.checkout_tree.column("Book ID", width=50)
        self.checkout_tree.column("Title", width=200)
        self.checkout_tree.column("User", width=150)
        self.checkout_tree.column("Due Date", width=100)
        
        self.checkout_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load initial checkout data
        self.refresh_checkout_list()
    
    def refresh_books_list(self):
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # Sort books based on the selected criteria
        self.sort_books()
    
    def sort_books(self):
        sort_by = self.sort_by_var.get()
        all_books = self.books.get_all_books()
        
        if sort_by == "ID":
            sorted_books = quick_sort_books(all_books, lambda book: book.book_id)
        elif sort_by == "Title":
            sorted_books = quick_sort_books(all_books, lambda book: book.title.lower())
        elif sort_by == "Author":
            sorted_books = quick_sort_books(all_books, lambda book: book.author.lower())
        elif sort_by == "Genre":
            sorted_books = quick_sort_books(all_books, lambda book: book.genre.lower())
        
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # Insert sorted books
        for book in sorted_books:
            status = "Available" if book.available else "Checked Out"
            self.book_tree.insert("", "end", values=(book.book_id, book.title, book.author, book.genre, status))
    
    def search_books(self):
        search_term = self.book_search_var.get().strip()
        if not search_term:
            self.refresh_books_list()
            return
        
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        all_books = self.books.get_all_books()
        
        # First try exact ID search
        try:
            book_id = int(search_term)
            book = self.books.search(book_id)
            if book:
                status = "Available" if book.available else "Checked Out"
                self.book_tree.insert("", "end", values=(book.book_id, book.title, book.author, book.genre, status))
                return
        except ValueError:
            pass
        
        # Search by title
        for book in all_books:
            if (search_term.lower() in book.title.lower() or 
                search_term.lower() in book.author.lower() or
                search_term.lower() in book.genre.lower()):
                status = "Available" if book.available else "Checked Out"
                self.book_tree.insert("", "end", values=(book.book_id, book.title, book.author, book.genre, status))
    
    def add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add New Book", font=("Arial", 12, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=author_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Genre:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        genre_var = tk.StringVar()
        genre_combo = ttk.Combobox(form_frame, textvariable=genre_var, width=28, 
                                   values=["Fiction", "Science Fiction", "Mystery", "Romance", 
                                           "Fantasy", "Biography", "History", "Self-Help", 
                                           "Technology", "Philosophy"])
        genre_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        def add_book():
            title = title_var.get().strip()
            author = author_var.get().strip()
            genre = genre_var.get().strip()
            
            if not title or not author or not genre:
                messagebox.showerror("Error", "All fields are required!", parent=dialog)
                return
            
            # Generate new book ID (max ID + 1)
            max_id = 0
            for book in self.books.get_all_books():
                if book.book_id > max_id:
                    max_id = book.book_id
            
            new_id = max_id + 1
            
            # Add book to BST
            self.books.insert(new_id, title, author, genre)
            
            messagebox.showinfo("Success", f"Book '{title}' added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_books_list()
        
        ttk.Button(dialog, text="Add Book", command=add_book).pack(pady=20)
    def view_book_details(self, event=None):
        selected_items = self.book_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a book to view.")
            return
        
        selected_item = selected_items[0]
        book_id = int(self.book_tree.item(selected_item, "values")[0])
        
        book = self.books.search(book_id)
        if book:
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Book Details: {book.title}")
            dialog.geometry("400x300")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Book Details", font=("Arial", 12, "bold")).pack(pady=10)
            
            details_frame = ttk.Frame(dialog)
            details_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            ttk.Label(details_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(details_frame, text=book.book_id).grid(row=0, column=1, padx=5, pady=5, sticky='w')
            
            ttk.Label(details_frame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(details_frame, text=book.title).grid(row=1, column=1, padx=5, pady=5, sticky='w')
            
            ttk.Label(details_frame, text="Author:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(details_frame, text=book.author).grid(row=2, column=1, padx=5, pady=5, sticky='w')
            
            ttk.Label(details_frame, text="Genre:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(details_frame, text=book.genre).grid(row=3, column=1, padx=5, pady=5, sticky='w')
            
            ttk.Label(details_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
            status = "Available" if book.available else "Checked Out"
            ttk.Label(details_frame, text=status).grid(row=4, column=1, padx=5, pady=5, sticky='w')
            
            if not book.available and book.checkout_user and book.due_date:
                user = self.users.get(book.checkout_user)
                if user:
                    ttk.Label(details_frame, text="Checked out by:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
                    ttk.Label(details_frame, text=user[1]).grid(row=5, column=1, padx=5, pady=5, sticky='w')
                
                ttk.Label(details_frame, text="Due date:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
                ttk.Label(details_frame, text=book.due_date.strftime("%Y-%m-%d")).grid(row=6, column=1, padx=5, pady=5, sticky='w')
            
            ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def delete_book(self):
        selected_items = self.book_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return
        
        selected_item = selected_items[0]
        book_id = int(self.book_tree.item(selected_item, "values")[0])
        
        book = self.books.search(book_id)
        if book:
            if not book.available:
                messagebox.showerror("Error", "Cannot delete book that is currently checked out!")
                return
            
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{book.title}'?")
            if confirm:
                # For simplicity, we'll just mark it as unavailable
                book.available = False
                
                # Remove it from the books_list for display purposes
                self.books.books_list = [b for b in self.books.books_list if b.book_id != book_id]
                
                messagebox.showinfo("Success", f"Book '{book.title}' deleted successfully!")
                self.refresh_books_list()
    
    def refresh_users_list(self):
        # Clear existing items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get all users
        all_users = self.users.get_all_users()
        
        # Sort users by ID
        all_users.sort(key=lambda user: user[0])
        
        # Insert users into treeview
        for user_id, name, email in all_users:
            self.user_tree.insert("", "end", values=(user_id, name, email))
    
    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add New User", font=("Arial", 12, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=email_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        def add_user():
            name = name_var.get().strip()
            email = email_var.get().strip()
            
            if not name or not email:
                messagebox.showerror("Error", "All fields are required!", parent=dialog)
                return
            
            # Generate new user ID (max ID + 1)
            max_id = 0
            for user_id, _, _ in self.users.get_all_users():
                if user_id > max_id:
                    max_id = user_id
            
            new_id = max_id + 1
            
            # Add user to hash table
            self.users.insert(new_id, name, email)
            
            messagebox.showinfo("Success", f"User '{name}' added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_users_list()
        
        ttk.Button(dialog, text="Add User", command=add_user).pack(pady=20)
    
    def view_user_books(self):
        selected_items = self.user_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a user to view checked out books.")
            return
        
        selected_item = selected_items[0]
        user_id = int(self.user_tree.item(selected_item, "values")[0])
        
        user = self.users.get(user_id)
        if not user:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Books Checked Out by {user[1]}")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Books Checked Out by {user[1]}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Create treeview for books
        tree = ttk.Treeview(dialog, columns=("ID", "Title", "Due Date"))
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Due Date", text="Due Date")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", width=50)
        tree.column("Title", width=300)
        tree.column("Due Date", width=100)
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Find books checked out by this user
        found_books = False
        for book in self.books.get_all_books():
            if not book.available and book.checkout_user == user_id:
                found_books = True
                tree.insert("", "end", values=(book.book_id, book.title, book.due_date.strftime("%Y-%m-%d")))
        
        if not found_books:
            ttk.Label(dialog, text="No books currently checked out by this user.").pack(pady=10)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def delete_user(self):
        selected_items = self.user_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return
        
        selected_item = selected_items[0]
        user_id = int(self.user_tree.item(selected_item, "values")[0])
        
        user = self.users.get(user_id)
        if user:
            # Check if user has books checked out
            has_books = False
            for book in self.books.get_all_books():
                if not book.available and book.checkout_user == user_id:
                    has_books = True
                    break
            
            if has_books:
                messagebox.showerror("Error", "Cannot delete user who has books checked out!")
                return
            
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user[1]}'?")
            if confirm:
                self.users.remove(user_id)
                messagebox.showinfo("Success", f"User '{user[1]}' deleted successfully!")
                self.refresh_users_list()
    
    def refresh_checkout_list(self):
        # Clear existing items
        for item in self.checkout_tree.get_children():
            self.checkout_tree.delete(item)
        
        # Find checked out books
        for book in self.books.get_all_books():
            if not book.available and book.checkout_user:
                user = self.users.get(book.checkout_user)
                if user:
                    due_date = book.due_date.strftime("%Y-%m-%d") if book.due_date else "N/A"
                    self.checkout_tree.insert("", "end", values=(book.book_id, book.title, user[1], due_date))
    
    def find_book_for_checkout(self):
        book_id_str = self.checkout_book_id.get().strip()
        if not book_id_str:
            self.book_info_label.config(text="Please enter a book ID")
            return
        
        try:
            book_id = int(book_id_str)
            book = self.books.search(book_id)
            
            if not book:
                self.book_info_label.config(text="Book not found!")
                return
            
            if not book.available:
                self.book_info_label.config(text=f"Book '{book.title}' is already checked out!")
                return
            
            self.book_info_label.config(text=f"Selected: {book.title} by {book.author}")
        except ValueError:
            self.book_info_label.config(text="Invalid book ID!")
    
    def find_user_for_checkout(self):
        user_id_str = self.checkout_user_id.get().strip()
        if not user_id_str:
            self.user_info_label.config(text="Please enter a user ID")
            return
        
        try:
            user_id = int(user_id_str)
            user = self.users.get(user_id)
            
            if not user:
                self.user_info_label.config(text="User not found!")
                return
            
            self.user_info_label.config(text=f"Selected: {user[1]} ({user[2]})")
        except ValueError:
            self.user_info_label.config(text="Invalid user ID!")
    
    def checkout_book(self):
        book_id_str = self.checkout_book_id.get().strip()
        user_id_str = self.checkout_user_id.get().strip()
        
        if not book_id_str or not user_id_str:
            messagebox.showwarning("Missing Information", "Please enter both book ID and user ID")
            return
        
        try:
            book_id = int(book_id_str)
            user_id = int(user_id_str)
            
            book = self.books.search(book_id)
            user = self.users.get(user_id)
            
            if not book or not user:
                messagebox.showerror("Error", "Book or user not found!")
                return
            
            if not book.available:
                messagebox.showerror("Error", "This book is already checked out!")
                return
            
            # Update book status
            book.available = False
            book.checkout_user = user_id
            book.due_date = datetime.datetime.now() + datetime.timedelta(days=14)  # 2 weeks
            
            messagebox.showinfo("Success", f"Book '{book.title}' checked out to {user[1]} successfully!\n"
                                         f"Due date: {book.due_date.strftime('%Y-%m-%d')}")
            
            # Clear fields and refresh lists
            self.checkout_book_id.set("")
            self.checkout_user_id.set("")
            self.book_info_label.config(text="No book selected")
            self.user_info_label.config(text="No user selected")
            self.refresh_checkout_list()
            self.refresh_books_list()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid book ID or user ID!")
    
    def return_book(self):
        book_id_str = self.checkout_book_id.get().strip()
        
        if not book_id_str:
            messagebox.showwarning("Missing Information", "Please enter book ID")
            return
        
        try:
            book_id = int(book_id_str)
            book = self.books.search(book_id)
            
            if not book:
                messagebox.showerror("Error", "Book not found!")
                return
            
            if book.available:
                messagebox.showerror("Error", "This book is not checked out!")
                return
            
            user = self.users.get(book.checkout_user)
            user_name = user[1] if user else "Unknown"
            
            # Update book status
            book.available = True
            book.checkout_user = None
            book.due_date = None
            
            messagebox.showinfo("Success", f"Book '{book.title}' returned successfully!"
                                         f"\nPreviously checked out to: {user_name}")
            
            # Clear fields and refresh lists
            self.checkout_book_id.set("")
            self.book_info_label.config(text="No book selected")
            self.refresh_checkout_list()
            self.refresh_books_list()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid book ID!")

def main():
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

lms = LibraryManagementSystem()