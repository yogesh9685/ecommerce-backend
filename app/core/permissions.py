from fastapi import HTTPException, status
from app.models.user import User


class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User) -> bool:
        user_permissions = {
            perm.name for role in current_user.roles for perm in role.permissions
        }
        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: '{perm}' required",
                )
        return True


def require_roles(*roles: str):
    def checker(current_user: User) -> User:
        user_roles = {role.name for role in current_user.roles}
        if not user_roles.intersection(set(roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required role to access this resource",
            )
        return current_user

    return checker
