from django.shortcuts import render
from .forms import UserProfileForm
from django.contrib import messages


def profile(request):
    user_form = UserProfileForm(instance=request.user.userprofile)

    if request.POST:
        user_form = UserProfileForm(request.POST,
                                    instance=request.user.userprofile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully.')

    template = 'user_profile/profile.html'

    context = {
        'user_form': user_form,
        'user_email': request.user.email
    }

    return render(request, template, context)
