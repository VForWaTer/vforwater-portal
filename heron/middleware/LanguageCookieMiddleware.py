from django.utils import translation
from django.conf import settings


# TODO: Now on every request django checks for a language cookie. Maybe set language in URL instead.
class LanguageCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # self.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'en-gb')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        """
        Sets language from the cookie value.
        """
        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES:
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            # translation.activate(language)
            # request.LANGUAGE_CODE = translation.get_language()
        else:
            language = 'en'

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.
        """
        Create cookie if not there already.

        Also deactivates language.
        (See http://stackoverflow.com/a/13031239/388835 )
        """
        if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'en-gb')
        translation.deactivate()
        return response
