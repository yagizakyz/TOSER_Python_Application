from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter import messagebox
from datetime import date

connection = connect("toserdb.db")
cursor = connection.cursor()
def personel_Page():
    def insertPersonel():
        cursor.execute("INSERT INTO PersonelTable(Name, Surname, PIN, StartDate, Passive, Wage) VALUES (?, ?, ?, ?, false, ?)",
                       (nameENT.get(), snameENT.get(), int(pinENT.get()), startdENT.get(), int(wageENT.get())))
        messagebox.showinfo("Başarılı", "Veri Ekleme Başarılı")
        connection.commit()

    def updateWage():
        cursor.execute("UPDATE PersonelTable SET Wage = ? Where Personel_Id = ?",
                (int(wageENT.get()), int(idENT.get())))
        messagebox.showinfo("Başarılı", "Veri Maaş Güncelleme Başarılı")
        connection.commit()

    def istenCikar():
        cursor.execute("UPDATE PersonelTable SET EndDate = ?, Passive = true Where Personel_Id = ?",
                       (date.today(), int(idENT.get())))
        messagebox.showinfo("Başarılı", nameENT.get() + " " + snameENT.get() + " İşten Çıkarma Başarılı")
        connection.commit()

    pen = Tk()
    pen.title("TOSER - Personel Sayfası")
    pen.config(bg="#a8ccf7")
    pen.geometry("1000x600+40+30")

    toser = Label(pen, text="Personel Sayfası", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    #region tablo
    columns = ('personel_id', 'name', 'surname', 'start_date', 'end_date', 'passive', 'wage')

    tree = ttk.Treeview(pen, columns=columns, show='headings')

    tree.column('personel_id', width=110, anchor=W)
    tree.column('name', width=110, anchor=W)
    tree.column('surname', width=110, anchor=W)
    tree.column('start_date', width=110, anchor=W)
    tree.column('end_date', width=110, anchor=W)
    tree.column('passive', width=110, anchor=W)
    tree.column('wage', width=110, anchor=W)

    # define headings
    tree.heading('personel_id', text='Personel ID')
    tree.heading('name', text='Ad')
    tree.heading('surname', text='Soyad')
    tree.heading('start_date', text='İşe Giriş Tarihi')
    tree.heading('end_date', text='İşten Çıkış Tarihi')
    tree.heading('passive', text='Pasiflik')
    tree.heading('wage', text='Maaş')

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            idENT.delete(0, "end")
            idENT.insert(0, str(record[0]))

            nameENT.delete(0, "end")
            nameENT.insert(0, str(record[1]))

            snameENT.delete(0, "end")
            snameENT.insert(0, str(record[2]))

            startdENT.delete(0, "end")
            startdENT.insert(0, str(record[3]))

            wageENT.delete(0, "end")
            wageENT.insert(0, str(record[6]))

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    contacts = []
    cursor.execute("SELECT Personel_Id, Name, Surname, StartDate, EndDate, Passive, Wage FROM PersonelTable")
    personelKayitlari = cursor.fetchall()

    for m in personelKayitlari:
        contacts.append((m[0], m[1], m[2], m[3], m[4], m[5], m[6]))

    for contact in contacts:
        tree.insert('', END, values=contact)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(pen, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')
    #endregion

    frame = Frame(pen, width=300, height=400, bg="#a8ccf7")
    frame.grid_propagate(0)
    frame.grid(row=2, column=0)

    # region veri giriş hazırlama
    idLBL = Label(frame, text="Personel ID: ", bg="#a8ccf7")
    idENT = Entry(frame)

    nameLBL = Label(frame, text="Personel Ad: ", bg="#a8ccf7")
    nameENT = Entry(frame)

    snameLBL = Label(frame, text="Personel Soyad: ", bg="#a8ccf7")
    snameENT = Entry(frame)

    pinLBL = Label(frame, text="PIN: ", bg="#a8ccf7")
    pinENT = Entry(frame)

    startdLBL = Label(frame, text="İşe Giriş Tarihi: ", bg="#a8ccf7")
    startdENT = Entry(frame)

    wageLBL = Label(frame, text="Maaş: ", bg="#a8ccf7")
    wageENT = Entry(frame)

    insertBTN = Button(frame, text="Ekle", bg="white", command=insertPersonel)
    wageBTN = Button(frame, text="Maaş Güncelle", bg="white", command=updateWage)
    cikarBTN = Button(frame, text="İşten Çıkar", bg="white", command=istenCikar)

    # endregion

    idLBL.grid(row=2, column=2, sticky=W)
    idENT.grid(row=2, column=3, sticky=W)

    nameLBL.grid(row=3, column=2, sticky=W)
    nameENT.grid(row=3, column=3, sticky=W)

    snameLBL.grid(row=4, column=2, sticky=W)
    snameENT.grid(row=4, column=3, sticky=W)

    pinLBL.grid(row=5, column=2, sticky=W)
    pinENT.grid(row=5, column=3, sticky=W)

    startdLBL.grid(row=6, column=2, sticky=W)
    startdENT.grid(row=6, column=3, sticky=W)

    wageLBL.grid(row=7, column=2, sticky=W)
    wageENT.grid(row=7, column=3, sticky=W)

    insertBTN.grid(row=8, column=1)
    wageBTN.grid(row=8, column=2)
    cikarBTN.grid(row=8, column=3)

    pen.mainloop()
