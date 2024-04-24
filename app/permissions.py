from flask_principal import Permission, RoleNeed

# Define some basic roles and permissions
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


def configure_permissions(app):
    """Configure permissions for the given app."""
    from flask_principal import identity_loaded
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Load the user's roles into the identity object."""
        # Set the identity user object
        identity.user = sender.current_user
        
        # Add the UserNeed to the identity
        if hasattr(sender.current_user, 'id'):
            identity.provides.add(UserNeed(sender.current_user.id))

        # Assuming the user object has a 'roles' attribute
        if hasattr(sender.current_user, 'roles'):
            for role in sender.current_user.roles:
                identity.provides.add(RoleNeed(role.name))


def require_admin():
    if not admin_permission.can():
        abort(403)


def require_user():
    if not user_permission.can():
        abort(403)
