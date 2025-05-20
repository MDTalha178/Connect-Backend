from authentication.models import OnlineStatus

COMMUNICATION_MODE = [
    'EMAIL', 'SMS'
]

USER_STATUS = {
    'online': OnlineStatus.ONLINE,
    'offline': OnlineStatus.OFFLINE
}
