# Standard modules.
from os import mkdir, path, stat, startfile
from configupdater import ConfigUpdater
from threading import Thread
from tkinter import messagebox
# Other modules.
import pyautogui as pyauto  # click, typewrite, press, keyDown, keyUp
import customtkinter as ct
from webbrowser import open as browser_open
from pynput.mouse import Listener
from urllib.request import urlopen, urlretrieve
# My modules.
from VN_Modules.Term_clear import clear_term
from VN_Modules.get_app_data import get_appdata

#  Made By Veernezus | Lampis Fotiadis | Use it at your own risk! | Do not edit for no reason!
#  Starting.


class main:
    VERSION = '1.0.2'  # Now on 1.0.3
    WIDTH = 400
    HEIGHT = 400
    APPDATA_SAME = get_appdata() + '\\Insta_bot'
    CONFIGS = ConfigUpdater(allow_no_value=True)

    def __init__(self) -> None:
        self.start_button_started = False
        self.use_mouse_clicking_value = False
        self.mouse_click_pos = []
        self.waited_first_time = None
        self.get_config()  # First
        self.check_update()
        self.root = ct.CTk()
        SCREEN_WIDTH = self.root.winfo_screenwidth()
        SCREEN_HEIGHT = self.root.winfo_screenheight()
        x = int((SCREEN_WIDTH/2) - (main.WIDTH/2))
        y = int((SCREEN_HEIGHT/2) - (main.HEIGHT/2))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.geometry(f'{main.WIDTH}x{main.HEIGHT}+{x-50}+{y}')
        self.root.title(f'Instagram Comments Bot | Version: {main.VERSION} :)')
        self.root.resizable(False, False)
        self.root.set_appearance_mode("System")
        ct.set_default_color_theme('dark-blue')
        self.root.attributes('-topmost', True)  # To pop window.
        self.root.attributes('-topmost', False)

        self.use_recommended_settings_box = ct.CTkCheckBox(
            master=self.root, text='\nUse recommended \nsettings.', text_font=('Arial', 9), height=15, width=9, state='disabled', command=self.use_recommended_settings_event)  # type: ignore
        self.use_recommended_settings_box.pack(pady=10, padx=60)
        self.use_recommended_settings_box.place(rely=0.06, relx=0.68)

        self.always_on_top_box = ct.CTkCheckBox(
            master=self.root, text='Keep app on top.', text_font=('Arial', 9), height=15, width=9, command=self.always_on_top_event)  # type: ignore
        self.always_on_top_box.pack(pady=10, padx=60)
        self.always_on_top_box.place(rely=0.097, relx=0.378)

        self.use_mouse_clicking = ct.CTkCheckBox(
            master=self.root, text='Force mouse clicking.', text_font=('Arial', 9), height=15, width=9, command=self.use_mouse_clicking_event)  # type: ignore
        self.use_mouse_clicking.pack(pady=10, padx=60)
        self.use_mouse_clicking.place(rely=0.098, relx=0.01)

        self.comment_box = ct.CTkEntry(
            master=self.root, placeholder_text='Comment...', placeholder_text_color="grey", corner_radius=15, width=250)  # type: ignore
        self.comment_box.pack(pady=10, padx=100)

        self.number_of_comments = ct.CTkOptionMenu(
            master=self.root, values=[str(numbers) for numbers in range(5, 151, 5)], button_color=['#36719F', '#144870'])  # type: ignore
        self.number_of_comments.pack(pady=10, padx=100)
        self.number_of_comments.set("Comments to make.")

        self.delay_of_comments = ct.CTkOptionMenu(
            master=self.root, values=['2 Seconds | Risk of ban'] +
            ['4 Seconds | Risk of ban'] + ['6 Seconds'] +
            ['8 Seconds'] + ['10 Seconds | Recommend...'] +
            [str(i)+' Seconds' for i in range(12, 21, 2)] +
            [str(i)+' Seconds' for i in range(40, 81, 20)],
            button_color=['#36719F', '#144870'])  # type: ignore
        self.delay_of_comments.pack(pady=10, padx=100)
        self.delay_of_comments.set("Delay of comments.")

        self.mouse_pos_set = ct.CTkButton(
            master=self.root, text='Set mouse position', width=5, command=self.mouse_pos_set_action)
        self.mouse_pos_set.pack(pady=10, padx=100)

        self.button_start = ct.CTkButton(
            master=self.root, text='Start', width=10, command=self.start_button_st)
        self.button_start.pack(pady=10, padx=100)
        # self.button_start.place(rely=0.8, relx=0.43)

        self.set_from_config()  # Last after the buttons initialize.
        # __init__

    @classmethod
    def check_update(cls):

        if cls.CONFIGS['Gui_saves']['check_update'].value == 'False':
            # No update check.
            promt = pyauto.confirm(
                text='WARNING\nYou have disabled the updates\nIf you didnt do this change press OK to enable updates.', title='Instagram comments bot ', timeout=3000)
            if promt == 'OK':
                main.set_config_value('Gui_saves', 'check_update', 'True')
            else:
                # So it checks for update if the user clicks OK.
                # Only returns when user doesnt click OK.
                return False

        update_get_url = 'https://raw.githubusercontent.com/veernezus/Instagram_auto_comment_bot/main/Version'

        # Checks if connection is present.
        try:
            update_get = urlopen(update_get_url)
            update_get = update_get.readline()
            update_get = update_get.decode('utf-8')
            update_get = update_get[:-1]
        except Exception:
            promt = pyauto.confirm(
                text=f'Cannot check for update\nCheck your network status or download update manualy\
                by clicking ok',
                title='Instagram comments bot ')
            if promt == 'OK':
                browser_open(
                    'https://github.com/veernezus/Instagram_auto_comment_bot/releases/')
            return False

        # IfGuard, if the update is the same.
        if cls.VERSION == update_get:
            return False

        # print(update_get)
        # if cls.VERSION != update_get:
        # If it needs an update.
        promt = pyauto.confirm(
            text='New update found\nDownload?', title='Instagram comments bot ')

        # IfGuard to cancel update.
        if promt == 'Cancel':
            return False

        # if promt == 'OK':
        try:
            urlretrieve(
                'https://github.com/veernezus/Instagram_auto_comment_bot/releases/download/test/main.exe',
                f'Instagram_bot_clicker_v{update_get}.exe')
            promt = pyauto.confirm(
                text=f'Install done\nVersion installed:{update_get}\nOpen Changelog?',
                title='Instagram comments bot ')
            if promt == "OK":
                browser_open(
                    'https://github.com/veernezus/Instagram_auto_comment_bot/releases/')
        except Exception as error:
            promt = pyauto.confirm(
                text=f'Error while trying to download the update\nPress Ok to download it manually,\
                Error: ({error})',
                title='Instagram comments bot ')
            if promt == 'OK':
                browser_open(
                    'https://github.com/veernezus/Instagram_auto_comment_bot/releases/')
        else:
            startfile(f'Instagram_bot_clicker_v{update_get}.exe')
            quit()

        return True

    @staticmethod
    def create_appdata_file():
        # If the directory does not exist, create one.
        if not path.exists(f'{main.APPDATA_SAME}'):
            mkdir(main.APPDATA_SAME)

        return True

    @classmethod
    def set_config_value(cls, section, option, value):
        cls.CONFIGS.set(section, option, value)

    def set_from_config(self):
        # Settings buttons values from config file.

        if main.CONFIGS['Gui_saves']['always_on_top'].value == 'True':
            # Setting keep on top button.
            self.always_on_top_box.select()
        else:
            self.always_on_top_box.deselect()

        if main.CONFIGS['Gui_saves']['force_mouse_clicking'].value == 'True':
            # Settings force_mouse_clicking button.
            self.use_mouse_clicking.select()
        else:
            self.use_mouse_clicking.deselect()

    @classmethod
    def get_config(cls):
        cls.create_appdata_file()
        # Default configs set from here | Changing the indent affects the file xD.
        cls.configs = fr"""
# Editing the file could cause errors.
# Values will change while interacting with the app so there is no reason to change them unless
# you know what you are doing, Possible values: (True, False, RESET_ALL (putting RESET_ALL as a value will reset everything to the default ) Anything else will cause errors.
# Do not change check_update unless you get slow loading time 
# Having the app non-updated will cause issues
# Use it at your own risk, if you get banned its your fault!

[Gui_saves]

check_update = True
force_mouse_clicking = False
always_on_top = False

[first_messages]
# messages being displayed for the first time.
force_mouse_clicking_warned = False
set_mouse_position_warned = False


"""

        with open(f'{cls.APPDATA_SAME}\\Configs.ini', 'a+') as cls.configs_file:
            cls.configs_file.seek(0)  # After here.

            if stat(cls.configs_file.name).st_size == 0:
                # If file is empty
                cls.CONFIGS.read_string(cls.configs)
                cls.CONFIGS.update_file()

                pyauto.alert(
                    text=f'Creating/Writing configs file... ',
                    title='Instagram comments bot ', timeout=350)

                return

            cls.CONFIGS.read(f'{cls.APPDATA_SAME}\\Configs.ini')
            cls.FILE_VALUES = []
            for sections in cls.CONFIGS.sections():
                # Keeping values from keys to replace them in the next for loop.
                for (each_key, each_val) in cls.CONFIGS.items(sections):
                    cls.FILE_VALUES.append(each_val.value)

            if 'RESET_ALL' in cls.FILE_VALUES:
                # If RESET_ALL found as value means reset is needed.
                cls.configs_file.truncate(0)
                return cls.get_config()

            cls.CONFIGS.read_string(cls.configs)
            # Outside for loop, used to iterate through cls.FILE_VALUES list.
            iter_values = 0
            for sections in cls.CONFIGS.sections():
                for (each_key, each_val) in cls.CONFIGS.items(sections):
                    if cls.CONFIGS.has_option(sections, option=each_key):
                        if each_val.raw_key.startswith('_'):
                            # Needs to be True after update.
                            cls.CONFIGS.set(
                                section=sections, option=each_key, value='True')
                        else:
                            # Classic.
                            try:
                                cls.CONFIGS.set(
                                    section=sections, option=each_key, value=cls.FILE_VALUES[iter_values])
                            except IndexError:
                                # False since it will be toggled through the app.
                                # IndexError expected as the bool list will be out of reach.
                                cls.CONFIGS.set(
                                    section=sections, option=each_key, value='False')
                                # print('a')
                            except Exception:
                                cls.CONFIGS.set(
                                    section=sections, option=each_key, value='RESET_ALL')
                                return None

                        iter_values += 1  # Needed

            cls.CONFIGS.update_file()  # Last always.

        return None

    def on_click(self, x, y, button, pressed):
        if self.clicked:
            return True
        self.mouse_click_pos = x, y
        self.clicked = True

        return True

    def mouse_pos_set_action(self):
        if main.CONFIGS['first_messages']['set_mouse_position_warned'].value != 'True':
            self.position_alert = messagebox.askquestion(
                'Instagram comments bot | Read!',
                'Open your browser and click on the comment box of the instagram post to get the position,\nWindow will not be responsive until you click\nPress Yes to continue')
            self.set_config_value(
                'first_messages', 'set_mouse_position_warned', 'True')

            # IfGuard | when user clicks no
            if self.position_alert == 'no':
                return False

        self.root.after(100)
        self.clicked = False
        while True:
            with Listener(on_click=self.on_click):
                self.root.after(100)
                if self.clicked == True:
                    # When user doesnt click in bottom right.
                    # type: ignore
                    if self.mouse_click_pos[0] < 1085 or self.mouse_click_pos[1] < 970:
                        # To focus messagebox.
                        self.root.attributes('-topmost', True)
                        self.promt = messagebox.askyesnocancel(
                            'Instagram comments bot ',
                            f'Are you sure you clicked on the comment box?\nPress no to set mouse position again, cancel to stop setting',
                            default='no')

                        if main.CONFIGS['Gui_saves']['always_on_top'].value != 'True':
                            self.root.attributes('-topmost', False)

                        if self.promt == False:
                            # No
                            self.clicked = False
                            continue

                        if self.promt == None:
                            # Cancel
                            self.mouse_click_pos = []
                            return

                    self.root.after(120)
                    self.root.bell()
                    pyauto.alert(
                        title='Instagram comments bot ',
                        text=f'Got position {self.mouse_click_pos}\nMake sure the position is correct otherwise it will cause clicking problems')
                    return True

    def use_recommended_settings_event(self):
        # Empty.
        pass

    def use_mouse_clicking_event(self):
        # 0 == off
        # To force mouse clicking.
        if self.use_mouse_clicking.get() == 0:
            self.use_mouse_clicking_value = False
            self.set_config_value('Gui_saves', 'force_mouse_clicking', 'False')
        else:
            if main.CONFIGS['first_messages']['force_mouse_clicking_warned'].value != 'True':
                pyauto.alert(title='Instagram comments bot ',
                             text=f'Make sure you click on the center-left of the comment box in order to work properly.\n(Wont work on minimized browser.)')
                self.set_config_value(
                    'first_messages', 'force_mouse_clicking_warned', 'True')

            self.set_config_value('Gui_saves', 'force_mouse_clicking', 'True')
            self.use_mouse_clicking_value = True

    def always_on_top_event(self):
        # Setting always on top.
        if self.always_on_top_box.get() == 0:
            self.root.attributes('-topmost', False)
            self.set_config_value('Gui_saves', 'always_on_top', 'False')
        else:
            self.set_config_value('Gui_saves', 'always_on_top', 'True')
            self.root.attributes('-topmost', True)

    def start_button_st(self):
        # To start (button_start_event)
        self.button_start_event_thread = Thread(
            target=self.button_start_event, daemon=True)

        self.button_start_event_thread.start()  # Last to run.
        return True

    def button_start_event(self):
        # Starting by self.start_button_st()
        # IfGuard so the user cannot start the program many times.
        if self.start_button_started == True:
            self.root.bell()
            return False

        self.user_comment = self.comment_box.get()
        self.user_number_of_comments = self.number_of_comments.get()
        self.user_delay_of_comments = self.delay_of_comments.get()[:2]

        # IfGuards.
        if not self.user_comment.strip():
            self.comment_box.configure(
                placeholder_text_color="red")
            self.comment_box.pack()
            self.root.bell()
            return False

        # When number of comments is/was not selected.
        if self.user_number_of_comments[0] == 'C':
            self.number_of_comments.configure(button_color='red')
            self.root.bell()
            return False

        self.number_of_comments.configure(
            button_color=['#36719F', '#144870'])

        # When number of comments is/was not selected.
        if self.user_delay_of_comments == 'De':
            self.delay_of_comments.configure(button_color='red')
            self.root.bell()
            return False

        # Setting back default colors.
        self.delay_of_comments.configure(
            button_color=['#36719F', '#144870'])

        self.comment_box.configure(
            placeholder_text_color="grey")

        if self.mouse_click_pos == []:
            # Mouse position was not given.
            pyauto.alert(
                title='Instagram comments bot ', text='You must set a mouse position first by clicking Set mouse position')
            self.root.bell()
            return False

        # Starting.
        self.delay_of_comments.configure(
            state='disabled')

        self.number_of_comments.configure(
            state='disabled')

        self.start_button_started = True
        self.button_start.configure(
            width=150, height=30, text="Running, don't use mouse...")

        self.user_number_of_comments = int(self.user_number_of_comments)
        self.user_delay_of_comments = int(self.user_delay_of_comments)
        self.waited_first_time = False

        for i in range(self.user_number_of_comments):
            if not self.waited_first_time:
                # So it doesnt wait long at the first click
                pyauto.sleep(2)
                self.waited_first_time = True
            else:
                pyauto.sleep(self.user_delay_of_comments+1.5)
            pyauto.click(self.mouse_click_pos)
            pyauto.typewrite(self.user_comment)
            pyauto.sleep(0.1)
            if self.use_mouse_clicking_value == True:
                # If user wants to force mouse click.
                pyauto.click(
                    self.mouse_click_pos[0] + 325, self.mouse_click_pos[1])
            else:
                pyauto.press('enter')

        self.button_start.configure(width=60, height=30, text="Start")
        self.delay_of_comments.configure(
            state='normal')
        self.number_of_comments.configure(
            state='normal')
        self.root.bell()
        self.start_button_started = False
        self.waited_first_time = False

        return False

    def on_closing(self):
        # When window closes.
        self.CONFIGS.update_file()
        self.root.destroy()

    def start_gui(self):
        # Always last.
        self.root.mainloop()
        return False


# Program.
if __name__ == '__main__':
    try:
        pyauto.alert(title='Instagram comments bot',
                     text='MADE BY LAMPIS, using custom tkinter \nPlease wait....', timeout=250)

        main().start_gui()

        clear_term()
    except Exception as error:
        pyauto.alert(title='Instagram comments bot',
                     text='Error occured while running the program, report the error on the github\n' +
                     f'Error : ({error!r})')
