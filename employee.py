from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
from pymongo import *
from requests import *
import re 


Main = Tk()
Main.title("Employee Management System")
Main.geometry("1000x800+50+50")
Main.iconbitmap("emp.ico")
f = ("Times New Roman", 18, "bold")


def center_window(window):	
	window.update_idletasks()
	width = window.winfo_width()
	height = window.winfo_height()		
	x = (window.winfo_screenwidth() // 2) - (width // 2)
	y = (window.winfo_screenheight() // 2) - (height // 2)
	window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def f1():
	Main.withdraw()
	Add.deiconify()

def f2():
	Add.withdraw()
	Main.deiconify()

def f3():
	Main.withdraw()
	View.deiconify()
	view_records()
    
def f4():
	View.withdraw()
	Main.deiconify()

def f5():
	Main.withdraw()
	Update.deiconify()

def f6():
	Update.withdraw()
	Main.deiconify()

def f7():
	Main.withdraw()
	Delete.deiconify()

def f8():
	Delete.withdraw()
	Main.deiconify()

def save():
    con = None
    try:
        con = MongoClient("localhost", 27017)
        db = con["employee30"]
        coll = db["emp"]
        eid = Add_ent_id.get()
        ename = Add_ent_name.get()
        esalary = Add_ent_salary.get()

        # Validation for eid
        if eid == "":
            showerror("Issue", "Employee ID cannot be empty")
            return
        if eid.isalpha():
            showerror("Issue", "Employee ID cannot be text")
            return
        if eid.isspace():
            showerror("Issue", "Employee ID cannot contain space")
            return
        try:
            eid = int(eid)
            if eid < 0:
                showerror("Issue", "Employee ID cannot be negative")
                return
            if eid < 1 or eid > 1000:
                showerror("Issue", "Employee ID must be between 1 and 1000")
                return
        except ValueError:
            showerror("Issue", "Invalid ID")
            return

        # Check if the employee ID already exists in the database
        if coll.find_one({"_id": eid}):
            showerror("Issue", "Employee ID already exists")
            return

        # Validation for ename
        if not ename:
            showerror("Issue", "Employee name cannot be empty")
            return
        if ename.isdigit():
            showerror("Issue", "Employee name cannot be a number")
            return
        if any(char == '-' for char in ename):
            showerror("Issue", "Employee name cannot be negative")
            return
        if not re.match(r"^[a-zA-Z\s]+$", ename):
            showerror("Issue", "Employee name cannot contain special characters")
            return
        if ename.isspace():
            showerror("Issue", "Employee name cannot contain spaces")
            return
        if len(ename) < 2 or len(ename) > 20:
            showerror("Issue", "Employee name length should be between 2 and 20 characters")
            return

        # Validation for salary
        if esalary.isspace():
            showerror("Issue", "Employee salary cannot contain space")
            return
        if esalary.isalpha():
            showerror("Issue", "Employee salary cannot be text")
            return
        try:
            esalary = int(esalary)
            if esalary < 0:
                showerror("Issue", "Employee salary cannot be negative")
                return
            if esalary < 1000 or esalary > 100000:
                showerror("Issue", "Employee salary must be between 1000 and 100000")
                return
        except ValueError:
            showerror("Issue", "Employee salary must be only numeric")
            return

        info = {"_id": eid, "name": ename, "salary": esalary}
        coll.insert_one(info)
        showinfo("Success", "Record Created")
        Add_ent_id.delete(0, END)
        Add_ent_name.delete(0, END)
        Add_ent_salary.delete(0, END)
        Add_ent_id.focus()

    except Exception as e:
        print("Error:", e)
        showerror("Issue", "Values cannot be empty")
    finally:
        if con is not None:
            con.close()

def clear_Add():
	Add_ent_id.delete(0, END)
	Add_ent_name.delete(0, END)
	Add_ent_salary.delete(0, END)
	Add_ent_id.focus()


def view_records():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee30"]
		coll = db["emp"]
		data = coll.find()
		View_st_data.delete(1.0, END)
		for d in data:
			View_st_data.insert(END, f"eid = {d['_id']}, ename =  {d['name']}, esalary = {d['salary']}\n")
	except Exception as e:
		showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()

def update():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee30"]
		coll = db["emp"]
		eid = Update_ent_id.get()
		ename = Update_ent_name.get()
		esalary = Update_ent_salary.get()
		
		if eid == "":
			showerror("issue", "Employee ID cannot be empty")
			return
		if eid.isalpha():
			showerror("issue", "Employee ID cannot be text")
			return
		if eid.isspace():
			showerror("issue", "Employee ID cannot contain space ")
			return

		try:
			eid = int(eid)
			if eid < 0:
				showerror("issue", "Employee ID cannot be negative")
				return
			if eid < 1 or eid > 1000:
				showerror("issue", "Employee ID must be between 1 and 1000")
				return

		except Exception:
			showerror("issue", "invalid id")
			return

        # Validation for esalary

		if esalary == "":
			showerror("issue", "Employee salary cannot be empty")
			return

		if esalary.isspace():
			showerror("issue", "Employee salary cannot contain space ")
			return

		if esalary.isalpha():
			showerror("issue", "Employee salary cannot be text")
			return

		try:
			esalary = int(esalary)
			if esalary < 0:
				showerror("issue", "Employee salary cannot be negative")
				return
			if esalary < 1000 or esalary > 100000:
				showerror("issue", "Employee salary must be between 1000 and 100000")
				return

		except Exception:
			showerror("issue", "Employee salary must be a numeric")
			return
 # Validation for ename

		if not ename:
			showerror("issue", "Employee name cannot be empty")
			return

		if ename.isdigit():
			showerror("issue", "Employee name cannot be number")
			return

		if any(char == '-' for char in ename):
			showerror("issue", "Employee name cannot be negative")
			return

		if not re.match(r"^[a-zA-Z\s]+$", ename):
			showerror("Error", "Employee name cannot contain special characters.")
			return

		if ename.isspace():
			showerror("issue", "Employee name cannot contain sapces")
			return


		if len(ename) < 2 or len(ename) > 20:
			showerror("issue", "Employee name length shud be  betn 2 and 20 char.")
			return


		if coll.find_one({"_id":eid}):
			coll.update_one({"_id":eid}, {"$set": {"name":ename, "salary":esalary}})
			showinfo("success", "record updated")
			Update_ent_id.delete(0, END)
			Update_ent_name.delete(0, END)
			Update_ent_salary.delete(0, END)
			Update_ent_id.focus()
		else:
			showinfo("issue", "record does not exists")
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()
def clear_Update():
	Update_ent_id.delete(0, END)
	Update_ent_name.delete(0, END)
	Update_ent_salary.delete(0, END)
	Update_ent_id.focus()


def delete():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee30"]
		coll = db["emp"]

		eid = Delete_ent_id.get()
		if eid == "":
			showerror("error", "please enter Employee ID ")
			return

		if not eid.isdigit():
			showerror("issue", "invalid Employee ID")
			return

		eid = int(eid)
		if coll.find_one({"_id": eid}):
			coll.delete_one({"_id": eid})
			showinfo("success", "record deleted successfully")
			Delete_ent_id.delete(0, END)
			Delete_ent_id.focus()
			
		else:
			showinfo("error", "record does not exist")
	except Exception:
			showerror("issue", "invalid id")
	finally:
		if con is not None:
			con.close()

def show():
	con = MongoClient("localhost", 27017)
	db = con["employee30"]
	coll = db["emp"]
	data = coll.find().sort("salary", -1).limit(5)
	enames = []
	esalaries = []
	for d in data:
		enames.append(d["name"])
		esalaries.append(d["salary"])

	plt.bar(enames, esalaries, color="blue", width=0.5)
	plt.xlabel("Employee Name")
	plt.ylabel("Salary")
	plt.title("Top5 Highest salaried Employees")
	
	plt.show()

def loc_temp():
	try:
		wa = "https://ipinfo.io/"
		res = get(wa)
		if res.status_code == 200:
			data = res.json()
			city_name = data['city']
			state_name = data['region']
			country_name = data['country']
			loc_msg = f"Location: {city_name}, {state_name}, {country_name}"
			Main_lab_loc.configure(text=loc_msg)

			api_key = "b65ff0940dfde6a3283d2d7ccfdd8a17"
			we = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
			responce = get(we)
			if res.status_code == 200:
				temp_data = responce.json()
				temp = temp_data['main']['temp']
				temp_msg = f"Temperature: {temp}\u00b0C"
				Main_lab_temp.configure(text=temp_msg)
			else:
				showerror("issue", "it failed to retrieve temperature data")
		else:
			showerror("issue", "failed to retrieve location")

	except Exception as e:
		showerror("issue", e)


# Center all windows
center_window(Main)

Main_lab_title = Label(Main, text="Employee Management System",font=("cambria", 25, "bold"))
Main_lab_title.pack(pady=30)
Main_btn_add = Button(Main, text="Add Employee", font=f, width=15, command=f1)
Main_btn_view = Button(Main, text="View Employee", font=f, width=15, command=f3)
Main_btn_update = Button(Main, text="Update Employee", font=f, width=15, command=f5)
Main_btn_delete = Button(Main, text="Delete Employee", font=f, width=15, command=f7)
Main_btn_chart = Button(Main, text="Charts", font=f, width=15, command=show)
Main_btn_add.pack(pady=10, anchor=CENTER)
Main_btn_view.pack(pady=10, anchor=CENTER)
Main_btn_update.pack(pady=10, anchor=CENTER)
Main_btn_delete.pack(pady=10, anchor=CENTER)
Main_btn_chart.pack(pady=10, anchor=CENTER)

Main_lab_title1 = Label(Main,text="***************************************************************", font=f)
Main_lab_title2 = Label(Main, text="Current Location and Temperature", font=f)
Main_lab_title1.pack(pady=30, anchor=CENTER)
Main_lab_title2.pack(pady=30, anchor=CENTER)
Main_lab_loc = Label(Main, text="",  font=f)
Main_lab_loc.pack(pady=10, anchor=CENTER)
Main_lab_temp = Label(Main, text="", font=f)
Main_lab_temp.pack(pady=5, anchor=CENTER)
loc_temp()

Add = Toplevel(Main)
Add.title("Add Employee")
Add.geometry("800x700+50+50")
Add.iconbitmap("emp.ico")
f = ("Times New Roman", 18, "bold")


Add_lab_title = Label(Add, text="Add New Employee", font=f)
Add_lab_id = Label(Add, text="Employee ID:", font=f)
Add_ent_id = Entry(Add, font=f)
Add_lab_name = Label(Add, text="Employee Name:", font=f)
Add_ent_name = Entry(Add, font=f)
Add_lab_salary = Label(Add, text="Employee Salary:", font=f)
Add_ent_salary = Entry(Add, font=f)
Add_btn_save = Button(Add, text="Save", width=12, command=save, font=f)
Add_btn_clear = Button(Add, text="Clear", width=12, command=clear_Add, font=f)
Add_btn_back = Button(Add, text="Back", width=12, command=f2, font=f)
Add_lab_title.pack(pady=30)
Add_lab_id.pack(pady=10, anchor=CENTER)
Add_ent_id.pack(pady=10, anchor=CENTER)
Add_lab_name.pack(pady=10, anchor=CENTER)
Add_ent_name.pack(pady=10, anchor=CENTER)
Add_lab_salary.pack(pady=10, anchor=CENTER)
Add_ent_salary.pack(pady=10, anchor=CENTER)
Add_btn_save.pack(pady=10, anchor=CENTER)
Add_btn_clear.pack(pady=10, anchor=CENTER)
Add_btn_back.pack(pady=10, anchor=CENTER)
Add.withdraw()

View = Toplevel(Main)
View.title("View Employee")
View.geometry("600x500+50+50")
View.iconbitmap("emp.ico")
f = ("Times New Roman", 18, "bold")

View_lab_title = Label(View, text="View Employee", font=f)
View_st_data = ScrolledText(View, width=40, height=10, font=f)
View_btn_back = Button(View, text="Back", font=f, width=12, command=f4)
View_lab_title.pack(pady=30)
View_st_data.pack(pady=10)
View_btn_back.pack(pady=10)
View.withdraw()

Update = Toplevel(Main)
Update.title("Update Employee")
Update.geometry("800x700+50+50")
Update.iconbitmap("emp.ico")
f = ("Times New Roman", 18, "bold")

Update_lab_title = Label(Update, text="Update Existing Employee", font=f)
Update_lab_id = Label(Update, text="Employee ID:", font=f)
Update_ent_id = Entry(Update, font=f)
Update_lab_name = Label(Update, text="Employee Name:", font=f)
Update_ent_name = Entry(Update, font=f)
Update_lab_salary = Label(Update, text="Employee Salary:", font=f)
Update_ent_salary = Entry(Update, font=f)
Update_btn_save = Button(Update, text="Save", font=f, width=12, command=update)
Update_btn_clear = Button(Update, text="Clear", font=f, width=12, command=clear_Update)
Update_btn_back = Button(Update, text="Back", font=f, width=12, command=f6)
Update_lab_title.pack(pady=30)
Update_lab_id.pack(pady=10, anchor=CENTER)
Update_ent_id.pack(pady=10, anchor=CENTER)
Update_lab_name.pack(pady=10, anchor=CENTER)
Update_ent_name.pack(pady=10, anchor=CENTER)
Update_lab_salary.pack(pady=10, anchor=CENTER)
Update_ent_salary.pack(pady=10, anchor=CENTER)
Update_btn_save.pack(pady=10, anchor=CENTER)
Update_btn_clear.pack(pady=10, anchor=CENTER)
Update_btn_back.pack(pady=10, anchor=CENTER)
Update.withdraw()

Delete = Toplevel(Main)
Delete.title("Delete Employee")
Delete.geometry("600x500+50+50")
Delete.iconbitmap("emp.ico")
f = ("Times New Roman", 18, "bold")

Delete_lab_title = Label(Delete, text="Delete Employee", font=f)
Delete_lab_id = Label(Delete, text="Employee ID:", font=f)
Delete_ent_id = Entry(Delete, font=f)
Delete_btn_delete = Button(Delete, text="Delete", font=f, width=12, command=delete)
Delete_btn_back = Button(Delete, text="Back", font=f, width=12, command=f8)
Delete_lab_title.pack(pady=30)
Delete_lab_id.pack(pady=10, anchor=CENTER)
Delete_ent_id.pack(pady=10, anchor=CENTER)
Delete_btn_delete.pack(pady=10, anchor=CENTER)
Delete_btn_back.pack(pady=10, anchor=CENTER)
Delete.withdraw()

Main.mainloop()
