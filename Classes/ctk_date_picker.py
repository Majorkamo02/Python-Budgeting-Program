import tkinter
import customtkinter
from PIL import Image, ImageTk
import sys
import os
import math
from ctkdlib.custom_widgets.ctk_calendar import CTkCalendar

class CTkDatePicker(customtkinter.CTkToplevel):
    def __init__(self, attach_widget, **kwargs):
        super().__init__(takefocus=1)

        self.attach = attach_widget  # The widget (e.g., Entry) where the selected date is set
        self.overrideredirect(True)  # Removes window decoration
        self.calendar_navigation = False  # Tracks if the user is navigating the calendar

        # Frame and calendar setup
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.calendar = CTkCalendar(self.frame, command=self._set_date, **kwargs)
        self.calendar.pack(expand=True, fill="both")

        # Override navigation buttons
        self._override_navigation_buttons()

        # Start hidden
        self.withdraw()

        # Bindings for behavior
        self.attach.bind("<Button-1>", lambda e: self._toggle_visibility())  # Show/hide date picker on click
        self.bind("<FocusOut>", self._on_focus_out)  # Close when clicking outside (but allow navigation)

    def _override_navigation_buttons(self):
        """Intercept navigation commands to track navigation state."""
        original_left_command = self.calendar.left.cget("command")
        original_right_command = self.calendar.right.cget("command")

        self.calendar.left.configure(command=lambda: self._on_navigate(original_left_command, -1))
        self.calendar.right.configure(command=lambda: self._on_navigate(original_right_command, 1))

    def _on_navigate(self, original_command, direction):
        """Handle navigation clicks, keeping the date picker open."""
        self.calendar_navigation = True
        original_command()  # Execute the original navigation command
        self.after(200, lambda: setattr(self, "calendar_navigation", False))  # Reset state after navigation

    def _toggle_visibility(self):
        """Toggle visibility of the date picker."""
        if self.winfo_ismapped():
            self.withdraw()  # Hide if visible
        else:
            self._place_dropdown()  # Show if hidden

    def _place_dropdown(self):
        """Place the date picker below the attached widget."""
        x = self.attach.winfo_rootx()
        y = self.attach.winfo_rooty() + self.attach.winfo_height()
        self.geometry(f"{200}x{200}+{x}+{y}")  # Adjust size as needed
        self.deiconify()
        self.calendar.focus_set()  # Ensure the calendar has focus

    def _set_date(self, date):
        """Set the selected date to the attached widget and close the picker."""
        formatted_date = f"{date[2]}-{date[1]:02d}-{date[0]:02d}"  # Format as YYYY-MM-DD
        self.attach.delete(0, "end")
        self.attach.insert(0, formatted_date)
        self.withdraw()  # Close after a date is picked

    def _on_focus_out(self, event):
        """Close the date picker if focus is lost, except during navigation."""
        if not self.calendar_navigation:  # Only close if not navigating
            self.withdraw()