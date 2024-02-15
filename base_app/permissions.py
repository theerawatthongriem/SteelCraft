def manager_user(user):
    return user.is_superuser or user.is_staff 

def members_user(user):
    return user.is_active and not user.is_superuser or not user.is_staff 