import qrcode
from PIL import Image

# # Background image
# img_bg = Image.open('icse.jpg')
#
# # QRCode instance
# qr = qrcode.QRCode(
#     version=5,
#     error_correction=qrcode.constants.ERROR_CORRECT_H,
#     # Size of cell
#     box_size=5,
#     # Outer margin
#     border=3
# )
# qr.add_data('test text')
# qr.make()
# img = qr.make_image(fill_color="red", back_color="#23dda0")

url = "https://www.qrcode-monkey.com/"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=0,
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="transparent").convert('RGBA')

img.save('./qrcode_test2_3.png')
