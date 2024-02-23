import os
import sys

import customtkinter as CTk
from PIL import Image

from SaveFileObfuscator import SaveFileObfuscator


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class InfoFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.actual_info_label = CTk.CTkLabel(master=self, state="disable", width=120, height=45,
                                              text="Hello!\nHere must be\nsome info :)")
        self.actual_info_label.grid(row=0, column=1)

        self.pbr_label = CTk.CTkLabel(master=self, state="disable", width=120, height=45, text_color="magenta",
                                      text='Powered by REI\ngithub.com/whyREI')
        self.pbr_label.grid(row=1, column=1)


class HeadFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Icon
        self.sts_icon = CTk.CTkImage(dark_image=Image.open(resource_path("src/icons/sts_icon.png")), size=(90, 90))
        self.sts_icon_label = CTk.CTkLabel(master=self, text="", image=self.sts_icon)
        self.sts_icon_label.grid(row=0, column=0)

        # Info frame
        self.info_frame = InfoFrame(self)
        self.info_frame.grid(row=0, column=1, padx=(10, 0))


class ArrowFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.autosave_label = CTk.CTkLabel(master=self, state="disable", width=80, height=30,
                                           text=".autosave")
        self.autosave_label.grid(row=0, column=0)

        self.arrow_btn = CTk.CTkButton(master=self, width=60, height=30, text=master.ARROW_ARR[master.arrow],
                                       command=master.arrow_swap)
        self.arrow_btn.grid(row=0, column=1)

        self.json_label = CTk.CTkLabel(master=self, state="disable", width=80, height=30,
                                       text=".json")
        self.json_label.grid(row=0, column=2)


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("240x280")
        self.title("STS_SaveChanger")
        self.resizable(False, False)

        self.save = None

        self.head_frame = HeadFrame(self)
        self.head_frame.grid(row=0, column=0, padx=10, pady=(10, 30))

        # Arrow
        self.ARROW_ARR = {'right': '--->', 'left': '<---'}
        self.arrow = 'right'

        self.arrow_frame = ArrowFrame(self)
        self.arrow_frame.grid(row=1, column=0, padx=10, pady=(0, 20))

        # Path to file
        self.path_to_file = None
        self.path_file_btn = CTk.CTkButton(self, width=220, height=30, text="Path to file",
                                           command=self.take_path_to_file)
        self.path_file_btn.grid(row=2, column=0, padx=10, pady=(0, 20))

        # Transform
        self.transform_btn = CTk.CTkButton(self, width=220, height=40, text="Transform",
                                           command=self.transform_file)
        self.transform_btn.grid(row=3, column=0, padx=10, pady=(0, 0))

    def arrow_swap(self):
        self.arrow = 'left' if self.arrow == 'right' else 'right'
        self.arrow_frame.arrow_btn.configure(text=self.ARROW_ARR[self.arrow])

    def update_file_path_btn(self):
        self.path_file_btn.configure(text='.../' + self.path_to_file.split('/')[-1])

    def take_path_to_file(self):
        file_path = CTk.filedialog.askopenfilename(filetypes=[("Autosave files", "*.autosave"),
                                                              ("JSON files", "*.json")])
        if file_path.split('.')[-1] in ('autosave', 'json'):
            self.path_to_file = file_path
            self.update_file_path_btn()

    # Write new file and delete old file
    @staticmethod
    def wd_file(data, file_path, new_format):
        new_file = file_path.split(".")[-2] + "." + new_format
        # Write
        with open(new_file, 'w') as f:
            f.write(data)
        # Delete
        if os.path.exists(file_path):
            os.remove(file_path)

        return new_file

    def transform_file(self):
        if self.path_to_file:
            self.path_file_btn.configure(border_width=0)
            with open(self.path_to_file, 'r') as f:
                self.save = f.read()
        else:
            self.path_file_btn.configure(border_color="red", border_width=1)

        if self.save:
            new_file = None
            file_format = self.path_to_file.split(".")[-1]
            self.arrow_frame.arrow_btn.configure(border_width=0)
            if self.arrow == "right":
                # To .json
                if file_format == "autosave":
                    save_json = SaveFileObfuscator().decode(self.save)
                    new_file = self.wd_file(data=save_json, file_path=self.path_to_file, new_format="json")
                else:
                    self.arrow_frame.arrow_btn.configure(border_color="red", border_width=1)
            else:
                # To .autosave
                if file_format == "json":
                    save_autosave = SaveFileObfuscator().encode(self.save)
                    new_file = self.wd_file(data=save_autosave, file_path=self.path_to_file, new_format="autosave")
                else:
                    self.arrow_frame.arrow_btn.configure(border_color="red", border_width=1)

            if new_file:
                self.arrow_swap()
                self.path_to_file = new_file
                self.update_file_path_btn()


if __name__ == '__main__':
    app = App()
    app.mainloop()
