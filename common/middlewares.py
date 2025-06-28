from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import get_language_from_request


class LanguageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.default = settings.LANGUAGE_CODE
        self.supported = set(k for k, _ in settings.LANGUAGES)

    def __call__(self, request):
        path = request.path_info
        if path.startswith('/__debug__/') or path.startswith('/i18n/'):
            return self.get_response(request)

        session = request.session
        url_lang = translation.get_language_from_path(path)

        if url_lang in self.supported:
            translation.activate(url_lang)
            request.LANGUAGE_CODE = url_lang
            session['lang_chosen'] = True

        else:
            if session.get('lang_chosen'):
                translation.activate(self.default)
                request.LANGUAGE_CODE = self.default

            else:
                lang = get_language_from_request(request, check_path=False)
                if lang not in self.supported:
                    lang = self.default

                if lang != self.default:
                    session['lang_chosen'] = True
                    new_path = f'/{lang}{path}'
                    if qs := request.META.get('QUERY_STRING'):
                        new_path += '?' + qs
                    return redirect(new_path)

                translation.activate(lang)
                request.LANGUAGE_CODE = lang
                session['lang_chosen'] = True

        response = self.get_response(request)
        response.setdefault('Content-Language', request.LANGUAGE_CODE)
        return response


class ChangeUserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.language != request.LANGUAGE_CODE:
                request.user.language = request.LANGUAGE_CODE
                request.user.save()
        response = self.get_response(request)
        return response
