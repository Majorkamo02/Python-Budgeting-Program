import customtkinter
from data_management import data_management
from user import User
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
from database import init_db

class Budgeting_App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x750")
        self.title("Login System")

        #Dictionary of pages later used by show_page to pull the instance of the page to bring up as well as to "forget" so a new page can be loaded
        self.pages = {}
        self.logged_in_user = None
        
        #Pages to be added to self.pages
        self.pages["login"] = LoginPage(self)
        self.pages["create_user"] = CreateUserPage(self)
        self.pages["dashboard"] = Dashboard(self)
        self.pages["profile"] = Profile(self)

        # Show the initial login page
        self.show_page("login")

    def show_page(self, page_name):
        """Switch between pages."""
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages so a new page can be loaded
        self.pages[page_name].pack(fill="both", expand=True)  # Show the requested page

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
            self.failed_login_label.configure(text="", text_color="green")
            self.master.show_page("dashboard")
            self.master.logged_in_user = current_user
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

        # self.graph_widget = customtkinter.CTkLabel(self, text="Graph Placeholder")
        # self.graph_widget.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # # Stats Section
        # self.stats_widget = customtkinter.CTkLabel(self, text="Stats Placeholder")
        # self.stats_widget.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.grid_columnconfigure(0, weight=1)  # Left side for graphs
        self.grid_columnconfigure(1, weight=3)  # Right side for other widgets
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.profile_button = customtkinter.CTkButton(master=self, text="Profile", command=self.handle_profile_button)
        self.profile_button.pack(padx=10, pady=10)

        self.logout_button = customtkinter.CTkButton(master=self, text="Logout", command=self.handle_logout)
        self.logout_button.pack(pady=12, padx=10)

        # self.plt_params = plt.RcParams["axes.prop_cycle"] = plt.cycler(
        #     color=["#4C2A85", ""])

        # Total Income, Expenses and Savings Chart
    def Finance_overview_chart(self, date_start, date_end,current_user:User):
        expense = data_management.get_expense(date_start,date_end,current_user)
        chart_data = []
        total_expense = 0 
        for each_expense in expense:
            total_expense += each_expense.amount
        chart_data.append(total_expense)

        income = data_management.get_income(date_start,date_end,current_user)
        total_income = 0 
        for each_income in income:
            total_income += each_expense.amount
        chart_data.append(total_income)

        saving = data_management.get_saving(date_start,date_end,current_user)
        total_saving = 0 
        for each_saving in saving:
            total_saving += each_saving.amount
        chart_data.append(total_saving)


        
        labels = ["Expense", "Income", "Savings"]
        
        fig1, ax1 = plt.subplots()
        ax1.bar(labels,chart_data )
        ax1.set_title("Financial Overview") 
        ax1.set_ylabel("Total USD")
        plt.show()



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

class Graphs(customtkinter.CTkFrame):
    pass

if __name__ == "__main__":
    init_db()
    app = Budgeting_App()
    app.mainloop()
