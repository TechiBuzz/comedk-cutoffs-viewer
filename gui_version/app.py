import os

from util.colleges_and_codes import college_n_codes
from CTkTable import CTkTable

import customtkinter as ctk
import json

ROUND_NUMBER_TO_FILE = {
    "2024 MOCK": "data/comedk-24-mock.json",
    "2024 Round 1": "data/comedk-24-r1.json",
    "2024 Round 2": "data/comedk-24-r2.json",
    "2024 Round 3": "data/comedk-24-r3.json",
    "2025 MOCK": "data/comedk-25-mock.json"
}


def retrieve_college(filepath: str, college_code: str) -> dict:
    college = dict()

    with open(filepath, 'r') as file:
        data = json.load(file)
        for thing in data:
            if thing['code'] == college_code:
                college = thing
                break

    return college


def retrieve_all_colleges(filepath: str) -> list:
    colleges_list = []

    with open(filepath, 'r') as file:
        data = json.load(file)
        for college in data:
            colleges_list.append(college)

    return colleges_list


class CollegeWidget(ctk.CTkFrame):
    def __init__(self, master, college_name: str, counselling_round: str, courses: dict):
        super().__init__(master, corner_radius=16)

        # Header Frame
        self.header_frame = ctk.CTkFrame(master=self, corner_radius=16,
            fg_color="#" + str(os.urandom(3).hex()))
        self.header_frame.pack(expand=True, fill="both", padx=10, pady=10, ipady=20)

        # College Label
        self.college_name_label = ctk.CTkLabel(
            master=self.header_frame,
            text=college_name,
            font=("Arial Rounded MT Bold", 20, "bold"),
            text_color='black'
        )
        self.college_name_label.pack(side="left", padx=(20, 0))

        # Round Info
        self.round_info = ctk.CTkLabel(
            master=self.header_frame,
            text=counselling_round,
            font=("Arial Rounded MT Bold", 15, "normal")
        )
        self.round_info.pack(side="right", padx=(0, 20))

        # Course List
        self.course_table_entries = [('Course', 'Closing Rank')]
        self.course_list = CTkTable(
            master=self,
            column=2,
            row=1
        )
        self.course_list.pack(expand=True, fill="both", padx=10, pady=(0, 10), ipady=10)

        # Enter and Update table values
        if len(courses) != 0:
            for key in courses:
                self.course_table_entries.append((key, courses[key]))
            self.course_list.rows = len(courses)
        else:  # No data / some error
            self.course_table_entries.append(('-', '-'))
            self.course_list.rows = 2

        self.course_list.update_values(self.course_table_entries)

        # Pack as soon as instantiated
        self.pack(expand=True, fill="both", pady=10)


class ComedkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # VARIABLES
        self.college_var = ctk.StringVar(value='ALL')
        self.counselling_round_var = ctk.StringVar(value='2024 Round 1')
        self.rank_range_var = ctk.StringVar(value='0-6000')

        # Main Frame
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=16)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Top half of the frame
        self.parameter_section = ctk.CTkFrame(master=self.main_frame, corner_radius=16)

        self.parameter_section.rowconfigure((0, 1, 2), weight=1)
        self.parameter_section.columnconfigure((0, 1, 2, 3), weight=1, uniform="yessir")

        self.parameter_section.pack(expand=True, fill="both", padx=20, pady=(20, 10))

        # College Name Label
        self.college_name = ctk.CTkLabel(
            master=self.parameter_section,
            text="[🏫] College(s):",
            font=('Helvetica', 24, 'bold')
        )
        self.college_name.grid(row=0, column=0, sticky='w', padx=(20, 0))

        # College List Dropdown
        self.dropdown_college_items = ['ALL'] + [x + ": " + y for x, y in college_n_codes.items()]
        self.dropdown_college = ctk.CTkOptionMenu(
            master=self.parameter_section,
            values=self.dropdown_college_items,
            variable=self.college_var,
            height=35,
            corner_radius=16
        )
        self.dropdown_college.grid(row=0, column=1, sticky='ew')

        # Counselling Round Label
        self.counselling_round = ctk.CTkLabel(
            master=self.parameter_section,
            text="[🎯] Round: ",
            font=('Helvetica', 24, 'bold')
        )
        self.counselling_round.grid(row=0, column=2, sticky='ew')

        # College List Dropdown
        self.dropdown_round = ctk.CTkOptionMenu(
            master=self.parameter_section,
            values=["2024 MOCK", "2024 Round 1", "2024 Round 2", "2024 Round 3", "2025 MOCK"],
            variable=self.counselling_round_var,
            height=35,
            corner_radius=16
        )
        self.dropdown_round.grid(row=0, column=3, sticky='ew', padx=20)

        # Rank Range Label
        self.rank_range = ctk.CTkLabel(
            master=self.parameter_section,
            text="[🔢] Rank Range: ",
            font=('Helvetica', 24, 'bold')
        )
        self.rank_range.grid(row=1, column=0, sticky='w', padx=(20, 0))

        # Rank Range Dropdown
        self.dropdown_rank_range = ctk.CTkOptionMenu(
            master=self.parameter_section,
            values=["ALL", "0-6000", "6000-12000", "12000-18000", "18000-24000", "24000-30000", "30000-36000",
                    "36000-42000", "42000-48000", "48000-54000", "54000-100000"],
            variable=self.rank_range_var,
            height=35,
            corner_radius=16
        )
        self.dropdown_rank_range.grid(row=1, column=1, sticky='ew', padx=(0, 20), columnspan=3)

        # Search Button
        self.search = ctk.CTkButton(
            master=self.parameter_section,
            text="🔍 Search",
            font=("Helvetica", 20, "bold"),
            corner_radius=100,
            fg_color="#588157",
            hover_color="#a3b18a",
            command=self.generate_list
        )
        self.search.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=20, pady=(0, 10))

        # Options List
        self.options_list = ctk.CTkScrollableFrame(master=self.main_frame, corner_radius=16)
        self.options_list.pack(expand=True, fill="both", padx=20, pady=(10, 20))

    def generate_list(self):
        round_file = ROUND_NUMBER_TO_FILE[self.counselling_round_var.get()]

        if not self.college_var.get() == "ALL":
            college = retrieve_college(round_file, self.college_var.get()[:4])

            CollegeWidget(
                master=self.options_list,
                college_name=college['name'],
                counselling_round=self.counselling_round_var.get(),
                courses=college['courses']
            )
        else:
            for college in retrieve_all_colleges(round_file):
                CollegeWidget(
                    master=self.options_list,
                    college_name=college['name'],
                    counselling_round=self.counselling_round_var.get(),
                    courses=college['courses']
                )


def main():
    # CTk Settings
    ctk.set_appearance_mode('dark')

    # Init
    app = ComedkApp()

    # Window Config
    app.title("COMED-K CUT-OFFS")
    app.geometry('980x540')
    # app.resizable(False, False)

    # Start GUI mainloop
    app.mainloop()


if __name__ == '__main__':
    main()
