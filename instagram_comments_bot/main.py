# Standard modules.
from distutils.version import Version
from time import sleep
import os
# Other modules.
import pyautogui as pyauto  # click, typewrite, press, keyDown, keyUp
import customtkinter as ct
import webbrowser
from pynput.mouse import Listener
from colorama import init
from urllib.request import urlopen
# My modules.
from VN_Modules.Term_clear import clear_term
from VN_Modules.get_app_data import get_appdata


#  Made By Veernezus | Lampis Fotiadis | use it at your own risk!
#  Starting.
class main:
    VERSION = '1.0.1\n'
    WIDTH = 400
    HEIGHT = 400
    APPDATA_SAME = get_appdata() + '/Insta_bot'

    def __init__(self) -> None:
        init()  # Coloroma init.
        self.root = ct.CTk()
        SCREEN_WIDTH = self.root.winfo_screenwidth()
        SCREEN_HEIGHT = self.root.winfo_screenheight()
        x = int((SCREEN_WIDTH/2) - (main.WIDTH/2))
        y = int((SCREEN_HEIGHT/2) - (main.HEIGHT/2))

        self.root.geometry(f'{main.WIDTH}x{main.HEIGHT}+{x-50}+{y}')
        self.root.title(f'Instagram Comments Bot | Version: {main.VERSION} :)')
        self.root.resizable(False, False)
        self.root.set_appearance_mode("System")
        ct.set_default_color_theme('dark-blue')
        self.mouse_click_pos = None

        self.url_open_check_box = ct.CTkCheckBox(
            master=self.root, text='  \nOpen post url on\n     web page.', text_font=('Arial', 9), height=15, width=15, command=self.url_open_check_box_event)
        self.url_open_check_box.pack(pady=10, padx=60)
        self.url_open_check_box.place(rely=0.06, relx=0.72)

        self.url_box = ct.CTkEntry(
            master=self.root, placeholder_text='Post url...', text_font=('default_theme', 9), placeholder_text_color="grey", corner_radius=15, width=250, state='disabled')  # type: ignore
        self.url_box.pack(pady=10, padx=60)

        self.comment_box = ct.CTkEntry(
            master=self.root, placeholder_text='Comment...', placeholder_text_color="grey", corner_radius=15, width=250)  # type: ignore
        self.comment_box.pack(pady=10, padx=100)

        self.number_of_comments = ct.CTkOptionMenu(
            master=self.root, values=[str(numbers) for numbers in range(4, 155, 8)], button_color=['#36719F', '#144870'])
        self.number_of_comments.pack(pady=10, padx=100)
        self.number_of_comments.set("Comments to make.")

        self.delay_of_comments = ct.CTkOptionMenu(
            master=self.root, values=['2 Seconds | Risk of ban!']+['4 Seconds | Risk of ban!'] +
            [str(i)+' Seconds' for i in range(6, 21, 2)], button_color=['#36719F', '#144870'])
        self.delay_of_comments.pack(pady=10, padx=100)
        self.delay_of_comments.set("Delay of comments.")

        self.mouse_pos_set = ct.CTkButton(
            master=self.root, text='Set mouse position', width=5, command=self.mouse_pos_set_action)
        self.mouse_pos_set.pack(pady=10, padx=100)

        self.button_start = ct.CTkButton(
            master=self.root, text='Start', width=10, command=self.button_start_event)
        self.button_start.pack(pady=10, padx=100)
        # self.button_start.place(rely=0.8, relx=0.43)

        # __init__

    @classmethod
    def check_update(cls):
        update = False

        update_get = urlopen(
            'https://raw.githubusercontent.com/veernezus/Instagram_auto_comment_bot/main/Version')
        update_get = update_get.readline()
        update_get = update_get.decode('utf-8')

        print(update_get)
        print(cls.VERSION)
        print(update_get == cls.VERSION)

    @classmethod
    def appdata_file(cls):
        # if not os.path.exists(f'{cls.APPDATA_SAME}'):
        #    with open(f'{cls.APPDATA_SAME}/Version','w') as version_file:

        # with open(f'{cls.APPDATA_SAME}'):
        pass

    def on_click(self, x, y, button, pressed):
        if self.clicked:
            return True
        self.mouse_click_pos = x, y
        self.clicked = True
        return True

    def mouse_pos_set_action(self):
        self.position_alert = pyauto.confirm(
            text='Open your browser and click on the comment box of the instagram post to get the position, press OK to continue', title='Instagram comments bot ')
        # IfGuard | when user clicks cancel.
        if self.position_alert == 'Cancel':
            return False

        self.clicked = False
        while True:
            with Listener(on_click=self.on_click):
                sleep(0.1)
                if self.clicked:
                    sleep(0.1)
                    self.url_box.bell()
                    pyauto.alert(
                        title='Instagram comments bot ', text=f'Got position {self.mouse_click_pos}\nMake sure the position is correct otherwise it will cause clicking problems')
                    return True

    def url_open_check_box_event(self):
        if self.url_open_check_box.get() == 0:
            self.url_box.configure(placeholder_text='')
            self.url_box.configure(state='disabled')
        else:
            self.url_box.configure(
                state='normal', placeholder_text='Post url...', placeholder_text_color='grey')

    def button_start_event(self):
        self.check_update()
        self.user_url_box = self.url_box.get()
        self.user_comment = self.comment_box.get()
        self.user_number_of_comments = self.number_of_comments.get()
        self.user_delay_of_comments = self.delay_of_comments.get()[:2]

        # IfGuards.
        if self.url_open_check_box.get() == 1:  # If the url_check_box is ticked.

            if not self.user_url_box.strip() or len(self.user_url_box) < 28 or not self.user_url_box[:28] == 'https://www.instagram.com/p/':
                self.url_box.configure(
                    placeholder_text_color="red")
                self.url_box.pack()
                self.url_box.bell()
                return False

        if not self.user_comment.strip():
            self.comment_box.configure(
                placeholder_text_color="red")
            self.comment_box.pack()
            self.comment_box.bell()
            return False

        # When number of comments is/was not selected.
        if self.user_number_of_comments[0] == 'C':
            self.number_of_comments.configure(button_color='red')
            self.number_of_comments.bell()
            return False

        self.number_of_comments.configure(
            button_color=['#36719F', '#144870'])

        # When number of comments is/was not selected.
        if self.user_delay_of_comments == 'De':
            self.delay_of_comments.configure(button_color='red')
            self.delay_of_comments.bell()
            return False

        # Setting back default colors.
        self.delay_of_comments.configure(
            button_color=['#36719F', '#144870'])

        self.url_box.configure(
            placeholder_text_color="grey")

        self.comment_box.configure(
            placeholder_text_color="grey")

        if self.mouse_click_pos == None:
            pyauto.alert(
                title='Instagram comments bot ', text='You must set a mouse position first by clicking Set mouse position')
            return False

        self.user_number_of_comments = int(self.user_number_of_comments)
        self.user_delay_of_comments = int(self.user_delay_of_comments)

        if self.url_open_check_box.get() == 1:
            webbrowser.open(self.user_url_box)
            sleep(4)
        else:
            sleep(1)

        for i in range(self.user_number_of_comments):
            pyauto.click(self.mouse_click_pos)
            pyauto.typewrite(self.user_comment)
            pyauto.sleep(0.1)
            pyauto.press('enter')
            sleep(self.user_delay_of_comments+2)

        self.url_box.bell()

    def start_gui(self):
        # Always last.
        self.root.mainloop()


# Program.
pyauto.alert(title='Instagram comments bot',
             text='Made by Lampis\nPlease wait....', timeout=500)


try:
    main().start_gui()
except Exception as error:
    print(f'ERROR : ({error})')
    pyauto.alert(title='ERROR OCCURED',
                 text=f'{error}')

clear_term()
