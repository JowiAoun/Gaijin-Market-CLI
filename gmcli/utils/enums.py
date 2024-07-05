from enum import Enum

def tagUnknown(cls):
    """Override to return UNKNOWN for any value not matching an enum."""
    return cls.UNKNOWN

class TagCategory(Enum):
    TYPE = "type"
    QUALITY = "quality"
    EVENT_NAME = "eventName"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        return tagUnknown(cls)

class TagName(Enum):
    TROPHY = "Trophy"
    COMMON = "Common"
    RED_SKIES = "'Red Skies'"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        return tagUnknown(cls)
