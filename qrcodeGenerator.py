import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

background_image_path = None
icon_image_path = None
color_start = "#000000"
color_end = "#000000"


def generate_qr_code():
    url = entry_url.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL to generate its QR code.")
        return

    try:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="transparent")

        if color_start and color_end:
            width, height = qr_image.size
            gradient_image = create_gradient_image(color_start, color_end, width, height)
            qr_image = apply_gradient_to_qrcode(qr_image, gradient_image)

        if icon_image_path:
            qr_image = add_icon_to_qrcode(qr_image)
        if background_image_path:
            qr_image = add_background_image_to_qrcode(qr_image)

        qr_image.save("website_qr.png")
        messagebox.showinfo("Success", "QR Code generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to generate QR code: " + str(e))


# QRcode operations

def add_background_image_to_qrcode(qr_image):
    background_image = Image.open(background_image_path).convert("RGBA")
    qr_image = qr_image.convert("RGBA")

    # Resize the background image to match the QR code's dimensions.
    background_image = background_image.resize((qr_image.size[0], qr_image.size[1]))

    # Create a new image to combine the background and the QR code.
    combined_image = Image.new("RGBA", qr_image.size)
    combined_image.paste(background_image, (0, 0))

    # Paste the QR code onto the background. Note
    combined_image.paste(qr_image, (0, 0), mask=qr_image)

    return combined_image


def add_icon_to_qrcode(qr_image):
    icon_image = Image.open(icon_image_path).convert("RGBA")
    icon_size = 100  # Define the size of the icon
    icon_image = icon_image.resize((icon_size, icon_size))

    # Calculate the position for the icon to be at the center.
    position = ((qr_image.size[0] - icon_size) // 2, (qr_image.size[1] - icon_size) // 2)
    mask = icon_image.split()[3]  # Use the alpha channel of the icon image as the mask.
    qr_image.paste(icon_image, position, mask=mask)

    return qr_image  # Return the updated QR code image.


def create_gradient_image(start_color, end_color, width, height):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []

    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)

    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def apply_gradient_to_qrcode(qr_image, gradient_image):
    qr_image = qr_image.convert('RGBA')
    gradient_image = gradient_image.resize(qr_image.size).convert('RGBA')

    # Create a new image to store the result
    result_image = Image.new('RGBA', qr_image.size)
    qr_pixels = qr_image.load()
    gradient_pixels = gradient_image.load()
    result_pixels = result_image.load()

    for y in range(qr_image.size[1]):
        for x in range(qr_image.size[0]):
            qr_pixel = qr_pixels[x, y]
            gradient_pixel = gradient_pixels[x, y]

            if qr_pixel[3] > 0:  # If QR code pixel is not transparent
                # Blend the QR code pixel with the gradient pixel
                result_pixels[x, y] = gradient_pixel
            else:
                # Keep the transparent pixels as they are
                result_pixels[x, y] = qr_pixel

    return result_image


# UI bond operations

def choose_background_image():
    global background_image_path
    background_image_path = filedialog.askopenfilename()
    if background_image_path:
        background_label.config(text="Background Image: " + background_image_path)
    else:
        background_label.config(text="No Background Image chosen")


def choose_icon_image():
    global icon_image_path
    icon_image_path = filedialog.askopenfilename()
    if icon_image_path:
        icon_label.config(text="Icon Image: " + icon_image_path)
    else:
        icon_label.config(text="No Icon Image chosen")


def choose_color_start():
    global color_start
    color_code = colorchooser.askcolor(title="Choose QR code start color")
    if color_code[1]:
        color_start = color_code[1]
        color_label_start.config(text="QR Code Start Color: " + color_start)


def choose_color_end():
    global color_end
    color_code = colorchooser.askcolor(title="Choose QR code end color")
    if color_code[1]:
        color_end = color_code[1]
        color_label_end.config(text="QR Code End Color: " + color_end)


# GUI setup
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("500x600")  # Adjust the window size

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

# Entry for URL
label_url = tk.Label(main_frame, text="Enter URL:")
label_url.grid(row=0, column=0, sticky="w")
entry_url = tk.Entry(main_frame, width=40)
entry_url.grid(row=0, column=1, pady=10, padx=10)

# Background Image Selection
button_background = tk.Button(main_frame, text="Choose Background Image", command=choose_background_image)
button_background.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
background_label = tk.Label(main_frame, text="No Background Image chosen")
background_label.grid(row=2, column=0, columnspan=2, sticky="w")

# Icon Image Selection
button_icon = tk.Button(main_frame, text="Choose Icon Image", command=choose_icon_image)
button_icon.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
icon_label = tk.Label(main_frame, text="No Icon Image chosen")
icon_label.grid(row=4, column=0, columnspan=2, sticky="w")

# QR Code Start Color Selection
color_label_start = tk.Label(main_frame, text="QR Code Start Color: #000000")  # Default color label
color_label_start.grid(row=5, column=0, columnspan=2, sticky="w")

button_color_start = tk.Button(main_frame, text="Choose QR Code Start Color", command=choose_color_start)
button_color_start.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)

# QR Code End Color Selection
color_label_end = tk.Label(main_frame, text="QR Code End Color: #000000")  # Default color label
color_label_end.grid(row=7, column=0, columnspan=2, sticky="w")

button_color_end = tk.Button(main_frame, text="Choose QR Code End Color", command=choose_color_end)
button_color_end.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)

# Generate QR Code Button
button_generate = tk.Button(main_frame, text="Generate QR Code", command=generate_qr_code)
button_generate.grid(row=10, column=0, columnspan=2, sticky="ew", pady=10)

# Entry point
root.mainloop()
