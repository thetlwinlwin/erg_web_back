from enum import Enum


class GServiceTypes(Enum):
    DRIVE = "drive"
    DOCS = "docs"


def get_scopes(type: GServiceTypes):
    all_scopes = {
        "drive": [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
    }
    return all_scopes[type.value]
