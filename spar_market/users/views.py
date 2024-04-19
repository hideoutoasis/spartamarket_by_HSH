from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {
        "member":member
    }
    return render(request, "profile.html", context)

@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("profile", username=member.username)
    return redirect("accounts:login")