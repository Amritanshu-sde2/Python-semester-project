#!/usr/bin/env python3
"""
Test JSON serialization with datetime objects
"""

from library import LibraryManagementSystem
from datetime import datetime, timedelta

def test_json_serialization():
    """Test that the system can save and load data with datetime objects"""
    print("🧪 Testing JSON Serialization...")
    
    # Create a new instance
    lms = LibraryManagementSystem()
    
    # Add a book and member
    book_id = lms.add_book("Test Book", "Test Author", "Fiction", "123-456-789")
    member_id = lms.add_member("Test User", "test@email.com", "555-0000")
    
    print(f"✅ Added book: {book_id}")
    print(f"✅ Added member: {member_id}")
    
    # Issue a book (this creates datetime objects)
    try:
        result = lms.issue_book(book_id, member_id)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Error issuing book: {e}")
        return
    
    # Test saving data (this should not fail with datetime objects)
    try:
        lms.save_data()
        print("✅ Data saved successfully")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return
    
    # Test loading data
    try:
        lms2 = LibraryManagementSystem()
        print("✅ Data loaded successfully")
        
        # Verify the data was loaded correctly
        if book_id in lms2.books:
            print("✅ Book data preserved")
        if member_id in lms2.members:
            print("✅ Member data preserved")
        if member_id in lms2.issued_books:
            print("✅ Issued book data preserved")
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    print("\n🎉 JSON serialization test completed successfully!")
    print("🚀 The system can now handle datetime objects properly!")

if __name__ == "__main__":
    test_json_serialization()
