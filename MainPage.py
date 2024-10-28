from tkinter import *
from MuayenePage import muayene_Page
from CompanyPage import company_Page
from DriverPage import driver_Page
from PersonelPage import personel_Page
from SparePartPage import sparePart_Page

def main_Page():
    pen = Tk()

    pen.title("TOSER - Ana Sayfa")
    pen.config(bg="#a8ccf7")
    pen.geometry("800x600+40+30")

    def muayene():
        muayene_Page()

    def company():
        company_Page()

    def driver():
        driver_Page()

    def personel():
        personel_Page()

    def sparePart():
        sparePart_Page()

    muayeneBTN = Button(pen, text="Muayene Sayfası", bg="white", command=muayene)
    muayeneLBL = Label(pen, text="Muayene kayıtları\ngörüntüleme, ekleme ve düzenleme", bg="#a8ccf7")

    companyBTN = Button(pen, text="Firma Sayfası", bg="white", command=company)
    companyLBL = Label(pen, text="Firma görüntüleme ve ekleme", bg="#a8ccf7")

    driverBTN = Button(pen, text="Şoför Sayfası", bg="white", command=driver)
    driverLBL = Label(pen, text="Şoför görüntüleme ve ekleme", bg="#a8ccf7")

    personelBTN = Button(pen, text="Personel Sayfası", bg="white", command=personel)
    personelLBL = Label(pen, text="Personel\ngörüntüleme, ekleme ve düzenleme", bg="#a8ccf7")

    sparePartBTN = Button(pen, text="Yedek Parça Sayfası", bg="white", command=sparePart)
    sparePartLBL = Label(pen, text="Yedek parça\ngörüntüleme, ekleme ve depodan çıkarma", bg="#a8ccf7")

    toser = Label(pen, text="TOSER", bg="#a8ccf7", font="25px")
    toser.grid(row=0, column=0, sticky="W")

    muayeneBTN.grid(row=1, column=0)
    muayeneLBL.grid(row=2, column=0)

    companyBTN.grid(row=1, column=1)
    companyLBL.grid(row=2, column=1)

    driverBTN.grid(row=1, column=2)
    driverLBL.grid(row=2, column=2)

    bosluk = Label(pen, text="   \n    ", bg="#a8ccf7")
    bosluk.grid(row=3, column=0)

    personelBTN.grid(row=4, column=0)
    personelLBL.grid(row=5, column=0)

    sparePartBTN.grid(row=4, column=2)
    sparePartLBL.grid(row=5, column=2)

    pen.mainloop()