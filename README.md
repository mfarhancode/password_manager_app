# Multi-Backend Desktop Password Manager

A local graphical vault application built in Python using Tkinter to compare data persistence, serialization, and storage models across four unique file systems.

## Project Structure
The repository contains four standalone storage variations of the same core application:
- **`password_manager_txt`**: Manages credentials using flat string parsing separated by a custom pipe delimiter (`|`).
- **`password_manager_csv`**: Implements structured tabular storage using Python's native `csv` reader and writer protocols.
- **`password_manager_json`**: Organizes data hierarchically using standard JavaScript Object Notation (`.json`) with structured exception handling (`try-except-else-finally`).
- **`password_manager_shelve`**: Uses standard binary persistent object storage (`shelve`) to securely serialize credential dictionaries into a key-value store.

## Features
- **Data Architecture Isolation:** Clean separation between the graphical user interface layer and the data persistence layers.
- **Dynamic Password Generator:** Shuffles and maps structural letters, punctuation symbols, and numeric characters to form complex user strings.
- **Smart Record Overwriting:** Checks the specific store for existing domain-username conflicts before programmatically rewriting entries.
- **Clipboard Integration:** Instantly copies newly generated or queried passwords directly to your local system clipboard using `pyperclip`.
