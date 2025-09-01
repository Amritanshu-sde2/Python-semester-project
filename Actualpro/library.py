#python Project Library Mgmt. System
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from functools import reduce
import json
import os

class LibraryManagementSystem:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.issued_books = {}
        self.categories = {'Fiction', 'Non-Fiction', 'Science', 'History', 'Technology', 'Literature'}
        self.library_rules = frozenset({
            'Maximum 3 books per member',
            '14 days loan period',
            'Late fee: $1 per day',
            'No food or drinks',
            'Quiet zone'
        })
        self.load_data()
    
    def load_data(self):
        if os.path.exists('library_data.json'):
            try:
                with open('library_data.json', 'r') as f:
                    data = json.load(f)
                    self.books = data.get('books', {})
                    self.members = data.get('members', {})
                    raw_issued_books = data.get('issued_books', {})
                    self.issued_books = {}
                    for member_id, issued_list in raw_issued_books.items():
                        self.issued_books[member_id] = []
                        for issued in issued_list:
                            issued_copy = issued.copy()
                            issued_copy['issue_date'] = datetime.strptime(issued['issue_date'], '%Y-%m-%d %H:%M:%S')
                            issued_copy['due_date'] = datetime.strptime(issued['due_date'], '%Y-%m-%d %H:%M:%S')
                            self.issued_books[member_id].append(issued_copy)
            except Exception as e:
                print(f"Error loading data: {e}")
                self.books = {}
                self.members = {}
                self.issued_books = {}
    
    def save_data(self):
        serializable_issued_books = {}
        for member_id, issued_list in self.issued_books.items():
            serializable_issued_books[member_id] = []
            for issued in issued_list:
                serializable_issued = issued.copy()
                serializable_issued['issue_date'] = issued['issue_date'].strftime('%Y-%m-%d %H:%M:%S')
                serializable_issued['due_date'] = issued['due_date'].strftime('%Y-%m-%d %H:%M:%S')
                serializable_issued_books[member_id].append(serializable_issued)
        
        data = {
            'books': self.books,
            'members': self.members,
            'issued_books': serializable_issued_books
        }
        with open('library_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_overdue_books(self):
        today = datetime.now()
        all_issued = []
        for issued_list in self.issued_books.values():
            all_issued.extend(issued_list)
        
        overdue = list(filter(
            lambda issued: (today - issued['issue_date']).days > 14,
            all_issued
        ))
        return overdue
    
    def calculate_total_late_fees(self):
        overdue_books = self.get_overdue_books()
        if not overdue_books:
            return 0
        
        def calculate_fee(issued):
            days_overdue = (datetime.now() - issued['issue_date']).days - 14
            return max(0, days_overdue) * 1.0
        
        total_fees = reduce(lambda total, issued: total + calculate_fee(issued), overdue_books, 0)
        return total_fees
    
    def search_books_recursive(self, query, book_ids=None, results=None):
        if book_ids is None:
            book_ids = list(self.books.keys())
            results = []
        
        if not book_ids:
            return results
        
        current_id = book_ids[0]
        book = self.books[current_id]
        
        if (query.lower() in book['title'].lower() or 
            query.lower() in book['author'].lower() or
            query.lower() in book['category'].lower()):
            results.append(current_id)
        
        return self.search_books_recursive(query, book_ids[1:], results)
    
    def issue_book(self, book_id, member_id):
        if member_id not in self.members:
            raise ValueError("Member not found")
        if member_id not in self.issued_books:
            self.issued_books[member_id] = []
        
        if len(self.issued_books[member_id]) >= 3:
            raise ValueError("Maximum book limit reached (3 books)")
        
        if book_id not in self.books:
            raise ValueError("Book not found")
        
        if self.books[book_id]['status'] != 'Available':
            raise ValueError("Book not available")
        
        issue_date = datetime.now()
        self.issued_books[member_id].append({
            'book_id': book_id,
            'issue_date': issue_date,
            'due_date': issue_date + timedelta(days=14)
        })
        
        self.books[book_id]['status'] = 'Issued'
        self.books[book_id]['issued_to'] = member_id
        
        return f"Book '{self.books[book_id]['title']}' issued to {self.members[member_id]['name']}"
    
    def return_book(self, book_id, member_id):
        if member_id not in self.issued_books:
            raise ValueError("No books issued to this member")
        
        for issued in self.issued_books[member_id]:
            if issued['book_id'] == book_id:
                days_overdue = (datetime.now() - issued['issue_date']).days - 14
                late_fee = max(0, days_overdue) * 1.0
                
                self.issued_books[member_id].remove(issued)
                self.books[book_id]['status'] = 'Available'
                self.books[book_id]['issued_to'] = None
                
                return f"Book returned. Late fee: ${late_fee:.2f}" if late_fee > 0 else "Book returned on time"
        
        raise ValueError("Book not issued to this member")
    
    def add_book(self, title, author, category, isbn):
        book_id = str(len(self.books) + 1).zfill(4)
        self.books[book_id] = {
            'title': title,
            'author': author,
            'category': category,
            'isbn': isbn,
            'status': 'Available',
            'issued_to': None
        }
        return book_id
    
    def delete_book(self, book_id):
        if book_id not in self.books:
            raise ValueError("Book not found")
        
        book = self.books[book_id]
        
        if book['status'] == 'Issued':
            raise ValueError("Cannot delete book that is currently issued")
        
        for member_id, issued_list in self.issued_books.items():
            for issued in issued_list:
                if issued['book_id'] == book_id:
                    raise ValueError("Cannot delete book that is currently issued")
        
        deleted_book = self.books.pop(book_id)
        return f"Book '{deleted_book['title']}' has been deleted from the library"
    
    def add_member(self, name, email, phone):
        member_id = str(len(self.members) + 1).zfill(4)
        self.members[member_id] = {
            'name': name,
            'email': email,
            'phone': phone,
            'join_date': datetime.now().strftime('%Y-%m-%d')
        }
        return member_id
    
    def delete_member(self, member_id):
        if member_id not in self.members:
            raise ValueError("Member not found")
        
        if member_id in self.issued_books and len(self.issued_books[member_id]) > 0:
            raise ValueError("Cannot delete member who has books currently issued")
        
        deleted_member = self.members.pop(member_id)
        
        if member_id in self.issued_books:
            self.issued_books.pop(member_id)
        
        return f"Member '{deleted_member['name']}' has been deleted from the library"

def manage_library():
    lms = LibraryManagementSystem()
    
    def issue_book_nested(book_id, member_id):
        return lms.issue_book(book_id, member_id)
    
    return lms, issue_book_nested

class LibraryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        self.lms, self.issue_book_nested = manage_library()
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📚 Library Management System", 
                               font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        books_frame = tk.LabelFrame(parent, text="📖 Book Management", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        books_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(books_frame, text="Add Book", command=self.add_book_dialog, 
                  bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(books_frame, text="Delete Book", command=self.delete_book_dialog, 
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(books_frame, text="Search Books", command=self.search_books_dialog, 
                  bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(books_frame, text="List All Books", command=self.list_all_books, 
                  bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        
        members_frame = tk.LabelFrame(parent, text="👥 Member Management", font=('Arial', 12, 'bold'), 
                                      bg='white', fg='#2c3e50')
        members_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(members_frame, text="Add Member", command=self.add_member_dialog, 
                  bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(members_frame, text="Delete Member", command=self.delete_member_dialog, 
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(members_frame, text="List Members", command=self.list_members, 
                  bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        
        operations_frame = tk.LabelFrame(parent, text="🔄 Library Operations", font=('Arial', 12, 'bold'), 
                                         bg='white', fg='#2c3e50')
        operations_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(operations_frame, text="Issue Book", command=self.issue_book_dialog, 
                  bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(operations_frame, text="Return Book", command=self.return_book_dialog, 
                  bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(operations_frame, text="Overdue Books", command=self.show_overdue_books, 
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(operations_frame, text="Late Fees", command=self.show_late_fees, 
                  bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        
        info_frame = tk.LabelFrame(parent, text="ℹ️ Library Information", font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#2c3e50')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(info_frame, text="Categories", command=self.show_categories, 
                  bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        tk.Button(info_frame, text="Library Rules", command=self.show_rules, 
                  bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(fill='x', padx=5, pady=5)
    
    def create_right_panel(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.books_frame = tk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text="📚 Books")
        
        self.books_tree = ttk.Treeview(self.books_frame, columns=('ID', 'Title', 'Author', 'Category', 'Status'), show='headings')
        self.books_tree.heading('ID', text='Book ID')
        self.books_tree.heading('Title', text='Title')
        self.books_tree.heading('Author', text='Author')
        self.books_tree.heading('Category', text='Category')
        self.books_tree.heading('Status', text='Status')
        
        self.books_tree.column('ID', width=80)
        self.books_tree.column('Title', width=250)
        self.books_tree.column('Author', width=180)
        self.books_tree.column('Category', width=120)
        self.books_tree.column('Status', width=100)
        
        books_scrollbar = ttk.Scrollbar(self.books_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=books_scrollbar.set)
        
        self.books_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        books_scrollbar.pack(side='right', fill='y', pady=10)
        
        self.members_frame = tk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text="👥 Members")
        
        self.members_tree = ttk.Treeview(self.members_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Join Date'), show='headings')
        self.members_tree.heading('ID', text='Member ID')
        self.members_tree.heading('Name', text='Name')
        self.members_tree.heading('Email', text='Email')
        self.members_tree.heading('Phone', text='Phone')
        self.members_tree.heading('Join Date', text='Join Date')
        
        self.members_tree.column('ID', width=80)
        self.members_tree.column('Name', width=180)
        self.members_tree.column('Email', width=250)
        self.members_tree.column('Phone', width=140)
        self.members_tree.column('Join Date', width=120)
        
        members_scrollbar = ttk.Scrollbar(self.members_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=members_scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        members_scrollbar.pack(side='right', fill='y', pady=10)
        
        self.issued_frame = tk.Frame(self.notebook)
        self.notebook.add(self.issued_frame, text="📖 Issued Books")
        
        self.issued_tree = ttk.Treeview(self.issued_frame, columns=('Member', 'Book', 'Issue Date', 'Due Date', 'Status'), show='headings')
        self.issued_tree.heading('Member', text='Member')
        self.issued_tree.heading('Book', text='Book')
        self.issued_tree.heading('Issue Date', text='Issue Date')
        self.issued_tree.heading('Due Date', text='Due Date')
        self.issued_tree.heading('Status', text='Status')
        
        self.issued_tree.column('Member', width=150)
        self.issued_tree.column('Book', width=250)
        self.issued_tree.column('Issue Date', width=120)
        self.issued_tree.column('Due Date', width=120)
        self.issued_tree.column('Status', width=100)
        
        issued_scrollbar = ttk.Scrollbar(self.issued_frame, orient='vertical', command=self.issued_tree.yview)
        self.issued_tree.configure(yscrollcommand=issued_scrollbar.set)
        
        self.issued_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        issued_scrollbar.pack(side='right', fill='y', pady=10)
    
    def load_data(self):
        self.refresh_books()
        self.refresh_members()
        self.refresh_issued_books()
    
    def refresh_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        for book_id, book in self.lms.books.items():
            self.books_tree.insert('', 'end', values=(
                book_id, book['title'], book['author'], book['category'], book['status']
            ))
    
    def refresh_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        for member_id, member in self.lms.members.items():
            self.members_tree.insert('', 'end', values=(
                member_id, member['name'], member['email'], member['phone'], member['join_date']
            ))
    
    def refresh_issued_books(self):
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        
        for member_id, issued_list in self.lms.issued_books.items():
            for issued in issued_list:
                book = self.lms.books[issued['book_id']]
                member = self.lms.members[member_id]
                
                days_overdue = (datetime.now() - issued['issue_date']).days - 14
                status = "Overdue" if days_overdue > 0 else "On Time"
                
                self.issued_tree.insert('', 'end', values=(
                    member['name'],
                    book['title'],
                    issued['issue_date'].strftime('%Y-%m-%d'),
                    issued['due_date'].strftime('%Y-%m-%d'),
                    status
                ))
    
    def add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Add New Book", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Title:", bg='white').pack()
        title_entry = tk.Entry(dialog, width=40)
        title_entry.pack(pady=5)
        
        tk.Label(dialog, text="Author:", bg='white').pack()
        author_entry = tk.Entry(dialog, width=40)
        author_entry.pack(pady=5)
        
        tk.Label(dialog, text="Category:", bg='white').pack()
        category_var = tk.StringVar(value=list(self.lms.categories)[0])
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=list(self.lms.categories))
        category_combo.pack(pady=5)
        
        tk.Label(dialog, text="ISBN:", bg='white').pack()
        isbn_entry = tk.Entry(dialog, width=40)
        isbn_entry.pack(pady=5)
        
        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            category = category_var.get()
            isbn = isbn_entry.get().strip()
            
            if title and author and category and isbn:
                book_id = self.lms.add_book(title, author, category, isbn)
                self.lms.save_data()
                self.refresh_books()
                messagebox.showinfo("Success", f"Book added with ID: {book_id}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")
        
        tk.Button(dialog, text="Save Book", command=save_book, bg='#2ecc71', fg='white').pack(pady=20)
    
    def delete_book_dialog(self):
        if not self.lms.books:
            messagebox.showinfo("Info", "No books available to delete")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Book")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Delete Book", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Select Book to Delete:", bg='white').pack()
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(dialog, textvariable=book_var, 
                                  values=[f"{bid}: {book['title']} ({book['status']})" 
                                         for bid, book in self.lms.books.items()])
        book_combo.pack(pady=5)
        
        warning_label = tk.Label(dialog, text="⚠️ Warning: This action cannot be undone!", 
                                fg='red', bg='white', font=('Arial', 10, 'bold'))
        warning_label.pack(pady=10)
        
        def delete_book():
            try:
                book_id = book_var.get().split(':')[0]
                
                confirm = messagebox.askyesno("Confirm Deletion", 
                                            "Are you sure you want to delete this book?\n\nThis action cannot be undone!")
                if not confirm:
                    return
                
                result = self.lms.delete_book(book_id)
                self.lms.save_data()
                self.refresh_books()
                messagebox.showinfo("Success", result)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(dialog, text="Delete Book", command=delete_book, bg='#e74c3c', fg='white').pack(pady=20)
    
    def add_member_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Member")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Add New Member", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Name:", bg='white').pack()
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:", bg='white').pack()
        email_entry = tk.Entry(dialog, width=40)
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:", bg='white').pack()
        phone_entry = tk.Entry(dialog, width=40)
        phone_entry.pack(pady=5)
        
        def save_member():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if name and email and phone:
                member_id = self.lms.add_member(name, email, phone)
                self.lms.save_data()
                self.refresh_members()
                messagebox.showinfo("Success", f"Member added with ID: {member_id}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")
        
        tk.Button(dialog, text="Save Member", command=save_member, bg='#2ecc71', fg='white').pack(pady=20)
    
    def delete_member_dialog(self):
        if not self.lms.members:
            messagebox.showinfo("Info", "No members available to delete")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Member")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Delete Member", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Select Member to Delete:", bg='white').pack()
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(dialog, textvariable=member_var, 
                                    values=[f"{mid}: {member['name']} ({member['email']})" 
                                           for mid, member in self.lms.members.items()])
        member_combo.pack(pady=5)
        
        warning_label = tk.Label(dialog, text="⚠️ Warning: This action cannot be undone!", 
                                fg='red', bg='white', font=('Arial', 10, 'bold'))
        warning_label.pack(pady=10)
        
        def delete_member():
            try:
                member_id = member_var.get().split(':')[0]
                
                confirm = messagebox.askyesno("Confirm Deletion", 
                                            "Are you sure you want to delete this member?\n\nThis action cannot be undone!")
                if not confirm:
                    return
                
                result = self.lms.delete_member(member_id)
                self.lms.save_data()
                self.refresh_members()
                self.refresh_issued_books()
                messagebox.showinfo("Success", result)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(dialog, text="Delete Member", command=delete_member, bg='#e74c3c', fg='white').pack(pady=20)
    
    def search_books_dialog(self):
        query = simpledialog.askstring("Search Books", "Enter search term:")
        if query:
            results = self.lms.search_books_recursive(query)
            if results:
                messagebox.showinfo("Search Results", f"Found {len(results)} books matching '{query}'")
                self.books_tree.selection_set()
                for book_id in results:
                    for item in self.books_tree.get_children():
                        if self.books_tree.item(item)['values'][0] == book_id:
                            self.books_tree.selection_add(item)
                            self.books_tree.see(item)
            else:
                messagebox.showinfo("Search Results", f"No books found matching '{query}'")
    
    def issue_book_dialog(self):
        if not self.lms.books or not self.lms.members:
            messagebox.showwarning("Warning", "No books or members available")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Issue Book")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Issue Book", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Book ID:", bg='white').pack()
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(dialog, textvariable=book_var, 
                                  values=[f"{bid}: {book['title']}" for bid, book in self.lms.books.items() if book['status'] == 'Available'])
        book_combo.pack(pady=5)
        
        tk.Label(dialog, text="Member ID:", bg='white').pack()
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(dialog, textvariable=member_var, 
                                    values=[f"{mid}: {member['name']}" for mid, member in self.lms.members.items()])
        member_combo.pack(pady=5)
        
        def issue():
            try:
                book_id = book_var.get().split(':')[0]
                member_id = member_var.get().split(':')[0]
                
                result = self.issue_book_nested(book_id, member_id)
                self.lms.save_data()
                self.refresh_books()
                self.refresh_issued_books()
                messagebox.showinfo("Success", result)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(dialog, text="Issue Book", command=issue, bg='#e67e22', fg='white').pack(pady=20)
    
    def return_book_dialog(self):
        if not self.lms.issued_books:
            messagebox.showinfo("Info", "No books are currently issued")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Return Book")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Return Book", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(dialog, text="Book ID:", bg='white').pack()
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(dialog, textvariable=book_var, 
                                  values=[f"{bid}: {self.lms.books[bid]['title']}" 
                                         for mid, issued_list in self.lms.issued_books.items() 
                                         for issued in issued_list 
                                         for bid in [issued['book_id']]])
        book_combo.pack(pady=5)
        
        tk.Label(dialog, text="Member ID:", bg='white').pack()
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(dialog, textvariable=member_var, 
                                    values=[f"{mid}: {self.lms.members[mid]['name']}" 
                                           for mid in self.lms.issued_books.keys()])
        member_combo.pack(pady=5)
        
        def return_book():
            try:
                book_id = book_var.get().split(':')[0]
                member_id = member_var.get().split(':')[0]
                
                result = self.lms.return_book(book_id, member_id)
                self.lms.save_data()
                self.refresh_books()
                self.refresh_issued_books()
                messagebox.showinfo("Success", result)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(dialog, text="Return Book", command=return_book, bg='#1abc9c', fg='white').pack(pady=20)
    
    def list_all_books(self):
        self.notebook.select(0)
        messagebox.showinfo("Books", f"Total books: {len(self.lms.books)}")
    
    def list_members(self):
        self.notebook.select(1)
        messagebox.showinfo("Members", f"Total members: {len(self.lms.members)}")
    
    def show_overdue_books(self):
        overdue = self.lms.get_overdue_books()
        if overdue:
            message = f"Found {len(overdue)} overdue books:\n\n"
            for issued in overdue:
                book = self.lms.books[issued['book_id']]
                member_name = "Unknown"
                for member_id, issued_list in self.lms.issued_books.items():
                    for issued_book in issued_list:
                        if issued_book['book_id'] == issued['book_id']:
                            member_name = self.lms.members[member_id]['name']
                            break
                    if member_name != "Unknown":
                        break
                
                days_overdue = (datetime.now() - issued['issue_date']).days - 14
                message += f"• {book['title']} - {member_name} ({days_overdue} days overdue)\n"
            messagebox.showinfo("Overdue Books", message)
        else:
            messagebox.showinfo("Overdue Books", "No overdue books found")
    
    def show_late_fees(self):
        total_fees = self.lms.calculate_total_late_fees()
        messagebox.showinfo("Late Fees", f"Total late fees: ${total_fees:.2f}")
    
    def show_categories(self):
        categories_text = "Available Categories:\n\n"
        for category in self.lms.categories:
            categories_text += f"• {category}\n"
        messagebox.showinfo("Categories", categories_text)
    
    def show_rules(self):
        rules_text = "Library Rules:\n\n"
        for rule in self.lms.library_rules:
            rules_text += f"• {rule}\n"
        messagebox.showinfo("Library Rules", rules_text)

def main():
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
