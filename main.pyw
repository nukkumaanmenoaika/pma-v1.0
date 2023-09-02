
from database import Database
from asyncio import run
import tkinter.messagebox
import tkinter
from tkinter import ttk
data = Database()
tk = tkinter.Tk()

tk.geometry("800x600")
tk.title("Manager of database version 1.0 by clarkcavers")
last_id = None
df = None

def get_info():
    global id, df
    id = patient_find.get()
    if not id:
        tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                    message="Поле пустое!")
        return
    try:
        df = run(Database().read_patients(id))
    except AssertionError as var:
        tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                                                    message=f"{var}")
    else:
        label_delete1 = tkinter.Label(tk, text=f"Patient id: {id}")
        label_delete1.place(x=230, y=255)
        new_window = tkinter.Toplevel(tk)
        new_window.geometry("860x630")
        new_window.resizable(False, False)
        canvas = tkinter.Canvas(new_window, bd=0, highlightthickness=0)
        canvas.pack(expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)
        treeview = ttk.Treeview(canvas, height=30)
        treeview.pack()
        treeview['columns'] = list(df.columns)
        for column in df.columns:
            treeview.heading(column, text=column)
        for index, row in df.iterrows():
            treeview.insert('', index, text=index, values=row.tolist())

        new_scrollbar = tkinter.Scrollbar(new_window, command=treeview.yview)
        new_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        treeview.configure(yscrollcommand=new_scrollbar.set)
        treeview.grid(row=1, column=1)
        treeview.rowconfigure(0, weight=1)
        treeview.columnconfigure(0, weight=1,)

        treeview.column("PATIENTID", width=10)
        treeview.column("SEX", width=10)
        treeview.column("MKBCODE", width=10)
        treeview.column("EXAMID", width=10)
        treeview.column("Type", width=10)
        treeview.column("SHEDULEDATE", width=10)
        treeview.column("BIRTHDATE", width=10)






def write_to_db():
    found = {"ID": patient_write.get(), "Sheludate": sheludate_write.get(), "Sex": sex_write.get(), "Birthday": birthday_write.get(), "Mkbcode": mkb_write.get(), "Type": type_write.get(), "Examid": examid_write.get()}
    clearly, mistakes = [], []

    for v, i in found.items():
        if not i: clearly.append(v)

    if clearly:
        tkinter.messagebox.showinfo(title="Manager of database version 1.0", message= f"Поле {', '.join(clearly)} пустое!")
        return
    test = run(Database().checker(**found))

    for i in test:
        if i: mistakes.append(i)
    if mistakes:
        tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                     message=f"{(' '*30).join(mistakes)}")
        return

    run(Database().write_database(PATIENTID=found["ID"], SHEDULEDATE=found["Sheludate"], TYPE=found["Type"],
                                    MKBCODE=found["Mkbcode"], EXAMID=found["Examid"], SEX=found["Sex"],
                                    BIRTHDATE=found["Birthday"]))
    tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                    message="Пациент успешно записан!")

def delete_line():
    try:
        line = int(line_del.get())
        if line in df.index:
            run(Database().delete_line(id, line))
            tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                        message="Строка успешно удалена!")
        else:
            tkinter.messagebox.showinfo(title="Manager of database version 1.0",
                                        message="Неверный номер строки!")
    except Exception as var:
        tkinter.messagebox.showinfo(title="Manager of database version 1.0", message=f"Пациент не выбран!") if isinstance(var,
                                                                                                             AttributeError) else ...
        tkinter.messagebox.showinfo(title="Manager of database version 1.0", message=f"{var}") if isinstance(var, AssertionError) else ...
        tkinter.messagebox.showinfo(title="Manager of database version 1.0", message="Номер строки должен быть числом!") if isinstance(var,
                                                                                              ValueError) else ...



tk.resizable(False, False)
# find patient
label_find = tkinter.Label(tk, text="Find patient", font=("Arial", 20))
label_find.place(x=315, y=5)

patient_find = tkinter.Entry(tk)
patient_find.place(x=330, y=50)


button_find = tkinter.Button(tk, text="Find", width="10", height="2", command=get_info)
button_find.place(x=350, y=75)


# delete line
label_delete = tkinter.Label(tk, text="Delete line", font=("Arial", 20))
label_delete.place(x=325, y=190)
label_delete1 = tkinter.Label(tk, text="Enter the line number")
label_delete1.place(x=334, y=230)

line_del = tkinter.Entry(tk)
line_del.place(x=330, y=255)



button_del = tkinter.Button(tk, text="Delete", width="10", height="2", command=delete_line)
button_del.place(x=350, y=290)


label_write = tkinter.Label(tk, text="Recording a patient", font=("Arial", 20))
label_write.place(x=270, y=350)

#patientid write
label_patientid = tkinter.Label(tk, text="ID")
label_patientid.place(x=205, y=400)

patient_write = tkinter.Entry(tk)
patient_write.place(x=180, y=425)


#birthday write
label_birthday = tkinter.Label(tk, text="Birthday")
label_birthday.place(x=205, y=470)

birthday_write = tkinter.Entry(tk)
birthday_write.place(x=180, y=495)




#sex write
label_sex = tkinter.Label(tk, text="Sex (0 or 1)")
label_sex.place(x=505, y=400)

sex_write = tkinter.Entry(tk)
sex_write.place(x=480, y=425)

#sheludate write
label_sheludate = tkinter.Label(tk, text="Sheludate")
label_sheludate.place(x=505, y=470)

sheludate_write = tkinter.Entry(tk)
sheludate_write.place(x=480, y=495)

#type write
label_type = tkinter.Label(tk, text="Type of diseases")
label_type.place(x=655, y=470)

type_write = tkinter.Entry(tk)
type_write.place(x=630, y=495)


#Examid write
label_examid = tkinter.Label(tk, text="Examid")
label_examid.place(x=50, y=470)

examid_write = tkinter.Entry(tk)
examid_write.place(x=30, y=495)


#Mkbcode write
label_mkb= tkinter.Label(tk, text="Mkbcode")
label_mkb.place(x=355, y=470)

mkb_write = tkinter.Entry(tk)
mkb_write.place(x=330, y=495)





button_find = tkinter.Button(tk, text="Write", width="10", height="2", command= write_to_db)
button_find.place(x=350, y=520)



tk.mainloop()