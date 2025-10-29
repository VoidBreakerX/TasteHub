import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk

# ==============================================================
#                DATABASE CONNECTION
# ==============================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # 👈 change this
        password="daljeet",  # 👈 change this
        database="attendance_payroll"
    )

# ==============================================================
#                LOGIN WINDOW
# ==============================================================

def login_window():
    def check_login():
        username = entry_user.get()
        password = entry_pass.get()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            login.destroy()
            if user['role'] == 'employer':
                employer_dashboard()
            else:
                employee_dashboard(user['emp_id'])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login = Tk()
    login.title("Login - Attendance & Payroll System")
    login.geometry("400x250")
    login.resizable(False, False)

    Label(login, text="Attendance & Payroll System", font=("Arial", 14, "bold")).pack(pady=10)
    Label(login, text="Username:", font=("Arial", 12)).pack(pady=5)
    entry_user = Entry(login, font=("Arial", 12))
    entry_user.pack(pady=5)
    Label(login, text="Password:", font=("Arial", 12)).pack(pady=5)
    entry_pass = Entry(login, show="*", font=("Arial", 12))
    entry_pass.pack(pady=5)
    Button(login, text="Login", command=check_login, width=15, bg="green", fg="white", font=("Arial", 12)).pack(pady=15)

    login.mainloop()

# ==============================================================
#                EMPLOYER DASHBOARD
# ==============================================================

def employer_dashboard():
    root = Tk()
    root.title("Employer Dashboard")
    root.geometry("750x600")
    root.resizable(False, False)

    # ---------- ADD EMPLOYEE ----------
    def add_employee():
        add_win = Toplevel(root)
        add_win.title("Add Employee")
        add_win.geometry("400x400")

        Label(add_win, text="Name:").pack()
        name = Entry(add_win); name.pack()
        Label(add_win, text="Dept ID:").pack()
        dept = Entry(add_win); dept.pack()
        Label(add_win, text="Designation:").pack()
        desig = Entry(add_win); desig.pack()
        Label(add_win, text="DOJ (YYYY-MM-DD):").pack()
        doj = Entry(add_win); doj.pack()
        Label(add_win, text="Base Salary:").pack()
        salary = Entry(add_win); salary.pack()

        def save_emp():
            db = get_connection()
            cur = db.cursor()
            cur.execute("INSERT INTO Employee(emp_name, dept_id, designation, doj, base_salary) VALUES (%s,%s,%s,%s,%s)",
                        (name.get(), dept.get(), desig.get(), doj.get(), salary.get()))
            db.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            emp_id = cur.fetchone()[0]
            # Create login for employee
            cur.execute("INSERT INTO Users(username, password, role, emp_id) VALUES (%s,%s,%s,%s)",
                        (name.get().lower(), "1234", "employee", emp_id))
            db.commit()
            db.close()
            messagebox.showinfo("✅ Success", f"Employee added!\nUsername: {name.get().lower()}\nPassword: 1234")
            add_win.destroy()

        Button(add_win, text="Save", command=save_emp, bg="blue", fg="white").pack(pady=10)

    # ---------- MARK ATTENDANCE ----------
    def mark_attendance():
        att_win = Toplevel(root)
        att_win.title("Mark Attendance")
        att_win.geometry("400x400")

        Label(att_win, text="Employee ID:").pack()
        emp = Entry(att_win); emp.pack()
        Label(att_win, text="Date (YYYY-MM-DD):").pack()
        date = Entry(att_win); date.pack()
        Label(att_win, text="Status (Present/Absent/Leave):").pack()
        status = Entry(att_win); status.pack()
        Label(att_win, text="In Time (HH:MM:SS):").pack()
        in_time = Entry(att_win); in_time.pack()
        Label(att_win, text="Out Time (HH:MM:SS):").pack()
        out_time = Entry(att_win); out_time.pack()
        Label(att_win, text="Overtime Hours:").pack()
        overtime = Entry(att_win); overtime.pack()

        def save_attendance():
            db = get_connection()
            cur = db.cursor()
            cur.execute("""INSERT INTO Attendance(emp_id, att_date, status, in_time, out_time, overtime_hours)
                           VALUES (%s,%s,%s,%s,%s,%s)""",
                        (emp.get(), date.get(), status.get(), in_time.get(), out_time.get(), overtime.get()))
            db.commit()
            db.close()
            messagebox.showinfo("✅ Success", "Attendance marked successfully!")
            att_win.destroy()

        Button(att_win, text="Save Attendance", command=save_attendance, bg="green", fg="white").pack(pady=10)

    # ---------- VIEW EMPLOYEES ----------
    def view_employees():
        emp_win = Toplevel(root)
        emp_win.title("Employee Records")
        emp_win.geometry("700x400")

        tree = ttk.Treeview(emp_win, columns=("id", "name", "dept", "designation", "salary"), show="headings")
        for col in ("id", "name", "dept", "designation", "salary"):
            tree.heading(col, text=col.capitalize())
        tree.pack(fill=BOTH, expand=True)

        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT emp_id, emp_name, dept_id, designation, base_salary FROM Employee")
        for row in cur.fetchall():
            tree.insert("", END, values=row)
        db.close()

    # ---------- VIEW ATTENDANCE ----------
    def view_attendance():
        att_win = Toplevel(root)
        att_win.title("Attendance Records")
        att_win.geometry("800x400")

        tree = ttk.Treeview(att_win, columns=("id", "emp", "date", "status", "in", "out", "overtime"), show="headings")
        for col in ("id", "emp", "date", "status", "in", "out", "overtime"):
            tree.heading(col, text=col.capitalize())
        tree.pack(fill=BOTH, expand=True)

        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT att_id, emp_id, att_date, status, in_time, out_time, overtime_hours FROM Attendance")
        for row in cur.fetchall():
            tree.insert("", END, values=row)
        db.close()

    # ---------- VIEW PAYROLL ----------
    def view_payroll():
        pay_win = Toplevel(root)
        pay_win.title("Payroll Records")
        pay_win.geometry("800x400")

        tree = ttk.Treeview(pay_win, columns=("emp_id", "month", "gross", "deduct", "net"), show="headings")
        for col in ("emp_id", "month", "gross", "deduct", "net"):
            tree.heading(col, text=col.capitalize())
        tree.pack(fill=BOTH, expand=True)

        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT emp_id, pay_month, gross_salary, deductions, net_salary FROM Payroll ORDER BY pay_id DESC")
        for row in cur.fetchall():
            tree.insert("", END, values=row)
        db.close()

    # ---------- MAIN DASHBOARD ----------
    Label(root, text="👔 Employer Dashboard", font=("Arial", 18, "bold")).pack(pady=15)
    Button(root, text="➕ Add Employee", width=25, command=add_employee).pack(pady=5)
    Button(root, text="🕒 Mark Attendance", width=25, command=mark_attendance).pack(pady=5)
    Button(root, text="👥 View Employees", width=25, command=view_employees).pack(pady=5)
    Button(root, text="📋 View Attendance", width=25, command=view_attendance).pack(pady=5)
    Button(root, text="💰 View Payroll", width=25, command=view_payroll).pack(pady=5)
    Button(root, text="🚪 Logout", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

# ==============================================================
#                EMPLOYEE DASHBOARD
# ==============================================================

def employee_dashboard(emp_id):
    root = Tk()
    root.title("Employee Dashboard")
    root.geometry("600x400")
    root.resizable(False, False)

    def view_my_attendance():
        att_win = Toplevel(root)
        att_win.title("My Attendance")
        att_win.geometry("600x400")

        tree = ttk.Treeview(att_win, columns=("date","status","overtime"), show="headings")
        tree.heading("date", text="Date")
        tree.heading("status", text="Status")
        tree.heading("overtime", text="Overtime Hours")
        tree.pack(fill=BOTH, expand=True)

        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT att_date, status, overtime_hours FROM Attendance WHERE emp_id=%s", (emp_id,))
        for row in cur.fetchall():
            tree.insert("", END, values=row)
        db.close()

    def view_my_payroll():
        pay_win = Toplevel(root)
        pay_win.title("My Payroll")
        pay_win.geometry("600x400")

        tree = ttk.Treeview(pay_win, columns=("month","gross","deduct","net"), show="headings")
        tree.heading("month", text="Month")
        tree.heading("gross", text="Gross")
        tree.heading("deduct", text="Deductions")
        tree.heading("net", text="Net")
        tree.pack(fill=BOTH, expand=True)

        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT pay_month, gross_salary, deductions, net_salary FROM Payroll WHERE emp_id=%s", (emp_id,))
        for row in cur.fetchall():
            tree.insert("", END, values=row)
        db.close()

    Label(root, text="👨‍💼 Employee Dashboard", font=("Arial", 18, "bold")).pack(pady=10)
    Button(root, text="View My Attendance", width=25, command=view_my_attendance).pack(pady=5)
    Button(root, text="View My Payroll", width=25, command=view_my_payroll).pack(pady=5)
    Button(root, text="Logout", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

# ==============================================================
#                MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":
    login_window()
