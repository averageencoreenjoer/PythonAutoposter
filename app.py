import tkinter as tk
from pages.instagram_page import InstagramPage
from pages.tiktok_page import TikTokPage
from pages.vk_page import VKPage
from pages.youtube_page import YouTubePage
from utils.icon_utils import open_icon


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Социальные сети")

        self.instagram_icon = open_icon('icons/instagram_icon.png', size=(300, 300))
        self.tiktok_icon = open_icon('icons/tiktok_icon.png', size=(300, 300))
        self.youtube_icon = open_icon('icons/youtube_icon.png', size=(300, 300))
        self.vk_icon = open_icon('icons/vk_icon.png', size=(300, 300))

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        self.create_button("Instagram", self.instagram_icon, self.open_instagram_page)
        self.create_button("TikTok", self.tiktok_icon, self.open_tiktok_page)
        self.create_button("VK", self.vk_icon, self.open_vk_page)
        self.create_button("YouTube", self.youtube_icon, self.open_youtube_page)

    def create_button(self, text, icon, command):
        button = tk.Button(self.main_frame, image=icon, command=command)
        button.image = icon
        button.pack(side=tk.LEFT, padx=10, pady=10)

    def open_instagram_page(self):
        self.main_frame.pack_forget()
        self.instagram_page = InstagramPage(self.master, self.go_back)

    def open_tiktok_page(self):
        self.main_frame.pack_forget()
        self.tiktok_page = TikTokPage(self.master, self.go_back)

    def open_vk_page(self):
        self.main_frame.pack_forget()
        self.vk_page = VKPage(self.master, self.go_back)

    def open_youtube_page(self):
        self.main_frame.pack_forget()
        self.youtube_page = YouTubePage(self.master, self.go_back)

    def go_back(self):
        if hasattr(self, 'youtube_page'):
            self.youtube_page.page_frame.pack_forget()
        self.main_frame.pack()