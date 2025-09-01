import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

class SimpleLibrary:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.issued_books = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('library_data.json'):
            try:
                with open('library_data.json', 'r') as f:
                    data = json.load(f)
                    self.books = data.get('books', {})
                    self.members = data.get('members', {})
            except:
                pass
    
    def save_data(self):
        data = {'books': self.books, 'members': self.members}
        with open('library_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_book(self, title, author, category):
        book_id = str(len(self.books) + 1).zfill(4)
        self.books[book_id] = {'title': title, 'author': author, 'category': category, 'status': 'Available'}
        return book_id
    
    def add_member(self, name, email, phone):
        member_id = str(len(self.members) + 1).zfill(4)
        self.members[member_id] = {'name': name, 'email': email, 'phone': phone, 'join_date': datetime.now().strftime('%Y-%m-%d')}
        return member_id

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Library Management")
        self.root.geometry("800x600")
        
        self.library = SimpleLibrary()
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="📚 Simple Library Management", font=('Arial', 20, 'bold'))
        title.pack(pady=20)
        
        # Buttons
        tk.Button(self.root, text="Add Book", command=self.add_book, bg='blue', fg='white', font=('Arial', 12)).pack(pady=10)
        tk.Button(self.root, text="Add Member", command=self.add_member, bg='green', fg='white', font=('Arial', 12)).pack(pady=10)
        tk.Button(self.root, text="View Books", command=self.view_books, bg='orange', fg='white', font=('Arial', 12)).pack(pady=10)
        tk.Button(self.root, text="View Members", command=self.view_members, bg='purple', fg='white', font=('Arial', 12)).pack(pady=10)
    
    def add_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Title:").pack()
        title_entry = tk.Entry(dialog, width=30)
        title_entry.pack()
        
        tk.Label(dialog, text="Author:").pack()
        author_entry = tk.Entry(dialog, width=30)
        author_entry.pack()
        
        tk.Label(dialog, text="Category:").pack()
        category_entry = tk.Entry(dialog, width=30)
        category_entry.pack()
        
        def save():
            title = title_entry.get()
            author = author_entry.get()
            category = category_entry.get()
            if title and author and category:
                book_id = self.library.add_book(title, author, category)
                self.library.save_data()
                messagebox.showinfo("Success", f"Book added with ID: {book_id}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields required")
        
        tk.Button(dialog, text="Save", command=save, bg='green', fg='white').pack(pady=20)
    
    def add_member(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Member")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Name:").pack()
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()
        
        tk.Label(dialog, text="Email:").pack()
        email_entry = tk.Entry(dialog, width=30)
        email_entry.pack()
        
        tk.Label(dialog, text="Phone:").pack()
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.pack()
        
        def save():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            if name and email and phone:
                member_id = self.library.add_member(name, email, phone)
                self.library.save_data()
                messagebox.showinfo("Success", f"Member added with ID: {member_id}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields required")
        
        tk.Button(dialog, text="Save", command=save, bg='green', fg='white').pack(pady=20)
    
    def view_books(self):
        if not self.library.books:
            messagebox.showinfo("Books", "No books available")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Books")
        dialog.geometry("600x400")
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Title', 'Author', 'Category', 'Status'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Title', text='Title')
        tree.heading('Author', text='Author')
        tree.heading('Category', text='Category')
        tree.heading('Status', text='Status')
        
        for book_id, book in self.library.books.items():
            tree.insert('', 'end', values=(book_id, book['title'], book['author'], book['category'], book['status']))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def view_members(self):
        if not self.library.members:
            messagebox.showinfo("Members", "No members available")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Members")
        dialog.geometry("600x400")
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Name', 'Email', 'Phone', 'Join Date'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Email', text='Email')
        tree.heading('Phone', text='Phone')
        tree.heading('Join Date', text='Join Date')
        
        for member_id, member in self.library.members.items():
            tree.insert('', 'end', values=(member_id, member['name'], member['email'], member['phone'], member['join_date']))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_data(self):
        pass

def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
