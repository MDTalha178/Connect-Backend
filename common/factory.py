from typing import Dict, Any

from authentication.Repository.UserRepository import UserRepository
from authentication.verification_strategy import EmailOtpVerificationStrategy, SMSOtpVerificationStrategy
from common.interface import VerificationInterface


class VerificationFactory:
    verification_strategy: Dict[str, VerificationInterface]

    def __init__(self, verification_strategy_type):
        self.verification_strategy_type = verification_strategy_type

        self.verification_strategy = {
            'EMAIL': EmailOtpVerificationStrategy(),
            'SMS': SMSOtpVerificationStrategy()
        }

    def get_verification_strategy(self) -> VerificationInterface:
        strategy = self.verification_strategy.get(self.verification_strategy_type, None)
        if strategy:
            return strategy
        raise ValueError("Invalid Verification Type")


class MessageFactory:
    """Factory for creating different message formats"""

    @staticmethod
    def create_chat_message(data, room_name) -> Dict[
        str, Any]:
        """Create a regular chat message payload"""
        return {
            'message': data['message'],
            'sender_id': data['sender_id'],
            'receiver_id': data['receiver_id'],
            'type': 'message',
            'room_name': room_name,
            'config_id': data['config_id']
        }

    @staticmethod
    def create_status_message(user_id: str, status: str) -> Dict[str, Any]:
        """Create a user status message payload"""
        return {
            'message_type': 'user_status',
            'message': f"User {status}",
            'user_id': user_id,
            'status': status.lower()
        }

    @staticmethod
    def create_notification_message(data, room_name) -> \
            Dict[str, Any]:
        """Create a notification message payload"""
        return {
            'message': data['message'],
            'sender_id': data['sender_id'],
            'receiver_id': data['receiver_id'],
            'room_name': room_name,
            'config_id': data['config_id']
        }
