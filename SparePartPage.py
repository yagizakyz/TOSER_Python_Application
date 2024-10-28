from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter import messagebox
from datetime import date

connection = connect("toserdb.db")
cursor = connection.cursor()
def sparePart_Page():
    def insertParca():
        cursor.execute("INSERT INTO SparePartTable(Name, Stock) VALUES (?, ?)",
                       (nameENT.get(), int(stockENT.get())))
        messagebox.showinfo("Başarılı", "Veri Ekleme Başarılı")
        connection.commit()

    def stockArttir():
        cursor.execute(
            "UPDATE SparePartTable SET Stock = ? Where SparePartId = ?",
            (int(stockENT.get()), int(idENT.get())))
        messagebox.showinfo("Başarılı", "Veri Güncelleme Başarılı")
        connection.commit()

    def insertLog():
        cursor.execute("INSERT INTO SparePartLog(SparePartID, Description, Dates) VALUES (?, ?, ?)",
                       (int(sidENT.get()), descriptionENT.get(), date.today()))
        connection.commit()

        cursor.execute(
            "UPDATE SparePartTable SET Stock = ? Where SparePartId = ?",
            (int(stockENT.get())-1, int(sidENT.get())))
        messagebox.showinfo("Başarılı", "Parça Çıkarma Kaydı Başarılı")
        connection.commit()

    pen = Tk()

    pen.title("TOSER - Yedek Parça Sayfası")
    pen.config(bg="#a8ccf7")
    pen.geometry("1000x600+40+30")

    toser = Label(pen, text="Yedek Parça Sayfası", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    #region tablo
    columns = ('sparepart_id', 'name', 'stock')

    tree = ttk.Treeview(pen, columns=columns, show='headings')

    tree.column('sparepart_id', width=110, anchor=W)
    tree.column('name', width=110, anchor=W)
    tree.column('stock', width=110, anchor=W)

    # define headings
    tree.heading('sparepart_id', text='Parça ID')
    tree.heading('name', text='Parça Ad')
    tree.heading('stock', text='Stok Sayısı')

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            idENT.delete(0, "end")
            idENT.insert(0, str(record[0]))

            sidENT.delete(0, "end")
            sidENT.insert(0, str(record[0]))

            nameENT.delete(0, "end")
            nameENT.insert(0, str(record[1]))

            stockENT.delete(0, "end")
            stockENT.insert(0, str(record[2]))

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    contacts = []
    cursor.execute("SELECT * FROM SparePartTable")
    parcaKayitlari = cursor.fetchall()

    for s in parcaKayitlari:
        contacts.append((s[0], s[1], s[2]))

    for contact in contacts:
        tree.insert('', END, values=contact)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(pen, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')
    #endregion

    #region log tablo
    logtFrame = Frame(pen, width=700, height=400, bg="#a8ccf7")
    logtFrame.grid_propagate(0)
    logtFrame.grid(row=1, column=2)

    columns1 = ('id', 'name', 'description', 'dates')

    tree1 = ttk.Treeview(logtFrame, columns=columns1, show='headings')

    tree1.column('id', width=110, anchor=W)
    tree1.column('name', width=110, anchor=W)
    tree1.column('description', width=180, anchor=W)
    tree1.column('dates', width=110, anchor=W)

    # define headings
    tree1.heading('id', text='Parça Ad')
    tree1.heading('name', text='Parça Ad')
    tree1.heading('description', text='Açıklama')
    tree1.heading('dates', text='Tarih')

    tree1.grid(row=1, column=0, sticky='nsew')

    contacts1 = []
    cursor.execute(
        "SELECT LogID, SparePartTable.Name, Description, Dates FROM SparePartLog INNER JOIN SparePartTable ON SparePartTable.SparePartId = SparePartLog.SparePartID")
    logKayitlari = cursor.fetchall()

    for f in logKayitlari:
        contacts1.append((f[0], f[1], f[2], f[3]))

    for contact in contacts1:
        tree1.insert('', END, values=contact)

    #endregion

    frame = Frame(pen, width=300, height=400, bg="#a8ccf7")
    frame.grid_propagate(0)
    frame.grid(row=2, column=0)

    #region veri giriş hazırlama
    idLBL = Label(frame, text="Parça ID: ", bg="#a8ccf7")
    idENT = Entry(frame)

    nameLBL = Label(frame, text="Parça Ad: ", bg="#a8ccf7")
    nameENT = Entry(frame)

    stockLBL = Label(frame, text="Stok Sayısı: ", bg="#a8ccf7")
    stockENT = Entry(frame)

    insertBTN = Button(frame, text="Ekle", bg="white", command=insertParca)
    supdateBTN = Button(frame, text="Stok Güncelle", bg="white", command=stockArttir)
    #endregion

    #region log girişi hazırlama

    logvFrame = Frame(pen, width=400, height=400, bg="#a8ccf7")
    logvFrame.grid_propagate(0)
    logvFrame.grid(row=2, column=2)

    lidLBL = Label(logvFrame, text="Log ID: ", bg="#a8ccf7")
    lidENT = Entry(logvFrame)

    sidLBL = Label(logvFrame, text="Parça ID: ", bg="#a8ccf7")
    sidENT = Entry(logvFrame)

    descriptionLBL = Label(logvFrame, text="Açıklama: ", bg="#a8ccf7")
    descriptionENT = Entry(logvFrame)

    logInsertBTN = Button(logvFrame, text="Ekle", bg="white", command=insertLog)

    #endregion

    idLBL.grid(row=2, column=2, sticky=W)
    idENT.grid(row=2, column=3, sticky=W)

    nameLBL.grid(row=3, column=2, sticky=W)
    nameENT.grid(row=3, column=3, sticky=W)

    stockLBL.grid(row=4, column=2, sticky=W)
    stockENT.grid(row=4, column=3, sticky=W)

    insertBTN.grid(row=5, column=2)
    supdateBTN.grid(row=5, column=3)

    lidLBL.grid(row=2, column=2, sticky=W)
    lidENT.grid(row=2, column=3, sticky=W)

    sidLBL.grid(row=3, column=2, sticky=W)
    sidENT.grid(row=3, column=3, sticky=W)

    descriptionLBL.grid(row=4, column=2, sticky=W)
    descriptionENT.grid(row=4, column=3, sticky=W)

    logInsertBTN.grid(row=5, column=2)

    pen.mainloop()
