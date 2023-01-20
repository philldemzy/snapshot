from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from snapshot.photographer.helpers import hash_pass
from snapshot.photographer.models import Photographer


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
                brand_name=brand_name,
                country=country,
                state=state,
                city=city,
                password=hashed_p,
                other_addy=other_addy
            )

            new_photographer.save()
            # TODO login user
            return JsonResponse({{'success': 'created successfully'}}, status=201)

        else:
            return JsonResponse({'error': 'user exists'}, status=401)
