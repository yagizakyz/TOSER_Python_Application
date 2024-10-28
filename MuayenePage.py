from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter import messagebox
from datetime import date

connection = connect("toserdb.db")
cursor = connection.cursor()
def muayene_Page():
    def insertMuayene():
        cursor.execute("INSERT INTO MuayeneTable(Plate, EntryDate, Amount, DriverID, PersonelID) VALUES (?, ?, ?, ?, ?)",
                       (plateENT.get(), date.today(), int(amountENT.get()), int(driverENT.get()), int(personENT.get())))
        messagebox.showinfo("Başarılı", "Veri Ekleme Başarılı")
        connection.commit()

    def updateLeavingDate():
        cursor.execute(
            "UPDATE MuayeneTable SET LeavingDate = ?, Amount = ? Where MuayeneId = ?",
            (date.today(), int(amountENT.get()), int(idENT.get())))
        messagebox.showinfo("Başarılı", "Veri Güncelleme Başarılı")
        connection.commit()


    pen = Tk()

    pen.title("TOSER - Muayene Sayfası")
    pen.config(bg="#a8ccf7")
    pen.geometry("1000x600+40+30")

    toser = Label(pen, text="Muayene Sayfası", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    #region tablo
    columns = ('muayene_id', 'plate', 'entry_date', 'leaving_date', 'amount', 'driver_name', 'personel_name')

    tree = ttk.Treeview(pen, columns=columns, show='headings')

    tree.column('muayene_id', width=110, anchor=W)
    tree.column('plate', width=110, anchor=W)
    tree.column('entry_date', width=110, anchor=W)
    tree.column('leaving_date', width=110, anchor=W)
    tree.column('amount', width=110, anchor=W)
    tree.column('driver_name', width=110, anchor=W)
    tree.column('personel_name', width=110, anchor=W)

    # define headings
    tree.heading('muayene_id', text='Muayene ID')
    tree.heading('plate', text='Plaka')
    tree.heading('entry_date', text='Giriş Tarihi')
    tree.heading('leaving_date', text='Ayrılma Tarihi')
    tree.heading('amount', text='Tutar')
    tree.heading('driver_name', text='Şoför Adı')
    tree.heading('personel_name', text='Personel Adı')

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            idENT.delete(0, "end")
            idENT.insert(0, str(record[0]))

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    contacts = []
    cursor.execute("SELECT MuayeneTable.MuayeneId, MuayeneTable.Plate, MuayeneTable.EntryDate, MuayeneTable.LeavingDate, MuayeneTable.Amount, (DriverTable.DriverName || ' ' || DriverTable.DriverSurname) as Şoför, (PersonelTable.Name || ' ' || PersonelTable.Surname) as personel FROM MuayeneTable INNER JOIN DriverTable ON DriverTable.TCKN = MuayeneTable.DriverID INNER JOIN PersonelTable ON PersonelTable.Personel_Id = MuayeneTable.PersonelID")
    muayeneKayitlari = cursor.fetchall()

    for m in muayeneKayitlari:
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

    #region veri giriş hazırlama
    plateLBL = Label(frame, text="Plaka: ", bg="#a8ccf7")
    plateENT = Entry(frame)

    entryLBL = Label(frame, text="Giriş Tarihi: ", bg="#a8ccf7")
    entryENT = Entry(frame)

    leaveLBL = Label(frame, text="Çıkış Tarihi: ", bg="#a8ccf7")
    leaveENT = Entry(frame)

    amountLBL = Label(frame, text="Tutar: ", bg="#a8ccf7")
    amountENT = Entry(frame)

    driverLBL = Label(frame, text="Şoför TCKN: ", bg="#a8ccf7")
    driverENT = Entry(frame)

    personLBL = Label(frame, text="Personel ID: ", bg="#a8ccf7")
    personENT = Entry(frame)

    insertBTN = Button(frame, text="Ekle", bg="white", command=insertMuayene)
    updateBTN = Button(frame, text="Aracı Çıkar", bg="white", command=updateLeavingDate)

    idENT = Entry(frame)

    #endregion

    plateLBL.grid(row=2, column=2, sticky=W)
    plateENT.grid(row=2, column=3, sticky=W)

    entryLBL.grid(row=3, column=2, sticky=W)
    entryENT.grid(row=3, column=3, sticky=W)

    leaveLBL.grid(row=4, column=2, sticky=W)
    leaveENT.grid(row=4, column=3, sticky=W)

    amountLBL.grid(row=5, column=2, sticky=W)
    amountENT.grid(row=5, column=3, sticky=W)

    driverLBL.grid(row=6, column=2, sticky=W)
    driverENT.grid(row=6, column=3, sticky=W)

    personLBL.grid(row=7, column=2, sticky=W)
    personENT.grid(row=7, column=3, sticky=W)

    insertBTN.grid(row=8, column=3)
    updateBTN.grid(row=9, column=3)

    idENT.grid(row=11, column=3)
    idENT.insert(0, "Muayene ID")

    pen.mainloop()
