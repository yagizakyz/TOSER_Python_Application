import tkinter as tk
from sqlite3 import *
from MainPage import main_Page

window = tk.Tk()
window.title("TOSER - Giriş Sayfası")
window.config(bg="#a8ccf7")
window.geometry("350x350+40+30")

connection = connect("toserdb.db")
cursor = connection.cursor()
def login():
    cursor.execute("SELECT * FROM PersonelTable WHERE PIN = " + str(entry.get()) + " AND Passive = 0")
    user = cursor.fetchone()

    if(user):
        window.destroy()
        main_Page()
    else:
        tk.messagebox.showerror("Hatalı Giriş", "Geçersiz PIN!")
        entry.delete(0, "end")

label = tk.Label(text="Lütfen PIN girin:", bg="#a8ccf7")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(text="Giriş", command=login)
button.pack()

window.mainloop()