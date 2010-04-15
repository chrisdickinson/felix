from nappingcat.exceptions import NappingCatRejected
from nappingcat import auth
import sys

PERMISSION_SEP = '::'

def add_user(request, username):
    if auth.has_permission(request, ('auth', 'adduser')):
        backend = auth.get_auth_backend_from_settings(request.settings)
        backend.add_user(username)
        return "Added user '%s'" % username
    raise NappingCatRejected("You don't have permission to add a user.")

def add_key_to_user(request, username):
    if auth.has_permission(request, ('auth', 'modifyuser')):
        backend = auth.get_auth_backend_from_settings(request.settings)
        key = sys.stdin.read()
        backend.add_key_to_user(username, key) 
        return "You added the key '%s...' to the user '%s'" % (key[0:30], username)
    raise NappingCatRejected("You don't have permission to modify users.")

def add_permission(request, username, permission):
    permission_tuple = permission.split(PERMISSION_SEP)
    # if you've got global rights to modifying users,
    # OR if you've already got the existing permission
    # you can pay it forward.
    if auth.has_permission(request, ('auth', 'modifyuser')) or auth.has_permission(request, permission_tuple):
        backend = auth.get_auth_backend_from_settings(request.settings)
        backend.add_permission(username, permission_tuple)
        return "You granted '%s' the permission '%s'" % (username, permission)
    raise NappingCatRejected("You really don't have the right to do that. Sorry.")

def remove_permission(request, username, permission):
    permission_tuple = permission.split(PERMISSION_SEP)
    user_owned_permission = request.user in permission_tuple[1:]
    # if the username is in the permission AND the user actually has
    # the permission, they can remove it from who they like.
    if auth.has_permission(request, ('auth', 'modifyuser')) or (user_owned_permission and auth.has_permission(request, permission_tuple)):
        backend = auth.get_backend_from_settings(request.settings)
        backend.remove_permission(username, permission_tuple)
        return "You removed the permission '%s' from '%s'." % (permission, username)
    raise NappingCatRejected("You really don't have the right to do that. Sorry.")
