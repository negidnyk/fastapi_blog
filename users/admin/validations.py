from fastapi import HTTPException


def is_admin_or_superadmin(role_id):
    if role_id != 1 or role_id != 3:
        raise HTTPException(status_code=403, detail="This option is for admins only!")


def is_superadmin(role_id):
    if role_id != 3:
        raise HTTPException(status_code=403, detail="This option is for superadmins only!")
