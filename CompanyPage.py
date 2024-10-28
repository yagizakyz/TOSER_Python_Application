from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter import messagebox
from datetime import date

connection = connect("toserdb.db")
cursor = connection.cursor()
def company_Page():
    def insertCompany():
        cursor.execute("INSERT INTO CompanyTable(CompanyName, TaxNumber, TaxAdministration, Address) VALUES (?, ?, ?, ?)",
                       (nameENT.get(), tnumberENT.get(), tadminENT.get(), addressENT.get()))
        messagebox.showinfo("Başarılı", "Veri Ekleme Başarılı")
        connection.commit()

    def updateCompany():
        cursor.execute(
            "UPDATE CompanyTable SET CompanyName = ?, TaxNumber = ?, TaxAdministration = ?, Address = ? Where CompanyId = ?",
            (nameENT.get(), tnumberENT.get(), tadminENT.get(), addressENT.get(), int(idENT.get())))
        messagebox.showinfo("Başarılı", "Veri Güncelleme Başarılı")
        connection.commit()

    pen = Tk()

    pen.title("TOSER - Firmalar Sayfası")
    pen.config(bg="#a8ccf7")
    pen.geometry("1000x600+40+30")

    toser = Label(pen, text="Firmalar Sayfası", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    #region tablo
    columns = ('company_id', 'company_name', 'tax_number', 'tax_administration', 'address')

    tree = ttk.Treeview(pen, columns=columns, show='headings')

    tree.column('company_id', width=110, anchor=W)
    tree.column('company_name', width=110, anchor=W)
    tree.column('tax_number', width=110, anchor=W)
    tree.column('tax_administration', width=110, anchor=W)
    tree.column('address', width=110, anchor=W)

    # define headings
    tree.heading('company_id', text='Firma ID')
    tree.heading('company_name', text='Firma Ad')
    tree.heading('tax_number', text='Vergi NO')
    tree.heading('tax_administration', text='Vergi Dairesi')
    tree.heading('address', text='Adres')

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            idENT.delete(0, "end")
            idENT.insert(0, str(record[0]))

            nameENT.delete(0, "end")
            nameENT.insert(0, str(record[1]))

            tnumberENT.delete(0, "end")
            tnumberENT.insert(0, str(record[2]))

            tadminENT.delete(0, "end")
            tadminENT.insert(0, str(record[3]))

            addressENT.delete(0, "end")
            addressENT.insert(0, str(record[4]))

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    contacts = []
    cursor.execute("SELECT * From CompanyTable")
    firmaKayitlari = cursor.fetchall()

    for f in firmaKayitlari:
        contacts.append((f[0], f[1], f[2], f[3], f[4]))

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
    idLBL = Label(frame, text="Firma ID: ", bg="#a8ccf7")
    idENT = Entry(frame)

    nameLBL = Label(frame, text="Firma Ad: ", bg="#a8ccf7")
    nameENT = Entry(frame)

    tnumberLBL = Label(frame, text="Vergi NO: ", bg="#a8ccf7")
    tnumberENT = Entry(frame)

    tadminLBL = Label(frame, text="Vergi Dairesi: ", bg="#a8ccf7")
    tadminENT = Entry(frame)

    addressLBL = Label(frame, text="Adres: ", bg="#a8ccf7")
    addressENT = Entry(frame)

    insertBTN = Button(frame, text="Ekle", bg="white", command=insertCompany)
    updateBTN = Button(frame, text="Güncelle", bg="white", command=updateCompany)

    #endregion

    idLBL.grid(row=2, column=2, sticky=W)
    idENT.grid(row=2, column=3, sticky=W)

    nameLBL.grid(row=3, column=2, sticky=W)
    nameENT.grid(row=3, column=3, sticky=W)

    tnumberLBL.grid(row=4, column=2, sticky=W)
    tnumberENT.grid(row=4, column=3, sticky=W)

    tadminLBL.grid(row=5, column=2, sticky=W)
    tadminENT.grid(row=5, column=3, sticky=W)

    addressLBL.grid(row=6, column=2, sticky=W)
    addressENT.grid(row=6, column=3, sticky=W)

    insertBTN.grid(row=7, column=3)
    updateBTN.grid(row=8, column=3)

    pen.mainloop()
