from typing import Dict

from authentication.verification_strategy import EmailOtpVerificationStrategy, SMSOtpVerificationStrategy
from common.interface import VerificationInterface


class VerificationFactory:
    verification_strategy: Dict[str, VerificationInterface]

    def __init__(self, verification_strategy_type):
        self.verification_strategy_type = verification_strategy_type

        self.verification_strategy = {
            'Email': EmailOtpVerificationStrategy(),
            'SMS': SMSOtpVerificationStrategy()
        }

    def get_verification_strategy(self) -> VerificationInterface:
        print(self.verification_strategy_type)
        strategy = self.verification_strategy.get(self.verification_strategy_type, None)
        if strategy:
            return strategy
        raise ValueError("Invalid Verification Type")
