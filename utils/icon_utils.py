from PIL import Image, ImageTk

def open_icon(path, size=(50, 50)):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)