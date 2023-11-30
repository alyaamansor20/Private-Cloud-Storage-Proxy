import secrets
import string
import uuid
import image
import qrcode as qrcode


class HostManager:

    """
    Holds Information about the host
    """

    def __init__(self, ip_address, port_number):
        self.mIpAddress = ip_address
        self.mPortNumber = port_number
        self.mUid = str(uuid.uuid4())
        self.mPassword = ""

        symbols = ['#', '$', '&', '@']  # Can add more
        for _ in range(8):
            self.mPassword += secrets.choice(string.ascii_lowercase)
            self.mPassword += secrets.choice(string.ascii_uppercase)
            self.mPassword += secrets.choice(string.digits)
            self.mPassword += secrets.choice(symbols)

        self.__generate_qrcode()

    def __generate_qrcode(self):
        qr_msg = self.mIpAddress + "," + str(self.mPortNumber) + "," + self.mUid + "," + self.mPassword
        qr_img = qrcode.make(qr_msg)
        qr_img.save("Proxy Information QR Code.png")
