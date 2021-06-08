from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk,ImageGrab,Image
from io import BytesIO
from glob import glob
from pymysql.cursors import DictCursor

import time
import tkinter as tk
import tkinter.ttk as ttk
import pypyodbc
import random
import cv2
import qrcode
import pymysql

window = tk.Tk()
window.title("QR сканер")
window.geometry()
window.resizable()

passwords=''
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def rand ():
    global passwords
    for x in range (1):
        passwords = ''

        for i in range (12):
            passwords += random.choice(chars)
            mylabel = tk.Label(window, text = passwords)
            mylabel.grid(column=1, row=4)
    file = open("password.txt", "w")
    file.write(passwords)
    file.close()
    
def history():
    global passwords
    if passwords=='':
        mb.showerror("Ошибка", "Учетная запись не подключена!")
    else:
        try:
            connection = pymysql.connect(
            host='remotemysql.com',
            user='NnJkRbCiAY',
            password='nxvzewI7Q3',
            db='NnJkRbCiAY',
            charset='utf8mb4',
            cursorclass=DictCursor
            )
            print('success')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT `link` FROM `{0}` WHERE 1".format(passwords))
                    rowss = cursor.fetchall()
                    ab=8
                    for rows in rowss:
                        label1=tk.Entry(window, width=40)
                        label1.insert(0, rows)
                        label1.grid(column=1, row=ab)
                        ab+=1
                    connection.close()
            except Exception:
                mb.showerror("Ошибка", "Список пуст!")
                connection.close()

        finally:
            print("")



def spravka():
    mb.showinfo("Справка!", "1.Для работы с программой выберете файл с учетной записью в виде\
    12 символов в txt файле.\nИли сгенерируйте новую. ПРИ ГЕНЕРЕАЦИИ ФАЙЛ ПЕРЕЗАПИСЫВАЕТСЯ.\n2.\
    При помощи комбинации 'win'+shift+s сделайте скриншот ТОЛЬКО qr-кода.\n3.Нажмите 'распознать'\n Если уч. запись подключена результат запишется в онлайн-базу\n\
    Нажмите история, чтобы посмотреть все просканированные коды")

def otkr():
    global passwords
    file_text = fd.askopenfilename(title = "Select file", filetypes= (("txt Files","*.txt"),))
    with open(file_text,"r") as f:
         passwords = f.read(12)
         mylabel = tk.Label(window, text = passwords)
         mylabel.grid(column=1, row=4)
         

def qropen():
        global passwords
        try:
            presentItem = ImageGrab.grabclipboard()
            presentItem.save("qr-code.png")
        #mb.showinfo("Готово!", "Потребуется краски - {0}л\nпри стоимости {1}р")
        except AttributeError:
            mb.showerror("Ошибка", "Выделен не qr-code или не изображение")
            return
    
        try:
            im = Image.open("qr-code.png")
        except FileNotFoundError:
            mb.showerror("Ошибка", "Изображение не найдено")
            return
    
        time.sleep(1)
        try:
            rgb_im = im.convert('RGB')
            rgb_im.save('qr-code.jpg')
        except UnboundLocalError:
            mb.showerror("Ошибка", "Конвертирование не выполнено. Программа работает только с jpg")
            return    
        time.sleep(2)
        try:
            img_qrcode = cv2.imread("qr-code.jpg")
            detector = cv2.QRCodeDetector()
            data, bbox, clear_qrcode = detector.detectAndDecode(img_qrcode)
            label1=tk.Entry(window, width=20)
            label1.insert(0, data)
            label1.grid(column=1, row=7)
            mb.showinfo("Готово!", "QR-code распознан!  {0}".format(data))
        except Exception:
            mb.showerror("Ошибка", "QR-code не распознан. Попробуйте ещё раз")
        
        if passwords=='':print(1)
        else:
            try:
                connection = pymysql.connect(
                host='remotemysql.com',
                user='NnJkRbCiAY',
                password='nxvzewI7Q3',
                db='NnJkRbCiAY',
                charset='utf8mb4',
                cursorclass=DictCursor
                )
                print('success')
                 
                try:
                    with connection.cursor() as cursor:
                    #cursor.execute ("CREATE TABLE {}(ID INT, LINK CHAR(99))".format(passwords));
                        cursor.execute ("CREATE TABLE `{0}`(`id` int(11) NOT NULL AUTO_INCREMENT,`link` varchar(255) COLLATE utf8_bin NOT NULL,PRIMARY KEY (`id`)) AUTO_INCREMENT=1 ;".format(passwords))
                        cursor.execute ("INSERT INTO `{0}`(`link`) VALUES ('{1}');".format(passwords, data)) 
                        connection.commit()
                        connection.close()
                        print("table create")
                except Exception:
                    with connection.cursor() as cursor:
                        cursor.execute ("INSERT INTO `{0}`(`link`) VALUES ('{1}');".format(passwords, data)) 
                        connection.commit()
                        connection.close()
            finally:
                print("")    
            
tk.Label (window, text = 'Для сохранения\n результатов сканирования\n выберете или создайте\n уч. запись').grid(column=1,row=1)

my_img2 = ImageTk.PhotoImage(Image.open ('pass.png'))
Label (image=my_img2).grid(column=1, row=2)

tk.Button(window, command=spravka, text='???').grid(column=2, row=1)

tk.Button(window, text='Открыть', command=otkr, width=13).grid(column=0, row=4)

tk.Button(window, command=rand, text='Сгенерировать', width=13).grid(column=2, row=4)

my_img3 = ImageTk.PhotoImage(Image.open ('th.jpg'))    
Label (image=my_img3).grid(column=1, row=5)

tk.Label (window, text = 'Для выделения кода \nнажмите "Win"+Shift+S').grid(column=1,row=6)

tk.Button(window, command=qropen, text='Распознать', width=13).grid(column=0, row=7)

tk.Button(window, command=history, text='История', width=13).grid(column=2, row=7)

window.mainloop()


