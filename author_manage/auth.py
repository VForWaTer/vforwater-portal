# -*- coding: utf-8 -*-
"""auth"""


from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    """CustomOIDCAuthenticationBackend"""

    def create_user(self, claims):
        user = super(CustomOIDCAuthenticationBackend, self).create_user(claims)
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()
        return user


    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        updated = False
        if not user.first_name:
            user.first_name = claims.get('given_name', '')
            updated = True
        if not user.last_name:
            user.last_name = claims.get('family_name', '')
            updated = True
        if updated:
            user.save()
        return user

    #def get_email(self, claims):
    #    email = claims.get('email')
    #    if not email:
    #        email = claims.get('sub')
    #    return email
    
    #def filter_users_by_claims(self, claims):
    #    """Create user with email base custom user model."""
    #    email = self.get_email(claims)
    #    if not email:
    #        return self.UserModel.objects.none()
    #    try:
    #        return self.UserModel.objects.filter(email=email)
    #    except self.UserModel.DoesNotExist:
    #        return self.UserModel.objects.none()
