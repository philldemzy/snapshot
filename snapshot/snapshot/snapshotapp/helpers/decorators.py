from functools import wraps

from jwt import decode
from jwt.exceptions import DecodeError

from django.http import JsonResponse
from django.conf import settings

from ..models import Photographer


def is_photographer(view):
    """
    check if request is from a logged-in user and also is a photographer
    """
    @wraps(view)
    def check(request, *args, **kwargs):
        token = request.headers.get('auth-token')
        if token is None:
            return JsonResponse({'error': 'authentication needed'}, status=403)

        # decode token
        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except DecodeError:
            return JsonResponse({'error': 'invalid token'}, status=403)
        except Exception as err:
            print(err)
            return JsonResponse({'error': 'invalid token'}, status=403)

        # check if user exists
        try:
            photographer = Photographer.objects.get(pk=payload['id'], email=payload['email'])
            is_photographer_ = payload['photographer']
        except KeyError:
            return JsonResponse({'error': 'invalid token'}, status=403)

        # go to view if all checks passed
        if photographer and is_photographer_:
            func = view(request, photographer, *args, **kwargs)
            return func
        return JsonResponse({'error': 'something went wrong'}, status=500)
    return check
