# from flask import Flask
# from flask_restful import Resource, Api
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from flask import jsonify
from flask_principal import Permission, RoleNeed
import logging

# Define some basic roles and permissions
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


def configure_permissions(app):
    """Configure permissions for the given app."""
    from flask_principal import identity_loaded, UserNeed

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


# Initialize logging
logging.basicConfig(level=logging.INFO)


def require_admin(current_user):
    if not admin_permission.can():
        logging.warning(f"Unauthorized admin access attempt by: {current_user.id}")
        return jsonify({'error': 'You do not have admin permissions'}), 403


def require_user(current_user):
    if not user_permission.can():
        logging.warning(f"Unauthorized user access attempt by: {current_user.id}")
        return jsonify({'error': 'You do not have user permissions'}), 403
