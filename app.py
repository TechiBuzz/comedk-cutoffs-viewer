from PIL import Image

from assets.util.colleges_and_codes import college_n_codes
from CTkTable import CTkTable

import customtkinter as ctk
import json


def retrieve_colleges(filepath: str, college_code: str, rank_range: str, branches: str) -> list[dict]:
    # Extract raw data]
    colleges_list = []

    with open(filepath, 'r') as file:
        data = json.load(file)
        if college_code == "ALL":
            for college in data:
                colleges_list.append(college)
        else:
            for college in data:
                if college['code'] == college_code:
                    colleges_list.append(college)
                    break

    # Return a formatted version with only required settings
    formatted_colleges_list = []

    cs = {
        "AD", "AI", "CA", "CB", "CD", "CG", "CI", "CN", "CO",
        "CM", "CS", "CY", "IA", "IC", "IN", "IS"
    }

    elec = {
        "EC", "EE", "EI", "ES", "ET", "EV", "UE", "VL"
    }

    other = {
        "AE", "AG", "AR", "AS", "AU", "BD", "BF", "BL", "BM", "BT",
        "CC", "CH", "CV", "IM", "MA", "ME", "MT", "RA", "RO"
    }

    branch_codes = {
        "cs": cs,
        "elec": elec,
        "all": cs | elec | other
    }

    rank_start = 0 if (rank_range == "ALL") else int(rank_range.partition('-')[0])
    rank_end = 20000 if (rank_range == "ALL") else int(rank_range.partition('-')[-1])

    for college in colleges_list:
        formatted_college = {'code': "", 'name': "", 'courses': {}}

        for key in college.keys():
            if key == 'courses':
                for course, cutoff in college['courses'].items():
                    if rank_start <= int(cutoff) <= rank_end and course[:2] in branch_codes[branches]:
                        formatted_college['courses'].update({course: cutoff})
            else:
                formatted_college.update({key: college[key]})

        if formatted_college['courses']:
            formatted_colleges_list.append(formatted_college)

    return formatted_colleges_list


class CollegeWidget(ctk.CTkFrame):
    def __init__(self, master, college_name: str, counselling_round: str, courses: dict):
        super().__init__(master, corner_radius=16)

        # Header Frame
        self.header_frame = ctk.CTkFrame(
            master=self, corner_radius=16,
            fg_color="#ff477e"
        )
        self.header_frame.pack(expand=True, fill="both", padx=10, pady=10, ipady=20)

        # College Label
        self.college_name_label = ctk.CTkLabel(
            master=self.header_frame,
            text=college_name,
            font=("Space Grotesk", 26, "bold"),
            text_color='#FFFFFF'
        )
        self.college_name_label.pack(side="left", padx=(20, 0))

        # Round Info
        self.round_info = ctk.CTkLabel(
            master=self.header_frame,
            text=counselling_round,
            font=("Space Grotesk", 17, "bold"),
            text_color='#FFFFFF',
            fg_color='#b81142',
            corner_radius=16
        )
        self.round_info.pack(side="right", padx=(0, 20))

        # Course List
        self.course_table_entries = [('Course', 'Closing Rank')]
        self.course_list = CTkTable(
            master=self,
            column=2, row=1,
            font=('Verdana', 16, 'bold'),
            pady=8,
        )
        self.course_list.pack(expand=True, fill="both", padx=10, pady=(0, 10), ipady=10)

        # Enter and Update table values
        for key in courses:
            self.course_table_entries.append((key, courses[key]))
        self.course_list.rows = len(courses) + 1

        self.course_list.update_values(self.course_table_entries)

        # Pack as soon as instantiated
        self.pack(expand=True, fill="both", pady=10)


class ComedkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # VARIABLES
        self.college_widget_instances = []

        self.college_var = ctk.StringVar(value='E027: BMS College of Engineering-Basavanagudi, Bengaluru')
        self.counselling_round_var = ctk.StringVar(value='2024 Round 1')
        self.rank_range_var = ctk.StringVar(value='0-6000')

        # Main Frame
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=16)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Top half of the frame
        self.parameter_section = ctk.CTkFrame(master=self.main_frame, corner_radius=16)

        self.parameter_section.rowconfigure((0, 1, 2), weight=1)
        self.parameter_section.rowconfigure(3, weight=2)
        self.parameter_section.columnconfigure((0, 1, 2, 3), weight=1, uniform="yessir")

        self.parameter_section.pack(fill="x", padx=20, pady=(20, 10))

        # College Name Label
        self.college_name = ctk.CTkLabel(
            master=self.parameter_section,
            text="    College:",
            font=('Helvetica', 26, 'bold'),
            image=ctk.CTkImage(
                light_image=Image.open('assets/ui/icons/college.png'),
                dark_image=Image.open('assets/ui/icons/college.png'),
                size=(48, 48)
            ),
            compound='left'
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
        self.dropdown_college.grid(row=0, column=1, sticky='ew', pady=30)

        # Counselling Round Label
        self.counselling_round = ctk.CTkLabel(
            master=self.parameter_section,
            text="    Round: ",
            font=('Helvetica', 26, 'bold'),
            image=ctk.CTkImage(
                light_image=Image.open('assets/ui/icons/round.png'),
                dark_image=Image.open('assets/ui/icons/round.png'),
                size=(48, 48)
            ),
            compound='left'
        )
        self.counselling_round.grid(row=0, column=2, sticky='w', padx=(20, 0))

        # College Round Dropdown
        self.dropdown_round = ctk.CTkOptionMenu(
            master=self.parameter_section,
            values=["2024 MOCK", "2024 Round 1", "2024 Round 2", "2024 Round 3", "2025 MOCK"],
            variable=self.counselling_round_var,
            height=35,
            corner_radius=16
        )
        self.dropdown_round.grid(row=0, column=3, sticky='ew', padx=20, pady=30)

        # Rank Range Label
        self.rank_range = ctk.CTkLabel(
            master=self.parameter_section,
            text="    Rank Range: ",
            font=('Helvetica', 26, 'bold'),
            image=ctk.CTkImage(
                light_image=Image.open('assets/ui/icons/rank.png'),
                dark_image=Image.open('assets/ui/icons/rank.png'),
                size=(48, 48)
            ),
            compound='left'
        )
        self.rank_range.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(0, 30))

        # Rank Range Dropdown
        self.dropdown_rank_range = ctk.CTkOptionMenu(
            master=self.parameter_section,
            values=["ALL", "0-6000", "6000-12000", "12000-18000", "18000-24000", "24000-30000", "30000-36000",
                    "36000-42000", "42000-48000", "48000-54000", "54000-100000"],
            variable=self.rank_range_var,
            height=35,
            corner_radius=16
        )
        self.dropdown_rank_range.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=(0, 30), columnspan=3)

        # Course Selector Label
        self.course_select = ctk.CTkLabel(
            master=self.parameter_section,
            text="    Courses: ",
            font=('Helvetica', 26, 'bold'),
            image=ctk.CTkImage(
                light_image=Image.open('assets/ui/icons/course.png'),
                dark_image=Image.open('assets/ui/icons/course.png'),
                size=(48, 48)
            ),
            compound='left'
        )
        self.course_select.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(0, 30))

        # Course Radio VARS
        self.course_select_var = ctk.StringVar(value='all')

        # Course Radio 1 (ALL)
        self.radio_course_all = ctk.CTkRadioButton(
            master=self.parameter_section,
            text="All",
            variable=self.course_select_var,
            value='all',
            fg_color='#9163cb'
        )
        self.radio_course_all.grid(row=2, column=1, sticky='ew', padx=(2, 0), pady=(0, 30))

        # Course Radio 2 (CS/IT)
        self.radio_course_cs = ctk.CTkRadioButton(
            master=self.parameter_section,
            text="CS/IT",
            variable=self.course_select_var,
            value='cs',
            fg_color='#9163cb'
        )
        self.radio_course_cs.grid(row=2, column=2, sticky='ew', padx=(22, 0), pady=(0, 30))

        # Course Radio 1 (ELECTRIC)
        self.radio_course_elec = ctk.CTkRadioButton(
            master=self.parameter_section,
            text="Electrical",
            variable=self.course_select_var,
            value='elec',
            fg_color='#9163cb'
        )
        self.radio_course_elec.grid(row=2, column=3, sticky='ew', padx=(22, 0), pady=(0, 30))

        # Search Button
        self.search = ctk.CTkButton(
            master=self.parameter_section,
            text="🔍 Search",
            font=("Helvetica", 20, "bold"),
            height=50,
            corner_radius=100,
            fg_color="#ff9f1c",
            hover_color="#ffbf69",
            command=lambda: self.generate_list(True)
        )
        self.search.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=20, pady=(0, 30))

        # Add Button
        self.add = ctk.CTkButton(
            master=self.parameter_section,
            text="➕ Add",
            font=("Helvetica", 20, "bold"),
            height=50,
            corner_radius=100,
            fg_color="#4f772d",
            hover_color="#90a955",
            command=lambda: self.generate_list(False)
        )
        self.add.grid(row=3, column=2, sticky='nsew', padx=20, pady=(0, 30))

        # Clear Button
        self.clear = ctk.CTkButton(
            master=self.parameter_section,
            text="♻️ Clear",
            font=("Helvetica", 20, "bold"),
            height=50,
            corner_radius=100,
            fg_color="#a53860",
            hover_color="#da627d",
            command=self.clear_entries
        )
        self.clear.grid(row=3, column=3, sticky='nsew', padx=20, pady=(0, 30))

        # Options List
        self.options_list = ctk.CTkScrollableFrame(master=self.main_frame, corner_radius=16)
        self.options_list.pack(expand=True, fill="both", padx=20, pady=(10, 20))

    def clear_entries(self):
        for thing in self.college_widget_instances:
            try:
                thing.pack_forget()
            except AttributeError:
                pass
        self.options_list._parent_canvas.yview_moveto(0.0)

    def generate_list(self, clear_old: bool):
        # Clear old entries
        if clear_old:
            self.clear_entries()

        round_file = {
            "2024 MOCK": "assets/data/json/comedk-24-mock.json",
            "2024 Round 1": "assets/data/json/comedk-24-r1.json",
            "2024 Round 2": "assets/data/json/comedk-24-r2.json",
            "2024 Round 3": "assets/data/json/comedk-24-r3.json",
            "2025 MOCK": "assets/data/json/comedk-25-mock.json"
        }
        round_file = round_file[self.counselling_round_var.get()]

        for college in retrieve_colleges(round_file, self.college_var.get()[:4], self.rank_range_var.get(), self.course_select_var.get()):
            if len(college['courses']) != 0:
                college_widget = CollegeWidget(
                    master=self.options_list,
                    college_name=college['name'],
                    counselling_round=self.counselling_round_var.get(),
                    courses=college['courses']
                )
                self.college_widget_instances.append(college_widget)

        self.options_list._parent_canvas.yview_moveto(0.0)


def main():
    # CTk Settings
    ctk.set_appearance_mode('dark')
    try:
        ctk.set_default_color_theme('assets/ui/themes/lavender.json')
    except FileNotFoundError:
        print("[!] Theme JSON file not found! Falling back to classic dark")

    # Init
    app = ComedkApp()

    # Window Config
    app.title("COMED-K CUT-OFFS")
    app.geometry('1280x720')
    app.minsize(980, 540)

    # Start GUI mainloop
    app.mainloop()


if __name__ == '__main__':
    main()
