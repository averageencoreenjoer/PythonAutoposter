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


class InstagramPage:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback

        self.page_frame = tk.Frame(self.master)
        self.page_frame.pack()

        label = tk.Label(self.page_frame, text='Instagram')
        label.pack(pady=20)

        self.create_buttons()
        self.selected_videopath = None

        back_button = tk.Button(self.page_frame, text="Назад", command=self.go_back)
        back_button.pack(pady=20)

    def create_buttons(self):
        buttons = [
            ("Ввести данные и авторизоваться", self.login_instagram),
        ]
        for text, command in buttons:
            button = tk.Button(self.page_frame, text=text, command=command)
            button.pack(pady=5)

    def login_instagram(self):
        self.open_login_dialog()

    def choose_videopath(self):
        video_path = filedialog.askopenfilename()
        self.selected_videopath = video_path

    def open_login_dialog(self):
        self.master.withdraw()
        input_window = tk.Toplevel(self.master)
        input_window.title("Введите данные")

        label = tk.Label(input_window, text='Введите подпись, тайминг и выберите видео')
        label.pack(pady=20)

        title = self.create_input_field(input_window, "Введите подпись:")
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

        driver.get("https://www.instagram.com/")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        WebDriverWait(driver, 120).until(EC.url_changes("https://www.instagram.com/"))

        while True:
            try:
                driver.get("https://www.instagram.com/")

                create_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Создать')]"))
                )

                try:
                    create_button.click()
                except:
                    not_now_button = WebDriverWait(driver, 120).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Не сейчас')]"))
                    )
                    not_now_button.click()

                    create_button = WebDriverWait(driver, 120).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Создать')]"))
                    )
                    create_button.click()

                try:
                    file_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    file_input.send_keys(video)
                except:
                    publication_button = WebDriverWait(driver, 120).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Публикация')]"))
                    )
                    publication_button.click()

                    file_input = WebDriverWait(driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    file_input.send_keys(video)

                try:
                    ok_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
                    )
                    ok_button.click()
                    print("Окно 'OK' найдено и закрыто.")
                except:
                    print("Окно 'OK' отсутствует, продолжаем выполнение.")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@role='dialog' and @aria-label='Обрезать']")
                        )
                    )
                    print("Модальное окно 'Обрезать' найдено.")

                    crop_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@role='dialog' and @aria-label='Обрезать']//button")
                        )
                    )

                    driver.execute_script("arguments[0].scrollIntoView();", crop_button)
                    driver.execute_script("arguments[0].click();", crop_button)
                    print("Кнопка 'Выбрать размер и обрезать' нажата.")

                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//div[@role='dialog' and @aria-label='Обрезать']//span[contains(text(), '9:16')]")
                        )
                    )

                    format_9_16 = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                             "//div[@role='dialog' and @aria-label='Обрезать']//span[contains(text(), '9:16')]")
                        )
                    )

                    driver.execute_script("arguments[0].scrollIntoView();", format_9_16)
                    driver.execute_script("arguments[0].click();", format_9_16)
                    print("Формат 9:16 успешно выбран.")

                except Exception as e:
                    print(f"Ошибка при выборе разрешения 9:16: {e}")

                next_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Далее')]"))
                )
                next_button.click()

                next_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Далее')]"))
                )
                next_button.click()

                description_field = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Добавьте подпись…']"))
                )
                description_field.click()
                description_field.send_keys(title)

                share_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Поделиться')]"))
                )
                share_button.click()

                try:
                    WebDriverWait(driver, 120).until(
                        EC.any_of(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//img[@src='https://static.cdninstagram.com/rsrc.php/v4/yU/r/b_y28Mnuau9.gif']")
                            ),
                            EC.visibility_of_element_located(
                                (By.XPATH, "//div[@aria-level='1' and contains(@class, '_ac7a') and contains(text(), 'Видео Reels опубликовано')]")
                            )
                        )
                    )
                except Exception as e:
                    print(f"Ошибка при ожидании завершения загрузки: {e}")
                    raise

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
                print("Некорректное значение тайминга. Используется значение по умолчанию 0.")
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