from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
import datetime as dt
from django.db import transaction
from .models import Image, Profile
from .forms import InfoImageForm, NewsLetterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/accounts/login')
def latest_images(request):
    date = dt.date.today()
    images = Image.todays_images()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('latest')

    else:
        form = NewsLetterForm()
    return render(request, 'allofinsta/insta-home.html', {"date": date, "images": images, "letterform": form})


@login_required(login_url='/accounts/login')
def search_results(request):
    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        searched_images = Image.search_by_image_name(search_term)
        message = f"{search_term}"

        return render(request, 'showme/search.html', {"message": message, "images": searched_images})

    else:
        message = "because you haven't searched for any term "
        return render(request, 'allofinsta/search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def image_detail(request, id):
    test = 'test'
    image = Image.objects.get(id=id)
    return render(request, 'allofinsta/details.html', {'image': image, 'test': test})


@login_required(login_url='/accounts/login/')
def image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "allofinsta/image.html", {"image": image})


@login_required(login_url='/accounts/login')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = InfoImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.editor = current_user
            image.save()
    else:
        form = InfoImageForm()
    return render(request, "new_image.html", {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):

    current_user = request.user
    current_user.id = request.user.id

    profiles = Image.objects.filter(editor__username__iexact=profile_id)
    # print(profiles)
    profile = Profile.objects.get(user__username__exact=profile_id)
    content = {
        "profiles": profiles,
        "profile": profile,
        "user": current_user,
        "profile_id": profile_id
    }
    return render(request, "profiles/profile.html", content)


def after_detail(request, id):
    # return HttpResponse(slug)
    image = Image.objects.filter(id=id).all()
    return render(request, 'allofinsta/after.html', {'image': image})


@login_required(login_url='/accounts/register')
def post(request):
    current_user = request.user
    profile = request.user.profile
    if request.method == 'POST':

        form = ImagePost(request.POST, request.FILES)

        if form.is_valid:
            image = form.save(commit=False)
            image.user = current_user
            image.profile = profile
            image.save()
            return redirect('profiles', current_user.username)
    else:
        form = ImagePost()

    title = "New Post"
    content = {
        "form": form,
        "title": title
    }
    return render(request, 'post.html', content)


@login_required(login_url='/accounts/login/')
def edit_profile(request, profile_id):

    current_user = request.user
    current_user.id = request.user.id

    profiles = Image.objects.filter(editor__username__iexact=profile_id)
    # print(profiles)
    profile = Profile.objects.get(user__username__exact=profile_id)
    content = {
        "profiles": profiles,
        "profile": profile,
        "user": current_user,
        "profile_id": profile_id
    }
    return render(request, "profiles/edit_profile.html", content)
