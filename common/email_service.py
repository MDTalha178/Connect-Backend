from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):

    @abstractmethod
    def send_email(self, data, **kwargs):
        raise NotImplementedError("Sub class should have to implement this")


class SMTPEmailService(EmailServiceInterface):

    def send_email(self, data, **kwargs):
        pass
    