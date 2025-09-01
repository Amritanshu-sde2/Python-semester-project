#!/usr/bin/env python3
"""
Demo script for the Simple Library Management System
This script demonstrates the simplified library system without authentication.
"""

import os
import sys

def demo_simple_library():
    """Demonstrate the simplified library system"""
    print("🚀 Simple Library Management System Demo")
    print("=" * 50)
    print("✨ Features:")
    print("• No login or authentication required")
    print("• Simple, intuitive interface")
    print("• Basic book and member management")
    print("• JSON file storage")
    print("• Clean, colorful UI")
    print("=" * 50)
    
    try:
        # Check if the main file exists
        if os.path.exists('simple_library.py'):
            print("✅ Main application file found")
            print("🚀 To run the application, use:")
            print("   python simple_library.py")
        else:
            print("❌ Main application file not found")
            print("Please ensure 'simple_library.py' is in the current directory")
        
        print("\n📚 What you can do:")
        print("1. Add new books with title, author, and category")
        print("2. Register new library members")
        print("3. View all books and members in tables")
        print("4. All data is automatically saved")
        
        print("\n🎯 Perfect for:")
        print("• Small libraries")
        print("• Educational purposes")
        print("• Personal book collections")
        print("• Learning Python GUI development")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_system_info():
    """Show system information"""
    print("\n💻 System Information:")
    print("=" * 30)
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"Python Version: {python_version}")
    
    # Check if tkinter is available
    try:
        import tkinter
        print("✅ Tkinter: Available")
    except ImportError:
        print("❌ Tkinter: Not available")
        print("   Tkinter is required for the GUI")
    
    # Check if required modules are available
    required_modules = ['json', 'os', 'datetime']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
        except ImportError:
            print(f"❌ {module}: Not available")

if __name__ == "__main__":
    print("📚 Simple Library Management System")
    print("=" * 50)
    
    demo_simple_library()
    show_system_info()
    
    print("\n🚀 Ready to use! Run 'python simple_library.py' to start.")
