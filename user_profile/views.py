from django.shortcuts import render
from .forms import UserProfileForm


def profile(request):
    user_form = UserProfileForm(instance=request.user.userprofile)

    template = 'user_profile/profile.html'

    context = {
        'user_form': user_form
    }

    return render(request, template, context)
