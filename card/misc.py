import os
import qrcode
import cv2
from pyzbar import pyzbar
import random
import string

from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

img_path = os.path.join(os.getcwd(), "img")


class FileManager:
    selected_file = None

    def __init__(self):
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser(img_path))
        self.manager_open = True

    def select_path(self, path: str):
        """
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        """

        self.selected_file = path
        self.exit_manager()
        return path

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def open_file_manager():
        file_manager = MDFileManager(
            preview=True,
        )
        file_manager.show(img_path)


def generate_rfid(length=10):
    rfid = "".join(random.choices(string.digits, k=length))
    return rfid


def create_qr_code():
    rfid = generate_rfid()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(rfid)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_name = os.path.join(img_path, f"{rfid}.png")
    img.save(img_name)
    return rfid


def read_qr_code():
    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detect barcodes in the frame
        barcodes = pyzbar.decode(frame)

        # Loop over the detected barcodes
        for barcode in barcodes:
            # Extract barcode data and type
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Print the barcode data and type
            print(f"Found {barcode_type}: {barcode_data}")
            return barcode_data

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    return None
