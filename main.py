# -*- coding: utf-8 -*- 
""" 
Created on Thu Mar  6 09:43:09 2025 
 
@author: admin 
""" 
 
import sqlite3 
import os 
import shutil  # Import shutil for file copying 
from tkinter import * 
from tkinter import filedialog 
from tkinter import messagebox 
from PIL import Image, ImageTk 
import re  # For date validation 
 
# Create or connect to SQLite database 
conn = sqlite3.connect('memories.db') 
c = conn.cursor() 
 
# Create memories table if it doesn't exist 
c.execute('''CREATE TABLE IF NOT EXISTS memories 
             (id INTEGER PRIMARY KEY, photo_path TEXT, description 
TEXT, tags TEXT, date TEXT)''') 
conn.commit() 
 
 
# Function to upload a new memory 
def upload_memory(): 
    # Open file dialog to choose an image 
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", 
"*.jpg;*.png;*.jpeg")]) 
    if not file_path: 
        return 
 
    # Open a form to enter the description, tags, and date 
    description = description_entry.get() 
    tags = tags_entry.get() 
    date = date_entry.get() 
 
    # Validate description and date fields 
    if not description or not date: 
        messagebox.showerror("Input Error", "Description and Date 
cannot be empty!") 
        return 
 
    # Validate date format (dd/mm/yyyy) 
    if not re.match(r"\d{2}/\d{2}/\d{4}", date): 
        messagebox.showerror("Date Error", "Date format must be 
dd/mm/yyyy!") 
        return 
 
    # Save the image in a folder and get the path 
    memory_folder = "memories/" 
    if not os.path.exists(memory_folder): 
        os.makedirs(memory_folder) 
     
    # Copy the file to the memories folder 
    image_path = os.path.join(memory_folder, 
os.path.basename(file_path)) 
    shutil.copy(file_path, image_path) 
 
    # Insert the memory data into the database 
    c.execute('''INSERT INTO memories (photo_path, description, tags, 
date) 
                 VALUES (?, ?, ?, ?)''', (image_path, description, 
tags, date)) 
    conn.commit() 
 
    messagebox.showinfo("Success", "Memory uploaded successfully!") 
    clear_entries() 
 
 
# Function to search and display memories 
def search_memories(): 
    search_term = search_entry.get()  # Get the search term entered by 
the user 
    conn = sqlite3.connect('memories.db')  # Connect to the database 
    c = conn.cursor() 
    # SQL query to search for memories based on description or tags 
    c.execute("SELECT * FROM memories WHERE description LIKE ? OR tags 
LIKE ?", 
              ('%' + search_term + '%', '%' + search_term + '%')) 
    results = c.fetchall()  # Fetch all the results 
    display_results(results)  # Display the results in the text box 
    conn.close() 
 
 
# Function to display memories 
def display_results(results): 
    result_text.delete(1.0, END)  # Clear existing results 
    if not results: 
        result_text.insert(END, "No memories found!") 
    for row in results: 
        result_text.insert(END, f"ID: {row[0]}\nDescription: 
{row[2]}\nTags: {row[3]}\nDate: {row[4]}\n\n") 
         
        # Open the image from the file path 
        try: 
            img = Image.open(row[1])  # Open the image from the stored 
path 
            img.thumbnail((100, 100))  # Resize the image to fit in the 
Text widget 
            img = ImageTk.PhotoImage(img)  # Convert to Tkinter format 
 
            # Store the image reference to prevent garbage collection 
            result_text.image_ref = img  # Store a reference to the 
image 
 
            # Insert image into the Text widget 
            result_text.image_create(END, image=img) 
        except Exception as e: 
            result_text.insert(END, f"Error loading image: {e}\n") 
         
        result_text.insert(END, '\n\n') 
    result_text.yview(END) 
 
 
# Function to clear input fields 
def clear_entries(): 
    description_entry.delete(0, END) 
    tags_entry.delete(0, END) 
    date_entry.delete(0, END) 
 
 
# GUI Setup using Tkinter 
root = Tk() 
root.title("Memory Keeper") 
root.geometry("700x600")  # Increased window size 
root.config(bg="#f0f0f0")  # Light background color 
 
# Create Frames for organization 
top_frame = Frame(root, bg="#E3F2FD", bd=5) 
top_frame.pack(fill="x", padx=10, pady=10) 
 
middle_frame = Frame(root, bg="#f0f0f0") 
middle_frame.pack(fill="x", padx=10) 
 
bottom_frame = Frame(root, bg="#f0f0f0") 
bottom_frame.pack(fill="both", expand=True, padx=10, pady=10) 
 
# Header Label 
header_label = Label(top_frame, text="Welcome to Memory Keeper", 
font=("Helvetica", 20, "bold"), bg="#E3F2FD", fg="#2C3E50") 
header_label.pack(pady=10) 
 
# Description Label and Entry 
description_label = Label(middle_frame, text="Description:", 
font=("Helvetica", 12), bg="#f0f0f0") 
description_label.grid(row=0, column=0, sticky="w", padx=10, pady=5) 
description_entry = Entry(middle_frame, width=40, font=("Helvetica", 
12)) 
description_entry.grid(row=0, column=1, padx=10, pady=5) 
 
# Tags Label and Entry 
tags_label = Label(middle_frame, text="Tags (comma-separated):", 
font=("Helvetica", 12), bg="#f0f0f0") 
tags_label.grid(row=1, column=0, sticky="w", padx=10, pady=5) 
tags_entry = Entry(middle_frame, width=40, font=("Helvetica", 12)) 
tags_entry.grid(row=1, column=1, padx=10, pady=5) 
 
# Date Label and Entry 
date_label = Label(middle_frame, text="Date (DD/MM/YYYY):", 
font=("Helvetica", 12), bg="#f0f0f0") 
date_label.grid(row=2, column=0, sticky="w", padx=10, pady=5) 
date_entry = Entry(middle_frame, width=40, font=("Helvetica", 12)) 
date_entry.grid(row=2, column=1, padx=10, pady=5) 
# Upload Button with Styling 
upload_button = Button(middle_frame, text="Upload Memory", 
command=upload_memory, bg="#4CAF50", fg="white", font=("Helvetica", 14, 
"bold"), relief="raised", bd=2) 
upload_button.grid(row=3, column=0, columnspan=2, pady=20) 
# Search Label and Entry 
search_label = Label(bottom_frame, text="Search for Memories:", 
font=("Helvetica", 12), bg="#f0f0f0") 
search_label.pack(pady=10) 
search_entry = Entry(bottom_frame, width=40, font=("Helvetica", 12)) 
search_entry.pack(pady=5) 
# Search Button with Styling 
search_button = Button(bottom_frame, text="Search", 
command=search_memories, bg="#3498DB", fg="white", font=("Helvetica", 
14, "bold"), relief="raised", bd=2) 
search_button.pack(pady=10) 
# Text Box for Results Display 
result_text = Text(bottom_frame, height=10, width=50, 
font=("Helvetica", 12), wrap=WORD, bd=2) 
result_text.pack(pady=10) 
# Start the Tkinter main loop 
root.mainloop() 
# Close the database connection
conn.close() 
