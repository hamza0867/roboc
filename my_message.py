from enum import Enum, auto, unique


@unique
class MessageType(Enum):
    MAZE = auto()
    PLAY = auto()
    INFO = auto()
    GAME_OVER = auto()


class Message:
    def __init__(self, string_message, message_type):
        self.string_message = string_message
        self.message_type = message_type
