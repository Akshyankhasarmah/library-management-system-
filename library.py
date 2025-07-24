import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox


class library():
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="light gray")
        self.root.title("Library Management")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        label = tk.Label(self.root, bg=self.clr(200, 100, 180), bd=3, fg="white", relief="groove",
                         text="Library Management", font=("Arial", 50, "bold"))
        label.pack(side="top", fill="x")

        # Input frame
        inFrame = tk.Frame(self.root, bg=self.clr(
            150, 100, 220), bd=4, relief="ridge")
        inFrame.place(width=self.width/3, height=self.height-180, x=80, y=100)

        tk.Button(inFrame, command=self.regFun, text="Register Student", bg="light green", bd=2,
                  font=("Arial", 15, "bold"), width=20).grid(row=0, column=0, padx=80, pady=80)

        tk.Button(inFrame, command=self.resBook, text="Reserve Book", bg="light green", bd=2,
                  font=("Arial", 15, "bold"), width=20).grid(row=1, column=0, padx=80, pady=60)

        tk.Button(inFrame, command=self.retFun, text="Return Book", bg="light green", bd=2,
                  font=("Arial", 15, "bold"), width=20).grid(row=2, column=0, padx=80, pady=60)

        # List Frame
        self.listFrame = tk.Frame(
            self.root, bd=4, relief="groove", bg=self.clr(120, 220, 100))
        self.listFrame.place(width=self.width/2,
                             height=self.height-180, x=self.width/3+130, y=100)

        self.tabFun()
        self.showBk()

    def tabFun(self):
        tabFrame = tk.Frame(self.listFrame, bd=4,
                            relief="sunken", bg=self.clr(200, 100, 110))
        tabFrame.place(width=self.width/2-60,
                       height=self.height-280, x=30, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, columns=("bId", "bname", "quant"),
                                  xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("bId", text="Book_ID")
        self.table.heading("bname", text="Book_Name")
        self.table.heading("quant", text="Quantity")
        self.table["show"] = "headings"

        self.table.column("bId", width=170)
        self.table.column("bname", width=170)
        self.table.column("quant", width=170)

        self.table.pack(fill="both", expand=1)

    def regFun(self):
        self.clearFrames()
        self.regFrame = tk.Frame(
            self.root, bd=3, relief="ridge", bg=self.clr(150, 150, 150))
        self.regFrame.place(width=self.width/3,
                            height=self.height-180, x=self.width/3+120, y=100)

        tk.Label(self.regFrame, text="RollNo:", bg=self.clr(150, 150, 150), fg="white",
                 font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=30)
        self.rnIn_reg = tk.Entry(
            self.regFrame, font=("Arial", 15, "bold"), width=20)
        self.rnIn_reg.grid(row=0, column=1, padx=10, pady=30)

        tk.Label(self.regFrame, text="Name:", bg=self.clr(150, 150, 150), fg="white",
                 font=("Arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=30)
        self.nameIn_reg = tk.Entry(
            self.regFrame, font=("Arial", 15, "bold"), width=20)
        self.nameIn_reg.grid(row=1, column=1, padx=10, pady=30)

        tk.Label(self.regFrame, text="Subject:", bg=self.clr(150, 150, 150), fg="white",
                 font=("Arial", 15, "bold")).grid(row=2, column=0, padx=20, pady=30)
        self.subIn_reg = tk.Entry(
            self.regFrame, font=("Arial", 15, "bold"), width=20)
        self.subIn_reg.grid(row=2, column=1, padx=10, pady=30)

        tk.Button(self.regFrame, command=self.insertFun, text="OK", bd=2, fg="white", bg="gray",
                  width=20, font=("Arial", 20, "bold")).grid(row=3, column=0, columnspan=2, pady=40)

    def insertFun(self):
        try:
            rn = int(self.rnIn_reg.get())
            name = self.nameIn_reg.get()
            subVal = self.subIn_reg.get()
            if rn and name and subVal:
                con = pymysql.connect(
                    host="localhost", user="root", passwd="admin", database="rec")
                cur = con.cursor()
                cur.execute("INSERT INTO reg (rollNo, sName, sub, total) VALUES (%s, %s, %s, %s)",
                            (rn, name, subVal, 0))
                con.commit()
                messagebox.showinfo("Success", "Student Registered")
                self.clearFrames()
                cur.close()
                con.close()
            else:
                messagebox.showerror("Error", "All fields are required")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def showBk(self):
        try:
            con = pymysql.connect(
                host="localhost", user="root", passwd="akshu", database="lib")
            cur = con.cursor()
            cur.execute("SELECT * FROM lib")
            data = cur.fetchall()
            self.tabFun()
            self.table.delete(*self.table.get_children())
            for row in data:
                self.table.insert('', tk.END, values=row)
            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def resBook(self):
        self.clearFrames()
        self.resFrame = tk.Frame(self.root, bg=self.clr(
            150, 200, 80), bd=4, relief="ridge")
        self.resFrame.place(width=self.width/3,
                            height=self.height-180, x=self.width/3+120, y=100)

        tk.Label(self.resFrame, text="RollNo:", bg=self.clr(150, 200, 80), fg="white",
                 font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=50)
        self.rnIn_res = tk.Entry(
            self.resFrame, font=("Arial", 15, "bold"), width=20)
        self.rnIn_res.grid(row=0, column=1, padx=10, pady=50)

        tk.Label(self.resFrame, text="Book_Id:", bg=self.clr(150, 200, 80), fg="white",
                 font=("Arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=50)
        self.bkIn_res = tk.Entry(
            self.resFrame, font=("Arial", 15, "bold"), width=20)
        self.bkIn_res.grid(row=1, column=1, padx=10, pady=50)

        tk.Button(self.resFrame, command=self.resFun, text="OK", bd=2, fg="white", bg="gray",
                  width=20, font=("Arial", 20, "bold")).grid(row=2, column=0, columnspan=2, pady=50)

    def resFun(self):
        try:
            rn = int(self.rnIn_res.get())
            bk = int(self.bkIn_res.get())
            con = pymysql.connect(
                host="localhost", user="root", passwd="akshu", database="lib")
            cur = con.cursor()
            cur.execute(f"SELECT sName, total FROM reg WHERE rollNo = {rn}")
            student = cur.fetchone()
            cur.execute(f"SELECT bName, quant FROM lib WHERE bookId = {bk}")
            book = cur.fetchone()

            if student and book:
                if book[1] > 0:
                    cur.execute(
                        f"UPDATE reg SET total_book = total_book + 1 WHERE rollNo = {rn}")
                    cur.execute(
                        f"UPDATE lib SET quant = quant - 1 WHERE bookId = {bk}")
                    con.commit()
                    messagebox.showinfo(
                        "Success", f"Book '{book[0]}' reserved for student '{student[0]}'")
                    self.showBk()
                    self.clearFrames()
                else:
                    messagebox.showerror("Error", "Book out of stock")
            else:
                messagebox.showerror("Error", "Invalid roll or book ID")

            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def retFun(self):
        self.clearFrames()
        self.resFrame = tk.Frame(self.root, bg=self.clr(
            150, 200, 80), bd=4, relief="ridge")
        self.resFrame.place(width=self.width/3,
                            height=self.height-180, x=self.width/3+120, y=100)

        tk.Label(self.resFrame, text="RollNo:", bg=self.clr(150, 200, 80), fg="white",
                 font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=50)
        self.rnIn_ret = tk.Entry(
            self.resFrame, font=("Arial", 15, "bold"), width=20)
        self.rnIn_ret.grid(row=0, column=1, padx=10, pady=50)

        tk.Label(self.resFrame, text="Book_Id:", bg=self.clr(150, 200, 80), fg="white",
                 font=("Arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=50)
        self.bkIn_ret = tk.Entry(
            self.resFrame, font=("Arial", 15, "bold"), width=20)
        self.bkIn_ret.grid(row=1, column=1, padx=10, pady=50)

        tk.Button(self.resFrame, command=self.retBk, text="OK", bd=2, fg="white", bg="gray",
                  width=20, font=("Arial", 20, "bold")).grid(row=2, column=0, columnspan=2, pady=50)

    def retBk(self):
        try:
            rn = int(self.rnIn_ret.get())
            bk = int(self.bkIn_ret.get())
            con = pymysql.connect(
                host="localhost", user="root", passwd="akshu", database="lib")
            cur = con.cursor()
            cur.execute(f"SELECT bName, quant FROM lib WHERE bookId = {bk}")
            book = cur.fetchone()
            cur.execute(f"SELECT sName, total FROM reg WHERE rollNo = {rn}")
            student = cur.fetchone()

            if book and student:
                cur.execute(
                    f"UPDATE lib SET quant = quant + 1 WHERE bookId = {bk}")
                cur.execute(
                    f"UPDATE reg SET total = total - 1 WHERE rollNo = {rn}")
                con.commit()
                messagebox.showinfo(
                    "Success", f"Book '{book[0]}' returned from '{student[0]}'")
                self.showBk()
                self.clearFrames()
            else:
                messagebox.showerror("Error", "Invalid data")

            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def clearFrames(self):
        for attr in ['regFrame', 'resFrame']:
            if hasattr(self, attr):
                getattr(self, attr).destroy()

    def clr(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"


root = tk.Tk()
obj = library(root)
root.mainloop()
