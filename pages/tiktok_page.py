import tkinter as tk
from tkinter import filedialog
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TikTokPage:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback

        self.page_frame = tk.Frame(self.master)
        self.page_frame.pack()

        label = tk.Label(self.page_frame, text='TikTok')
        label.pack(pady=20)

        self.create_buttons()
        self.selected_videopath = None

        back_button = tk.Button(self.page_frame, text="Назад", command=self.go_back)
        back_button.pack(pady=20)

    def create_buttons(self):
        buttons = [
            ("Ввести данные и авторизоваться", self.login_tiktok),
        ]
        for text, command in buttons:
            button = tk.Button(self.page_frame, text=text, command=command)
            button.pack(pady=5)

    def login_tiktok(self):
        self.open_login_dialog()

    def choose_videopath(self):
        video_path = filedialog.askopenfilename()
        self.selected_videopath = video_path

    def open_login_dialog(self):
        self.master.withdraw()
        input_window = tk.Toplevel(self.master)
        input_window.title("Введите данные")

        label = tk.Label(input_window, text='Введите описание, тайминг и выберите видео')
        label.pack(pady=20)

        title = self.create_input_field(input_window, "Введите описание:")
        timing = self.create_input_field(input_window, "Введите тайминг в полных секундах:")

        choose_button = tk.Button(input_window, text="Выбрать путь к mp4", command=self.choose_videopath)
        choose_button.pack(pady=20)

        save_button = tk.Button(input_window, text="Войти и загрузить",
                                command=lambda: self.log_and_load(title.get(), timing.get(), self.selected_videopath, input_window))
        save_button.pack(pady=10)
        input_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_add_dialog(input_window))

    def log_and_load(self, title, timing, video, input_window):
        input_window.destroy()
        self.master.deiconify()
        threading.Thread(target=self.continue_loading, args=(title, timing, video)).start()

    def continue_loading(self, title, timing, video):
        stop = False

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        WebDriverWait(driver, 120).until(EC.url_changes("https://www.tiktok.com/login/phone-or-email/email"))

        while True:
            try:
                driver.get("https://www.tiktok.com/tiktokstudio/upload")

                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))

                file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys(video)

                editable_div = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-text="true"]'))
                )
                editable_div.click()
                editable_div.send_keys(Keys.CONTROL, 'a')
                editable_div.send_keys(Keys.DELETE)
                editable_div = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.public-DraftStyleDefault-block'))
                )
                editable_div.click()
                editable_div.send_keys(title)

                publish_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'TUXButton') and .//div[text()='Опубликовать'] and @aria-disabled='false']"))
                )
                publish_button.click()

                WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Управляйте своими публикациями или загрузите еще видео.')]"))
                )

            except Exception as e:
                driver.quit()
                error_window = tk.Toplevel()
                error_window.title("Ошибка")
                error_window.geometry("300x150")
                error_label = tk.Label(error_window, text=f'Ошибка - {e}', wraplength=280)
                error_label.pack(pady=20)
                stop = True

            if stop:
                break

            try:
                timing_seconds = int(timing)
            except ValueError:
                print("Некорректное значение тайминга. Используется значение по умолчанию 100.")
                timing_seconds = 100

            if timing_seconds > 0:
                print(f"Ожидание {timing_seconds} секунд перед следующей загрузкой...")
                time.sleep(timing_seconds)

    def create_input_field(self, parent, label_text):
        tk.Label(parent, text=label_text).pack(pady=5)
        entry = tk.Entry(parent, width=40)
        entry.pack(pady=5)
        return entry

    def on_close_add_dialog(self, input_window):
        input_window.destroy()
        self.master.deiconify()

    def go_back(self):
        self.page_frame.pack_forget()
        self.go_back_callback()