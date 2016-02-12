def is_app_admin(user):
    """
    Determine if a user is the app admin
    """
    return user.has_perm('auth.hydro_prospector_app_admin')
