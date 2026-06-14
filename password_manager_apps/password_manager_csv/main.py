from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
from pathlib import Path
import csv

# ---------------------------- CONSTANTS & SETUP ------------------------------- #
BG_COLOR = "#f4f4f2"
PRIMARY_COLOR = "#3e4a61"
ACCENT_COLOR = "#ec7373"
FONT_NAME = "Verdana"

csv_path = Path(__file__).parent.joinpath('data.csv')

def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters = list(letters) + list(letters.upper())
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    password_list = []
    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo('Password Manager', 'Password copied to clipboard')


def check_data(website, email, get_password=False):
    if not csv_path.exists():
        with open('data.csv',mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['website','email_or_username','password'])
        return False
    with csv_path.open(newline='', encoding='utf-8') as data:
        reader = csv.reader(data)
        header = next(reader)
        for row in reader:
            if len(row) == 3:
                web, eml, pswrd = row
                if web == website and eml == email:
                    return (True, pswrd) if get_password else True
    return False

# print(check_data('instagram.com','farhan@gmail.com', get_password=True))


def overwrite_data(website, email, password):
    update_pass = messagebox.askokcancel(title=website, message=f'You have already added this website with this email/username.\nDo you want to update the password?')
    if update_pass:
        # save all the data in list
        with csv_path.open(newline='', encoding='utf-8') as f:
            lines = list(csv.reader(f))
        # write whole file from scratch again, to update that password
        with csv_path.open('w',newline='', encoding='utf-8') as data:
            writer = csv.writer(data)
            for line in lines:
                if len(line) == 3:
                    w,e,p = line
                    if w == website and e == email:
                        writer.writerow([website, email, password])
                    else:
                        writer.writerow(line)
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo('Success', 'Data updated successfully')

def add_data():
    website = website_entry.get().lower().strip()
    email = email_entry.get().lower().strip()
    password = password_entry.get().strip()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='Error', message='Please do not leave any fields empty')
    else:
        # check if email and website already exists
        if check_data(website, email):
            overwrite_data(website, email, password)
            return

        # add new data
        is_ok = messagebox.askokcancel(title=website, message=f'Details entered: \nEmail: {email} \nPassword: {password} \nSave this?')
        if is_ok:
            # to check if there is any empty line at end
            with csv_path.open('r', encoding='utf-8') as f:
                last_line = None
                for last_line in f:
                    pass
            with csv_path.open('a',newline='', encoding='utf-8') as data:
                writer = csv.writer(data)
                row_to_add = [website, email, password]
                if last_line and not last_line.endswith('\n'):
                    data.write('\n')
                writer.writerow(row_to_add)
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo('Success', 'Data saved succesfully')

def find_password():
    website = website_entry.get().lower()
    email = email_entry.get().lower()
    if len(website) == 0 or len(email) == 0:
        messagebox.showinfo(title='Error', message='Enter both Website and Email to search')
        return
    
    result = check_data(website, email, get_password=True)
    if isinstance(result, tuple):
        pswrd = result[1]
        pyperclip.copy(pswrd)
        messagebox.showinfo(website.title(), f'Email: {email}\nPassword: {pswrd}\n\n(Password copied to clipboard)')
        # print(check_data(website, email))
    else:
        messagebox.showinfo('Password Manager', 'No data found')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('MyPass | Password Manager')
window.config(padx=60, pady=50, bg=BG_COLOR)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_path = Path(__file__).parent.joinpath('logo.png')
logo = PhotoImage(file=logo_path)
canvas.create_image((100,100),image=logo)
canvas.grid(row=0, column=1, pady=(0, 20))

# Labels
def create_label(text, row, col):
    lbl = Label(text=text, font=(FONT_NAME, 10, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR)
    lbl.grid(row=row, column=col, sticky="e", padx=10, pady=5)

create_label("Website:", 1, 0)
create_label("Email/Username:", 2, 0)
create_label("Password:", 3, 0)

# Entries
website_entry = Entry(width=30, font=(FONT_NAME, 10))
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="w")

email_entry = Entry(width=50, font=(FONT_NAME, 10))
email_entry.insert(0, 'name@gmail.com')
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

password_entry = Entry(width=30, font=(FONT_NAME, 10))
password_entry.grid(row=3, column=1, sticky="w")

# Buttons
find_pass_btn = Button(text='Search Vault', width=15, bg=PRIMARY_COLOR, fg="white", 
                       command=find_password, relief="flat", cursor="hand2")
find_pass_btn.grid(row=1, column=2, sticky="w")

generate_pass_btn = Button(text='Generate', width=15, bg=PRIMARY_COLOR, fg="white", 
                           command=generate_password, relief="flat", cursor="hand2")
generate_pass_btn.grid(row=3, column=2, sticky="w")

add_btn = Button(text='Save to Vault', width=42, bg=ACCENT_COLOR, fg="white", 
                 font=(FONT_NAME, 10, "bold"), command=add_data, relief="flat", cursor="hand2")
add_btn.grid(row=4, column=1, columnspan=2, pady=30)

window.mainloop()
