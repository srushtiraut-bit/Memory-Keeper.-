
# 📸 Memory Keeper

A Python-based desktop application to store, manage, and search personal photo memories with descriptions, tags, and dates.

---

## 📌 Overview

Memory Keeper allows users to:
- Upload images
- Add descriptions and tags
- Store memory dates
- Search memories easily
- View image previews inside the application

The project uses Tkinter for GUI and SQLite for database management.

---

## 🚀 Features

✔ Upload JPG, PNG, JPEG images  
✔ Add description and comma-separated tags  
✔ Date validation (DD/MM/YYYY format)  
✔ Search memories by description or tags  
✔ Automatic image storage in local folder  
✔ SQLite database integration  
✔ Image preview in search results  

---

## 🛠 Technologies Used

- Python  
- Tkinter (GUI)  
- SQLite3 (Database)  
- Pillow (PIL)  
- OS & Shutil modules  
- Regular Expressions (Regex)

---

## 🗄 Database Structure

**Table Name:** memories

| Column       | Type    |
|--------------|---------|
| id           | INTEGER (Primary Key) |
| photo_path   | TEXT    |
| description  | TEXT    |
| tags         | TEXT    |
| date         | TEXT    |

---

## 📂 Project Structure

