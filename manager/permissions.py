def manager_user(user):
    return user.is_superuser or user.is_staff 