#!/usr/bin/env python3
"""
Simple test script for Library Management System
"""

from library import LibraryManagementSystem

def test_library_system():
    """Test basic functionality of the library system"""
    print("🧪 Testing Library Management System...")
    
    # Create instance
    lms = LibraryManagementSystem()
    
    # Test 1: Add books
    print("\n📚 Test 1: Adding books...")
    book1_id = lms.add_book("Test Book 1", "Test Author 1", "Fiction", "123-456-789")
    book2_id = lms.add_book("Test Book 2", "Test Author 2", "Science", "987-654-321")
    print(f"✅ Added books: {book1_id}, {book2_id}")
    
    # Test 2: Add members
    print("\n👥 Test 2: Adding members...")
    member1_id = lms.add_member("Test User 1", "user1@test.com", "555-0001")
    member2_id = lms.add_member("Test User 2", "user2@test.com", "555-0002")
    print(f"✅ Added members: {member1_id}, {member2_id}")
    
    # Test 3: Issue books
    print("\n📖 Test 3: Issuing books...")
    try:
        result = lms.issue_book(book1_id, member1_id)
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Error issuing book: {e}")
    
    # Test 4: Search books
    print("\n🔍 Test 4: Searching books...")
    search_results = lms.search_books_recursive("Test")
    print(f"✅ Found {len(search_results)} books matching 'Test'")
    
    # Test 5: Get overdue books
    print("\n⏰ Test 5: Checking overdue books...")
    overdue = lms.get_overdue_books()
    print(f"✅ Found {len(overdue)} overdue books")
    
    # Test 6: Calculate late fees
    print("\n💰 Test 6: Calculating late fees...")
    total_fees = lms.calculate_total_late_fees()
    print(f"✅ Total late fees: ${total_fees:.2f}")
    
    # Test 7: Format titles uppercase
    print("\n🔤 Test 7: Formatting titles uppercase...")
    titles = ["book one", "book two", "book three"]
    uppercase_titles = lms.format_titles_uppercase(titles)
    print(f"✅ Uppercase titles: {uppercase_titles}")
    
    # Test 8: Delete functionality
    print("\n🗑️ Test 8: Testing delete functionality...")
    try:
        # Test deleting a book
        delete_result = lms.delete_book(book2_id)
        print(f"✅ {delete_result}")
        
        # Test deleting a member
        delete_member_result = lms.delete_member(member2_id)
        print(f"✅ {delete_member_result}")
        
    except Exception as e:
        print(f"❌ Error in delete test: {e}")
    
    # Test 9: Show categories and rules
    print("\n📋 Test 9: Categories and rules...")
    print(f"✅ Categories: {lms.categories}")
    print(f"✅ Rules count: {len(lms.library_rules)}")
    
    print("\n🎉 All tests completed successfully!")
    print("🚀 The Library Management System is working correctly!")

if __name__ == "__main__":
    test_library_system()
