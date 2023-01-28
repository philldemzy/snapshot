from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .helpers.decorators import is_photographer
from .helpers.helpers import hash_pass, login_photographer, is_password
from .models import Photographer, Media


@csrf_exempt
def register(request):
    if request.method == "POST":
        # checks for all these fields must be checked from client end before post req is sent here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile_image')
        brand_name = request.POST.get('brand_name')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        other_addy = request.POST.get('other_addy')
        hashed_p = hash_pass(request.POST.get('password'))
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')

        # Check if photographer exists
        exists = Photographer.objects.filter(
            first_name=first_name,
            last_name=last_name,
            brand_name=brand_name
        ).first()

        if not exists:
            new_photographer = Photographer(
                first_name=first_name,
                last_name=last_name,
                bio=bio,
                profile=profile,
                phone_num=phone_num,
                email=email,
                brand_name=brand_name,
                country=country,
                state=state,
                city=city,
                password=hashed_p,
                other_addy=other_addy,
                min_price=min_price,
                max_price=max_price,
            )

            new_photographer.save()

            return JsonResponse({
                'success': 'created successfully',
                'token': login_photographer(new_photographer)
            }, status=201)

        return JsonResponse({'error': 'user exists'}, status=400)

    return JsonResponse({'error': 'wrong method'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # get user with email
        try:
            photographer = Photographer.objects.get(email=email)
        except Photographer.DoesNotExist:
            return JsonResponse({'error': 'user does not exist'}, status=400)

        if is_password(password, photographer.password):
            return JsonResponse({
                'success': 'logged in successfully',
                'token': login_photographer(photographer)
            }, status=201)

        return JsonResponse({'error': 'wrong username or password'}, status=400)

    return JsonResponse({'error': 'wrong method'}, status=400)


@csrf_exempt
@is_photographer
def upload_media(request, photographer):
    if request.method == "POST":
        media = request.FILES.get('media')
        alt = request.POST.get('alt')

        new_media = Media(
            photographer=photographer,
            upload=media,
            alt=alt,
        )
        new_media.save()
        return JsonResponse({'success': 'created successfully'}, status=200)

    return JsonResponse({'error': 'wrong method'}, status=400)
