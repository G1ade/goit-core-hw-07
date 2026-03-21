def input_error(func):
    def inner(*args, **kwargs):
        """
        Decorator that handles input errors for contact management functions.
        
        Catches and handles:
        - ValueError: when name and phone are not provided correctly
        - IndexError: when contact name is missing
        - KeyError: when contact does not exist in the list
        
        On KeyError, offers interactive option to add the missing contact.
        
        Args:
            func: Function to decorate (add_contact, change_contact, etc.)
            
        Returns:
            inner: Wrapped function with comprehensive error handling
        """

        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "You need to enter the contact's name"
        except KeyError:
            # Extract contact name from args (first element of first argument)
            contact_name = args[0][0]
            
            if not contact_name.isdigit():
                print(f"The contact '{contact_name}' does not exist in your list")

                # Interactive loop to offer adding the contact
                while True:
                    user_input = input('Would you like to add a contact? Yes/No ')
                    # Get first character and normalize to uppercase
                    first_char = user_input[0].upper()

                    if first_char == 'Y':
                        # User wants to add contact
                        number = input(f'enter {contact_name} contact number ')
                        return add_contact([contact_name, number], args[1])
                    if first_char == 'N':
                        return 'As you say'
            else:
                return "You need to enter the contact's name, not the number!"
            
    return inner

def parse_input(user_input: str) -> tuple:
    """
    Parse user input into command and arguments.
    
    Splits input string by spaces. First word becomes command,
    remaining words are collected into args list.
    
    Args:
        user_input (str): Raw input string from user
        
    Returns:
        tuple: (command, *args) where command is lowercase string
    """

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args: tuple, path: str) -> str:
    """
    Add a new contact to the phone book file.
    
    If file doesn't exist, creates it. Appends contact in format 'name:phone'.
    
    Args:
        args (list): List containing [name, phone]
        path (str): Path to the contacts file
        
    Returns:
        str: Success message or error description
    """

    name, phone = args
    mode = 'a'

    # Loop until successfully written (handles missing file case)
    while True:
        try:
            with open(path, mode, encoding='utf-8') as file:
                file.write(f'{name}:{phone}\n')
                break
        except FileNotFoundError:
            mode = "w"

    return "Contact added."

@input_error
def change_contact(args: tuple, path: str) -> str:
    """
    Update phone number for an existing contact.
    
    Reads all contacts, updates specified contact's phone,
    then rewrites the entire file.
    
    Args:
        args (list): List containing [name, new_phone]
        path (str): Path to the contacts file
        
    Returns:
        str: Success message or error description
    """

    desired_name, new_phone = args

    try:
        # Read existing contacts into dictionary
        with open(path, 'r', encoding='utf-8') as file:
            contacts = dict(el.strip().split(':') for el in file.readlines())

            # Check if contact exists
            if desired_name not in contacts:
                return f'contact {desired_name} not found.'
            else:
                contacts[desired_name] = new_phone
        
        # Rewrite file with updated data
        with open(path, 'w', encoding='utf-8') as file:
            for name, phone in contacts.items():
                file.write(f'{name}:{phone}\n')
                
    except FileNotFoundError:
        return "You haven't added any contacts yet!"
        
    return "contact changed"

@input_error
def phone_username(args, path):
    """
    Retrieve phone number for a specific contact.
    
    Args:
        args (list): List containing [name]
        path (str): Path to the contacts file
        
    Returns:
        str: Contact info or error message
    """

    try:
        # Load contacts from file
        with open(path, 'r', encoding='utf-8') as file:
            contacts = dict(el.strip().split(':') for el in file.readlines())
            # Get phone for requested contact (args[0] is the name)
            return f'{args[0]} {contacts[args[0]]}'
        
    except FileNotFoundError:
        return "You haven't added any contacts yet!"

def all_contacts(path: str) -> str:
    """
    Display all contacts in formatted table.
    
    Args:
        path (str): Path to the contacts file
        
    Returns:
        str: Formatted table of contacts or error message
    """

    try:
        # Read all contacts
        with open(path, 'r', encoding='utf-8') as file:
            contacts = dict(el.strip().split(':') for el in file.readlines())
        
        # Build formatted output lines
        lines = []
        lines.append("-" * 25)
        lines.append(f"{'Name':<10} | {'Phone':<10}")
        lines.append("-" * 25)
        
        # Add each contact to table
        for name, phone in contacts.items():
            lines.append(f"{name:<10} | {phone}")
            
        lines.append("-" * 25)
        
        # Join all lines with newlines
        return "\n".join(lines)
        
    except FileNotFoundError:
        return "You haven't added any contacts yet!"
