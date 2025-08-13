# Social Media Uploader

This is a Python script that allows you to upload videos to various social media platforms (Instagram, TikTok, VK, and YouTube) using a graphical user interface (GUI) built with `tkinter`. The script automates the process of logging in, selecting a video, and uploading it with a specified title and timing.

## Features

- **Multi-Platform Support**: Upload videos to Instagram, TikTok, VK, and YouTube.
- **User-Friendly Interface**: Simple and intuitive GUI for easy navigation.
- **Automated Uploading**: Automates the process of logging in and uploading videos.
- **Customizable Timing**: Set a delay between uploads.
- **Error Handling**: Displays error messages if something goes wrong during the upload process.

## Requirements

To run this script, you need the following Python packages installed:

- `tkinter` (usually comes pre-installed with Python)
- `Pillow` (for image handling)
- `selenium` (for browser automation)
- `webdriver_manager` (for managing ChromeDriver)

You can install the required packages using `pip`:

```bash
pip install pillow selenium webdriver_manager
```

## Usage

1. **Run the Script**: Execute the script using Python.

   ```bash
   python main.py
   ```

2. **Select a Platform**: The main window will display buttons for each social media platform. Click on the platform you want to upload to.

3. **Enter Details**: 
   - **Title/Description**: Enter the title or description for your video.
   - **Timing**: Specify the delay (in seconds) before the next upload.
   - **Select Video**: Choose the video file you want to upload.

4. **Login and Upload**: The script will open a browser window, log in to the selected platform, and upload the video. You may need to manually log in if the platform requires additional authentication (e.g., 2FA).

5. **Monitor Uploads**: The script will handle the upload process and display any errors if they occur.

## File Structure

- **`social_media_uploader.py`**: The main script containing the GUI and upload logic.
- **`icons/`**: Directory containing icons for each social media platform (e.g., `instagram_icon.png`, `tiktok_icon.png`, etc.).

## Notes

- **Browser Automation**: The script uses Selenium to automate the browser. Ensure that you have the latest version of Chrome installed.
- **Manual Login**: Some platforms may require manual login (e.g., entering a 2FA code). The script will wait for you to complete the login process.
- **Error Handling**: If an error occurs during the upload process, a new window will pop up displaying the error message.

## Example

Here’s a quick example of how to use the script:

1. Run the script.
2. Click on the "Instagram" button.
3. Enter the title, timing, and select the video file.
4. The script will open a browser, log in to Instagram, and upload the video.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Any feedback or suggestions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This script is for educational purposes only. Use it responsibly and ensure you comply with the terms of service of the respective social media platforms.
