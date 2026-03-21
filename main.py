from contacts import *
from pathlib import Path

def main():
    """
    Main entry point for the assistant bot.
    
    Runs interactive command loop until user exits.
    """

    # Path to the contacts file
    path = Path(__file__).parent / 'contact_list.txt'

    print("Welcome to the assistant bot!")

    # Main command processing loop
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        # Command routing
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, path))
        elif command == "change":
            print(change_contact(args, path))
        elif command == "phone":
            print(phone_username(args, path))
        elif command == "all":
            print(all_contacts(path))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()