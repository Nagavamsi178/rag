# admin/user access
from typing import Literal

Role = Literal["admin", "user"]

def can_view_document(
    role: Role,
    document_owner: str,
    current_user: str
) -> bool:
    if role == "admin":
        return True
    return document_owner == current_user


def can_delete_document(role: Role) -> bool:
    return role == "admin"
