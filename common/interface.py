from abc import ABC, abstractmethod


class GenerateOTPInterface(ABC):

    @abstractmethod
    def generate_otp(self, otp_length=6):
        raise NotImplementedError("Sub class should have to implement this")


class VerificationInterface(ABC):

    @abstractmethod
    def verification(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")
