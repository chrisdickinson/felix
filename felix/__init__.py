from nappingcat.auth import AuthBackend
import simplejson
import os

class JSONAuth(AuthBackend):

    def get_auth_dict(self):
        settings_dict = dict(self.settings.items('jsonauth'))
        filename = os.path.expanduser(settings_dict.get('file', '~/nappingcat_auth.json')) 
        f = open(filename, 'r')
        json = simplejson.loads(f.read())
        f.close()
        return json

    def save_auth_dict(self, json):
        settings_dict = dict(self.settings.items('jsonauth'))
        filename = os.path.expanduser(settings_dict.get('file', '~/nappingcat_auth.json')) 
        f = open(filename, 'w')
        f.write(simplejson.dumps(json))
        f.close()

    def has_permission(self, user, permission):
        auth_dict = self.get_auth_dict()
        user_perms = auth_dict['users'].get(user, {})
        for level in permission:
            user_perms = user_perms.get(level, {}) 
        return bool(user_perms)

    def add_permission(self, user, permission):
        auth_dict = self.get_auth_dict()
        user_perms = auth_dict['users'].get(user, {})
        for level in permission[:-1]:
            next = user_perms.get(level, None)
            if next is None:
                user_perms[level] = {}
                user_perms = user_perms[level]

        user_perms[permission[-1]] = True
        self.save_auth_dict(auth_dict)

    def remove_permission(self, user, permission):
        auth_dict = self.get_auth_dict()
        user_perms = auth_dict['users'].get(user, {})
        for level in permission[:-1]:
            next = user_perms.get(level, None)
            if next is None:
                user_perms[level] = {}
                user_perms = user_perms[level]
        del user_perms[permission[-1]]
        self.save_auth_dict(auth_dict)

    def add_user(self, user):
        auth_dict = self.get_auth_dict()
        auth_user = auth_dict['users'].get(user, None)
        if auth_user is None:
            auth_dict['users'][user] = {
                'keys':[]
            }
        self.save_auth_dict(auth_dict)

    def add_key_to_user(self, user, key):
        auth_dict = self.get_auth_dict()
        auth_user = auth_dict['users'].get(user, None)
        auth_user['keys'] = [key] if not auth_user['keys'] else auth_user['keys'] + [key]
        self.save_auth_dict(auth_dict)
