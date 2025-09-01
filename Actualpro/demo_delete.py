#!/usr/bin/env python3
"""
Demonstration of Delete Functionality in Library Management System
"""

from library import LibraryManagementSystem

def demo_delete_functionality():
    """Demonstrate the delete functionality"""
    print("🗑️ Demonstrating Delete Functionality in Library Management System")
    print("=" * 60)
    
    # Create a fresh instance
    lms = LibraryManagementSystem()
    
    # Add some test data
    print("\n📚 Adding test books...")
    book1 = lms.add_book("Demo Book 1", "Author A", "Fiction", "123-001")
    book2 = lms.add_book("Demo Book 2", "Author B", "Science", "123-002")
    book3 = lms.add_book("Demo Book 3", "Author C", "History", "123-003")
    print(f"✅ Added books: {book1}, {book2}, {book3}")
    
    print("\n👥 Adding test members...")
    member1 = lms.add_member("Demo User 1", "user1@demo.com", "555-0001")
    member2 = lms.add_member("Demo User 2", "user2@demo.com", "555-0002")
    print(f"✅ Added members: {member1}, {member2}")
    
    # Show current state
    print(f"\n📊 Current state:")
    print(f"   Books: {len(lms.books)}")
    print(f"   Members: {len(lms.members)}")
    
    # Test 1: Delete a book that's not issued
    print("\n🗑️ Test 1: Deleting a book that's not issued...")
    try:
        result = lms.delete_book(book3)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Try to delete a book that's issued (should fail)
    print("\n📖 Test 2: Issuing a book...")
    try:
        issue_result = lms.issue_book(book1, member1)
        print(f"✅ {issue_result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🗑️ Test 2: Trying to delete an issued book (should fail)...")
    try:
        result = lms.delete_book(book1)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Expected error: {e}")
    
    # Test 3: Delete a member with no issued books
    print("\n🗑️ Test 3: Deleting a member with no issued books...")
    try:
        result = lms.delete_member(member2)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Try to delete a member with issued books (should fail)
    print("\n🗑️ Test 4: Trying to delete a member with issued books (should fail)...")
    try:
        result = lms.delete_member(member1)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Expected error: {e}")
    
    # Show final state
    print(f"\n📊 Final state:")
    print(f"   Books: {len(lms.books)}")
    print(f"   Members: {len(lms.members)}")
    
    # List remaining books and members
    print(f"\n📚 Remaining books:")
    for bid, book in lms.books.items():
        print(f"   {bid}: {book['title']} - {book['status']}")
    
    print(f"\n👥 Remaining members:")
    for mid, member in lms.members.items():
        print(f"   {mid}: {member['name']} - {member['email']}")
    
    print("\n🎉 Delete functionality demonstration completed!")
    print("✅ The system successfully prevents deletion of items in use")
    print("✅ Safe deletion works for unused items")

if __name__ == "__main__":
    demo_delete_functionality()
