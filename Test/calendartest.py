import customtkinter
import ctkdlib # pip install ctkdlib

class CTkDatePicker(customtkinter.CTkToplevel):
    def __init__(self,
                 master,
                 height=200,
                 width=200,
                 **kwargs):
        
        super().__init__(takefocus=1)

        self.attach = master
        self.height = height
        self.width = width
        
        self.overrideredirect(True)
    
        self.attach._canvas.tag_bind("right_parts", "<Button-1>", lambda e: self._iconify())
        self.attach._canvas.tag_bind("dropdown_arrow", "<Button-1>", lambda e: self._iconify())
        self.attach.bind('<Configure>', lambda e: self._withdraw(), add="+")
        self.attach.winfo_toplevel().bind('<Configure>', lambda e: self._withdraw(), add="+")
        
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.calendar = ctkdlib.CTkCalendar(self.frame, command=self._pass, **kwargs)
        self.calendar.pack(expand=True, fill="both")
        
        self.update_idletasks()
        self.deiconify()
        self.withdraw()
        
        date = self.calendar.current_date()
        self.attach.set(f"{date[0]}/{date[1]}/{date[2]}")
        
        self.hide = True
        
    def _iconify(self):
        if self.attach.cget("state")=="disabled": return

        if self.winfo_ismapped():
            self.hide = False
            
        if self.hide:
            self.deiconify()        
            self.hide = False
            self.place_dropdown()
        else:
            self.withdraw()
            self.hide = True
            
    def _withdraw(self):
        if self.winfo_ismapped():
            self.withdraw()
            self.hide = True
            
    def _pass(self, date):
        self.attach.set(f"{date[0]}/{date[1]}/{date[2]}")
        self._withdraw()
        
    def place_dropdown(self):
        x_pos = self.attach.winfo_rootx() 
        y_pos = self.attach.winfo_rooty() + self.attach.winfo_reqheight()

        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x_pos, y_pos))

if __name__ == "__main__":
    root = customtkinter.CTk()

    combobox = customtkinter.CTkComboBox(root)
    combobox.pack(padx=10, pady=10)

    CTkDatePicker(combobox) # just add this line in the combobox/optionmenu

    root.mainloop()