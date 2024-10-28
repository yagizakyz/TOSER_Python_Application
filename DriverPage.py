from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter import messagebox

connection = connect("toserdb.db")
cursor = connection.cursor()
def driver_Page():
    def insertDriver():
        cursor.execute("INSERT INTO DriverTable(TCKN, DriverName, DriverSurname, CompanyID) VALUES (?, ?, ?, ?)",
                       (idENT.get(), nameENT.get(), snameENT.get(), cidENT.get()))
        messagebox.showinfo("Başarılı", "Veri Ekleme Başarılı")
        connection.commit()

    def updateDriver():
        cursor.execute(
            "UPDATE DriverTable SET DriverName = ?, DriverSurname = ?, CompanyID = ? Where TCKN = ?",
            (nameENT.get(), snameENT.get(), cidENT.get(), int(idENT.get())))
        messagebox.showinfo("Başarılı", "Veri Güncelleme Başarılı")
        connection.commit()

    pen = Tk()

    pen.title("TOSER - Şoförler Sayfası")
    pen.config(bg="#a8ccf7")
    pen.geometry("1000x600+40+30")

    toser = Label(pen, text="Şoförler Sayfası", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    #region tablo
    columns = ('tckn', 'driver_name', 'driver_surname', 'company_name')

    tree = ttk.Treeview(pen, columns=columns, show='headings')

    tree.column('tckn', width=110, anchor=W)
    tree.column('driver_name', width=110, anchor=W)
    tree.column('driver_surname', width=110, anchor=W)
    tree.column('company_name', width=110, anchor=W)

    # define headings
    tree.heading('tckn', text='TCKN')
    tree.heading('driver_name', text='Şoför Ad')
    tree.heading('driver_surname', text='Şoför Soyad')
    tree.heading('company_name', text='Firma Ad')

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

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    contacts = []
    cursor.execute("SELECT DriverTable.TCKN, DriverTable.DriverName, DriverTable.DriverSurname, CompanyTable.CompanyName FROM DriverTable INNER JOIN CompanyTable ON DriverTable.CompanyID = CompanyTable.CompanyId")
    soforKayitlari = cursor.fetchall()

    for s in soforKayitlari:
        contacts.append((s[0], s[1], s[2], s[3]))

    for contact in contacts:
        tree.insert('', END, values=contact)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(pen, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')
    #endregion

    #region firma tablo
    firmaFrame = Frame(pen, width=300, height=400, bg="#a8ccf7")
    firmaFrame.grid_propagate(0)
    firmaFrame.grid(row=1, column=2)

    columns1 = ('company_id', 'company_name')

    tree1 = ttk.Treeview(firmaFrame, columns=columns1, show='headings')

    tree1.column('company_id', width=110, anchor=W)
    tree1.column('company_name', width=110, anchor=W)

    # define headings
    tree1.heading('company_id', text='Firma ID')
    tree1.heading('company_name', text='Firma Ad')

    def item_selected(event):
        for selected_item in tree1.selection():
            item = tree1.item(selected_item)
            record = item['values']
            # show a message
            cidENT.delete(0, "end")
            cidENT.insert(0, str(record[0]))

    tree1.bind('<<TreeviewSelect>>', item_selected)

    tree1.grid(row=1, column=0, sticky='nsew')

    contacts1 = []
    cursor.execute(
        "SELECT CompanyId, CompanyName FROM CompanyTable")
    firmaKayitlari = cursor.fetchall()

    for f in firmaKayitlari:
        contacts1.append((f[0], f[1]))

    for contact in contacts1:
        tree1.insert('', END, values=contact)

    """# add a scrollbar
    scrollbar1 = ttk.Scrollbar(pen, orient=VERTICAL, command=tree.yview)
    tree1.configure(yscroll=scrollbar1.set)
    scrollbar1.grid(row=1, column=3, sticky='ns')"""

    #endregion

    frame = Frame(pen, width=300, height=400, bg="#a8ccf7")
    frame.grid_propagate(0)
    frame.grid(row=2, column=0)

    #region veri giriş hazırlama
    idLBL = Label(frame, text="TCKN: ", bg="#a8ccf7")
    idENT = Entry(frame)

    nameLBL = Label(frame, text="Şoför Ad: ", bg="#a8ccf7")
    nameENT = Entry(frame)

    snameLBL = Label(frame, text="Şoför Soyad: ", bg="#a8ccf7")
    snameENT = Entry(frame)

    cidLBL = Label(frame, text="Firma ID: ", bg="#a8ccf7")
    cidENT = Entry(frame)

    insertBTN = Button(frame, text="Ekle", bg="white", command=insertDriver)
    updateBTN = Button(frame, text="Güncelle", bg="white", command=updateDriver)

    #endregion

    idLBL.grid(row=2, column=2, sticky=W)
    idENT.grid(row=2, column=3, sticky=W)

    nameLBL.grid(row=3, column=2, sticky=W)
    nameENT.grid(row=3, column=3, sticky=W)

    snameLBL.grid(row=4, column=2, sticky=W)
    snameENT.grid(row=4, column=3, sticky=W)

    cidLBL.grid(row=5, column=2, sticky=W)
    cidENT.grid(row=5, column=3, sticky=W)

    insertBTN.grid(row=6, column=3)
    updateBTN.grid(row=7, column=3)

    pen.mainloop()
