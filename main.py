from pathlib import Path
from contacts import *

def main():
    """Main entry point for the assistant bot."""
    
    # Path to the data file
    path = Path(__file__).parent / 'contact_list.pkl'
    
    # Load existing data or create new book
    book = load_data(path)
    
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            save_data(book, path)
            print("Good bye!")
            break
            
        elif command == "hello":
            print("How can I help you?")
            
        elif command == "help":
            print(show_help())
            
        elif command == "add":
            print(add_contact(args, book))
            
        elif command == "add-birthday":
            print(add_birthday(args, book))
            
        elif command == "show-birthday":
            print(show_birthday(args, book))
            
        elif command == "birthdays":
            print(birthdays(args, book))
            
        elif command == "change":
            print(change_contact(args, book))
            
        elif command == "phone":
            print(phone_username(args, book))
            
        elif command == "remove":
            print(remove_phone(args, book))
            
        elif command == "delete":
            print(delete_contact(args, book))
            
        elif command == "all":
            print(all_contacts(book))
            
        elif command == "save":
            save_data(book, path)
            print("Data saved.")
            
        else:
            print("Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()