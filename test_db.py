from core.database import engine, test_db_connection
import sys

def print_status(message, is_error=False):
    """Print status message with error handling for Windows console"""
    try:
        print(f"[{'ERROR' if is_error else 'INFO'}] {message}")
    except UnicodeEncodeError:
        # Fallback for Windows console with limited character set
        message = message.encode('ascii', 'replace').decode('ascii')
        print(f"[{'ERROR' if is_error else 'INFO'}] {message}")

def main():
    print_status("Testing database connection...")
    try:
        if test_db_connection():
            print_status("Database connection successful!")
        else:
            print_status("Database connection failed!", is_error=True)
    except Exception as e:
        print_status(f"Error: {str(e)}", is_error=True)
        print_status("\nTroubleshooting tips:")
        print_status("1. Check if your Supabase database is running")
        print_status("2. Verify your database credentials in .env")
        print_status("3. Ensure your IP is whitelisted in Supabase")
        print_status("4. Check if you're using the correct port (6543 for Supabase)")
        print_status("5. Make sure SSL is properly configured")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
