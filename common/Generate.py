import random
import string
from common.interface import GenerateInterface


class GenerateDigitStrategy(GenerateInterface):

    def generate(self, length=6):
        # return ''.join(random.choices(string.digits, k=otp_length))
        return '111111'


class GenerateRoomId(GenerateInterface):

    def generate(self, length=10):
        return ''.join(random.choices(string.digits + string.ascii_letters, k=length))
