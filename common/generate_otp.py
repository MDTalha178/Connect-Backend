import random
import string
from common.interface import GenerateOTPInterface


class GenerateDigitOTPStrategy(GenerateOTPInterface):

    def generate_otp(self, otp_length=6):
        # return ''.join(random.choices(string.digits, k=otp_length))
        return '111111'
