import customtkinter
from data_management import data_management
from user import User
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import init_db
import datetime
import ctkdlib
from ctk_date_picker import CTkDatePicker as date_picker

class Budgeting_App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW",self.on_exit)

        self.geometry("1000x750")
        self.title("Finance Program")

        #Dictionary of pages later used by show_page to pull the instance of the page to bring up as well as to "forget" so a new page can be loaded
        self.pages = {}
        self.logged_in_user = None
        
        #Pages to be added to self.pages
        self.pages["login"] = LoginPage(self)
        self.pages["create_user"] = CreateUserPage(self)
        self.pages["dashboard"] = Dashboard(self)
        self.pages["profile"] = Profile(self)
        self.pages["expense"] = Create_Expense(self)
        self.pages["income"] = Create_Income(self)
        self.pages["saving"] = Create_Saving(self)


        # Show the initial login page
        self.show_page("login")

    def show_page(self, page_name):
        """Switch between pages."""
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages so a new page can be loaded
        self.pages[page_name].pack(fill="both", expand=True)  # Show the requested page



    def on_exit(self):
        #dumb useless obscure error with the CTk exit function. overrode the windows default button to fix this
        try:
            self.withdraw()
            self.quit()
        except:
            self.withdraw()
            self.quit()

class LoginPage(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.label = customtkinter.CTkLabel(master=self, text="Cameron's Budgeting Program", font=("Roboto", 30))
        self.label.pack(pady=12, padx=10)

        self.entry1 = customtkinter.CTkEntry(master=self, placeholder_text="Email Address")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=self, placeholder_text="Password", show="*")
        self.entry2.pack(pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=self, text="Login", command=self.handle_login)
        self.login_button.pack(pady=12, padx=10)

        self.failed_login_label = customtkinter.CTkLabel(master=self, text="", font=("Roboto", 13), text_color="red")
        self.failed_login_label.pack(pady=1, padx=5)

        self.new_user_button = customtkinter.CTkButton(master=self, text="Create New User", command=self.handle_create_user)
        self.new_user_button.pack(pady=12, padx=10)

    def handle_create_user(self):
        self.master.show_page("create_user")
        new_user_clear = self.master.pages["create_user"]
        new_user_clear.clear_fields()

    def handle_login(self):
        email = self.entry1.get()
        password = self.entry2.get()
        current_user = data_management.login(email, password)

        if current_user:
            print(f"Logged in as {current_user.first_name} {current_user.last_name}")
            self.master.logged_in_user = current_user            
            self.failed_login_label.configure(text="", text_color="green")
            self.master.show_page("dashboard")
            self.master.pages["dashboard"].refresh_dashboard()
        else:
            self.failed_login_label.configure(text="Please try another email or password", text_color="red")

    def clear_fields(self):
        self.failed_login_label.configure(text="")
        self.entry1.delete(0, "end")  
        self.entry2.delete(0, "end")

class CreateUserPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = customtkinter.CTkLabel(master=self, text="Create New User", font=("Roboto", 30))
        self.label.pack(pady=12, padx=10)

        self.first_name_entry = customtkinter.CTkEntry(master=self, placeholder_text="First Name")
        self.first_name_entry.pack(pady=12, padx=10)

        self.last_name_entry = customtkinter.CTkEntry(master=self, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=12, padx=10)

        self.email_entry = customtkinter.CTkEntry(master=self, placeholder_text="Email Address")
        self.email_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.create_user_button = customtkinter.CTkButton(master=self, text="Submit", command=self.handle_create_user)
        self.create_user_button.pack(pady=12, padx=10)

        self.back_button = customtkinter.CTkButton(master=self, text="Back to Login", command=self.handle_back_button)
        self.back_button.pack(pady=12, padx=10)

        self.feedback_label = customtkinter.CTkLabel(master=self, text="", font=("Roboto", 13), text_color="red")
        self.feedback_label.pack(pady=1, padx=5)

    def handle_back_button(self):
        self.master.show_page("login")
        Logout_control = self.master.pages["login"]
        Logout_control.clear_fields()

    def handle_create_user(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        current_user = data_management.create_new_user(first_name, last_name, email, password)

        if current_user:
            self.feedback_label.configure(text="User created successfully!", text_color="green")
        else:
            self.feedback_label.configure(text="Error: Please try a different email", text_color="red")
            
    def clear_fields(self):
        self.feedback_label.configure(text="")
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

class Dashboard(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        #grid setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3) 
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.button_frame = customtkinter.CTkFrame(master=self)
        self.button_frame.grid(row=0, column=1, pady=10, padx=10,sticky="nesw", rowspan = 2)

        self.profile_button = customtkinter.CTkButton(master=self.button_frame, text="Profile", command=self.handle_profile_button)
        self.profile_button.grid(row=0, column= 1,pady=10, padx=10)

        self.logout_button = customtkinter.CTkButton(master=self.button_frame, text="Logout", command=self.handle_logout)
        self.logout_button.grid(row=1, column= 1,pady=10, padx=10)

        self.create_expense_button = customtkinter.CTkButton(master=self.button_frame, text="Create Expense", command=self.handle_create_expense)
        self.create_expense_button.grid(row=0, column=0,pady=10, padx=10)

        self.create_income_button = customtkinter.CTkButton(master=self.button_frame, text="Create Income", command=self.handle_create_income)
        self.create_income_button.grid(row=1, column=0,pady=10, padx=10)

        self.create_saving_button = customtkinter.CTkButton(master=self.button_frame, text="Create Saving", command=self.handle_create_saving)
        self.create_saving_button.grid(row=2, column=0,pady=10, padx=10)

        
        #calendar Frame and date pickers
        calendar_frame = customtkinter.CTkFrame(self)
        calendar_frame.grid(row=2, column=1, pady=10, padx=10,sticky="nesw")

        self.start_date_entry = customtkinter.CTkEntry(master=calendar_frame, placeholder_text="Start Date")
        self.start_date_entry.grid(row=0, column=0, pady=10, padx=10)
        self.start_date_picker = date_picker(self.start_date_entry)

        self.end_date_entry = customtkinter.CTkEntry(master=calendar_frame, placeholder_text="End Date")
        self.end_date_entry.grid(row=0, column=1, pady=10, padx=10)
        self.end_date_picker = date_picker(self.end_date_entry)

        self.update_graphs = customtkinter.CTkButton(master=calendar_frame, text="Update Based on Dates", command=self.update_based_on_dates)
        self.update_graphs.grid(row=3,column=0, columnspan=2,padx=10, pady=10, sticky="nsew")

        self.canvas_widget = None
        self.canvas_widget2 = None

        # all plot line colors
        plt.rcParams["text.color"] = "white"
        plt.rcParams["axes.labelcolor"] = "white"
        plt.rcParams["xtick.color"] = "white"
        plt.rcParams["ytick.color"] = "white"

    def update_based_on_dates(self):
        self.Expense_by_category_graph(current_user=self.master.logged_in_user, date_end=self.end_date_entry.get(), date_start=self.start_date_entry.get())
        self.Finance_overview_chart(current_user=self.master.logged_in_user, date_end=self.end_date_entry.get(), date_start=self.start_date_entry.get())

    # Total Income, Expenses and Savings Chart
    def Finance_overview_chart(self, date_start="1900-01-01", date_end= datetime.date.today(),current_user=User):
        if current_user != None:               

            if self.canvas_widget != None:
                plt.close()
                self.canvas_widget=None

            expense = data_management.get_expense(date_start,date_end,current_user)
            chart_data = []
            total_expense = 0 
            for each_expense in expense:
                total_expense += round(each_expense.amount,2)
            chart_data.append(total_expense)

            income = data_management.get_income(date_start,date_end,current_user)
            total_income = 0 
            for each_income in income:
                total_income += round(each_income.amount,2)
            chart_data.append(total_income)

            saving = data_management.get_saving(date_start,date_end,current_user)
            total_saving = 0 
            for each_saving in saving:
                total_saving += round(each_saving.amount,2)
            chart_data.append(total_saving)


            
            labels = ["Expense", "Income", "Savings"]
            colors = ["#ff9393","#009500","#006c6c"]

            fig1, ax1 = plt.subplots()
            fig1.set_facecolor("#2b2b2b")
            ax1.set_facecolor("#2b2b2b")
            ax1.bar(labels,chart_data, color=colors)
            ax1.set_title("Financial Overview") 
            ax1.set_ylabel("Total USD")
            for i in range(len(labels)):
                plt.text(i, chart_data[i]//2, chart_data[i], ha='center')
            

            canvas = FigureCanvasTkAgg(fig1, self)
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            canvas.draw()
        
        else:
            pass

    # Total Income, Expenses and Savings Chart
    def Expense_by_category_graph(self, date_start="1900-01-01", date_end= datetime.date.today(),current_user=User):
        if current_user != None:  
            
            if self.canvas_widget2 != None:
                plt.close()
                self.canvas_widget2=None

            expense_list = data_management.get_expense(current_user=current_user, start_date=date_start, end_date=date_end)
            
            # Combine expenses by category
            category_totals = {}
            for expense in expense_list:
                if expense.category in category_totals:
                    category_totals[expense.category] += round(expense.amount,2)
                else:
                    category_totals[expense.category] = expense.amount


            labels = list(category_totals.keys()) 
            sizes = list(category_totals.values())
            total = sum(sizes)
            
            percentages = [(amount / total) * 100 for amount in sizes]
            
            
            
            fig2, ax2 = plt.subplots()
            fig2.set_facecolor("#2b2b2b")
            ax2.set_facecolor("#2b2b2b")
            ax2.pie(percentages, labels=labels,autopct='%1.1f%%')
            ax2.set_title("Split by category")

            canvas = FigureCanvasTkAgg(fig2, self)
            self.canvas_widget2 = canvas.get_tk_widget()
            self.canvas_widget2.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            canvas.draw()
                

        else:
            pass



    def refresh_dashboard(self):
        if self.master.logged_in_user != None:
            self.Finance_overview_chart(current_user=self.master.logged_in_user)
            self.Expense_by_category_graph(current_user=self.master.logged_in_user)

    def handle_create_expense(self):
        self.master.show_page("expense")
        self.master.pages["expense"].clear_fields()

    def handle_create_income(self):
        self.master.show_page("income")
        self.master.pages["income"].clear_fields()

    def handle_create_saving(self):
        self.master.show_page("saving")
        self.master.pages["saving"].clear_fields()

    #Login and Logout
    def handle_profile_button(self):
        self.master.show_page("profile")
        self.master.pages["profile"].update_profile()

    def handle_logout(self):
        self.master.show_page("login")
        self.master.pages["login"].clear_fields()
        self.master.logged_in_user = None

class Profile(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.handle_back_button)
        self.back_button.pack(pady=12, padx=10)

        self.email = customtkinter.CTkLabel(self, text="", font=("Roboto", 20))
        self.email.pack()

        self.name = customtkinter.CTkLabel(self, text="", font=("Roboto", 20))
        self.name.pack()

        self.id = customtkinter.CTkLabel(self, text="", font=("Roboto", 20))
        self.id.pack()

        self.delete_user_button = customtkinter.CTkButton(master=self, text="Delete Account", command=self.delete_user)
        self.delete_user_button.pack()

    def update_profile(self):
        self.email.configure(text=f"Email Address: {self.master.logged_in_user.email}")
        self.name.configure(text=f"Name: {self.master.logged_in_user.first_name} {self.master.logged_in_user.last_name}")
        self.id.configure(text=f"ID: {self.master.logged_in_user.id}")

    def handle_back_button(self):
        self.master.show_page("dashboard")

    def delete_user(self):
        deleted = data_management.close_account(self.master.logged_in_user)
        if deleted != None:
            self.master.pages["dashboard"].handle_logout()

class Create_Expense(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title = customtkinter.CTkLabel(master=self, text="Create A New Expense",font=("Roboto", 30))
        self.title.pack(pady=12, padx=10)

        self.entry_amount = customtkinter.CTkEntry(master=self, placeholder_text="Amount")
        self.entry_amount.pack(pady=12, padx=10)

        self.entry_category = customtkinter.CTkEntry(master=self, placeholder_text="Category")
        self.entry_category.pack(pady=12, padx=10)

        self.entry_storename = customtkinter.CTkEntry(master=self, placeholder_text="Storename")
        self.entry_storename.pack(pady=12, padx=10)

        self.date_entry = customtkinter.CTkEntry(master=self, placeholder_text="Expense Date")
        self.date_entry.pack(pady=10, padx=10)
        self.end_date_picker = date_picker(self.date_entry)

        self.create_expense_button = customtkinter.CTkButton(master=self, text="Create New Expense", command=self.create_new_expense)
        self.create_expense_button.pack(pady=12, padx=10)

        self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.handle_back_button)
        self.back_button.pack(pady=12, padx=10)

        self.create_expense_status = customtkinter.CTkLabel(master=self, text="",font=("Roboto", 15), text_color="green")
        self.create_expense_status.pack(pady=12, padx=10)

        self.current_user = self.master.logged_in_user

    def clear_fields(self):
        self.entry_amount.delete(0, "end")  
        self.entry_category.delete(0, "end")
        self.entry_storename.delete(0, "end")
        self.date_entry.delete(0, "end")
        
        self.create_expense_status.configure(text="")

    def create_new_expense(self):
        amount = self.entry_amount.get()
        category = self.entry_category.get()
        storename = self.entry_storename.get()
        date = self.date_entry.get()
        
        if date:
            date=date
        else:
            date=None
            
        new_expense = data_management.create_expense(current_user=self.master.logged_in_user, amount=amount, category=category, storename=storename, expense_date=date)
        self.clear_fields()
        self.create_expense_status.configure(text="Success! A new expense amount has been added to the system")


    def handle_back_button(self):
        self.master.show_page("dashboard")
        self.master.pages["dashboard"].refresh_dashboard()

class Create_Income(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title = customtkinter.CTkLabel(master=self, text="Create A New Income Amount",font=("Roboto", 30))
        self.title.pack(pady=12, padx=10)

        self.entry_amount = customtkinter.CTkEntry(master=self, placeholder_text="Amount")
        self.entry_amount.pack(pady=12, padx=10)

        self.entry_employer = customtkinter.CTkEntry(master=self, placeholder_text="Employer")
        self.entry_employer.pack(pady=12, padx=10)

        self.date_entry = customtkinter.CTkEntry(master=self, placeholder_text="Income Date")
        self.date_entry.pack(pady=10, padx=10)
        self.end_date_picker = date_picker(self.date_entry)

        self.create_income_button = customtkinter.CTkButton(master=self, text="Create New Income", command=self.create_new_income)
        self.create_income_button.pack(pady=12, padx=10)

        self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.handle_back_button)
        self.back_button.pack(pady=12, padx=10)

        self.create_income_status = customtkinter.CTkLabel(master=self, text="",font=("Roboto", 15),text_color="green")
        self.create_income_status.pack(pady=12, padx=10)

        self.current_user = self.master.logged_in_user

    def clear_fields(self):
        self.entry_amount.delete(0, "end")  
        self.entry_employer.delete(0, "end")
        self.date_entry.delete(0, "end")
        
        self.create_income_status.configure(text="")

    def create_new_income(self):
        amount = self.entry_amount.get()
        employer = self.entry_employer.get()
        date = self.date_entry.get()
        
        if date:
            date=date
        else:
            date=None
            
        new_income = data_management.create_income(current_user=self.master.logged_in_user, amount=amount, employer=employer, Income_date=date)
        self.clear_fields()
        self.create_income_status.configure(text="Success! A new income amount has been added to the system")

    def handle_back_button(self):
        self.master.show_page("dashboard")
        self.master.pages["dashboard"].refresh_dashboard()

class Create_Saving(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title = customtkinter.CTkLabel(master=self, text="Create A New Saving Amount",font=("Roboto", 30))
        self.title.pack(pady=12, padx=10)

        self.entry_amount = customtkinter.CTkEntry(master=self, placeholder_text="Amount")
        self.entry_amount.pack(pady=12, padx=10)

        self.entry_account_name = customtkinter.CTkEntry(master=self, placeholder_text="Account Name")
        self.entry_account_name.pack(pady=12, padx=10)

        self.entry_account_type = customtkinter.CTkEntry(master=self, placeholder_text="Account Type")
        self.entry_account_type.pack(pady=12, padx=10)

        self.date_entry = customtkinter.CTkEntry(master=self, placeholder_text="Saving Date")
        self.date_entry.pack(pady=10, padx=10)
        self.date_entry_picker = date_picker(self.date_entry)

        self.create_saving_button = customtkinter.CTkButton(master=self, text="Create New Saving", command=self.create_new_income)
        self.create_saving_button.pack(pady=12, padx=10)

        self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.handle_back_button)
        self.back_button.pack(pady=12, padx=10)

        self.create_saving_status = customtkinter.CTkLabel(master=self, text="",font=("Roboto", 15),text_color="green")
        self.create_saving_status.pack(pady=12, padx=10)

        self.current_user = self.master.logged_in_user

    def clear_fields(self):
        self.entry_amount.delete(0, "end")  
        self.entry_account_name.delete(0, "end")
        self.entry_account_type.delete(0, "end")
        self.date_entry.delete(0, "end")
        
        self.create_saving_status.configure(text="")

    def create_new_income(self):
        amount = self.entry_amount.get()
        account_type = self.entry_account_type.get()
        account_name = self.entry_account_name.get()
        date = self.date_entry.get()
        
        if date:
            date=date
        else:
            date=None
            
        new_savings = data_management.create_saving(current_user=self.master.logged_in_user, amount=amount, account_name=account_name,account_type=account_type, saving_date=date)
        self.clear_fields()
        self.create_saving_status.configure(text=f"Success! A new savings amount of has been added to the system", text_color="green")


    def handle_back_button(self):
        self.master.show_page("dashboard")
        self.master.pages["dashboard"].refresh_dashboard()



if __name__ == "__main__":
    init_db()
    app = Budgeting_App()
    app.mainloop()
