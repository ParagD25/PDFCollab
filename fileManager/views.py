from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Topic, Feed
from .forms import FeedForm, CommentForm, CustomUserCreationForm, CustomUserChangeForm


# Create your views here.


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username Incorrect")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password incorrect")

    context = {"page": page}
    return render(request, "fileManager/register_login.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error occurred during Registrations")
    return render(request, "fileManager/register_login.html", {"form": form})


def home(request):
    search_element = (
        request.GET.get("search") if request.GET.get("search") != None else ""
    )
    feeds = Feed.objects.filter(
        Q(topic__topic__icontains=search_element) | Q(title__icontains=search_element)
    )

    topics = Topic.objects.all()
    context = {"feeds": feeds, "topics": topics}
    return render(request, "fileManager/home.html", context)


@login_required(login_url="/login")
def feed(request, pk):
    feed = Feed.objects.get(id=pk)
    feed_comments = feed.commented_feed.all()

    if request.method == "POST":
        comment = Comment.objects.create(
            user=request.user, feed=feed, comment_body=request.POST.get("comment_body")
        )

        return redirect("feed", pk=feed.id)

    context = {"feed": feed, "feed_comments": feed_comments}
    return render(request, "fileManager/feed.html", context)


@login_required(login_url="/login")
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    feed_comments = user.comment_set.all()
    feeds = user.feed_set.all()
    topics = Topic.objects.all()
    topic_count = Topic.objects.all()[0:5]
    context = {
        "user": user,
        "feed_comments": feed_comments,
        "feeds": feeds,
        "topics": topics,
        "topic_count": topic_count,
    }
    return render(request, "fileManager/profile.html", context)


@login_required(login_url="login")
def createFeed(request):
    form = FeedForm()
    topics = Topic.objects.all()
    valid_formats = ["application/pdf"]
    if request.method == "POST":
        if request.FILES["file"].content_type not in valid_formats:
            messages.error(request, "Only PDF files are allowed.")
            return redirect("create-feed")
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(topic=topic_name)

        Feed.objects.create(
            host=request.user,
            topic=topic,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            file=request.FILES["file"],
        )

        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "fileManager/feed_form.html", context)


@login_required(login_url="login")
def editFeed(request, pk):
    feed = Feed.objects.get(id=pk)
    form = FeedForm(instance=feed)
    topics = Topic.objects.all()
    if request.user != feed.host:
        return HttpResponse("Your are not allowed here!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(topic=topic_name)
        feed.title = request.POST.get("title")
        feed.topic = topic
        feed.description = request.POST.get("description")
        # feed.file = request.FILES["file"]
        feed.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "feed": feed}
    return render(request, "fileManager/feed_edit.html", context)


@login_required(login_url="/login")
def deleteFeed(request, pk):
    feed = Feed.objects.get(id=pk)

    if request.user != feed.host:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        feed.delete()
        return redirect("home")

    return render(request, "fileManager/delete.html", {"obj": feed})


@login_required(login_url="/login")
def editComment(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)

    if request.user != comment.user:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("feed", pk=comment.feed.id)

    context = {"form": form}
    return render(request, "fileManager/comment_form.html", context)


@login_required(login_url="/login")
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse("Not Allowed")

    if request.method == "POST":
        comment.delete()
        return redirect("feed", pk=comment.feed.id)

    return render(request, "fileManager/delete.html", {"obj": comment})


@login_required(login_url="/login")
def editUser(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)  # Set the new password
            user.save()
            return redirect("user-profile", pk=user.id)

    return render(request, "fileManager/edit_user.html", {"form": form})


def topicsPage(request):
    search = request.GET.get("search") if request.GET.get("search") != None else ""
    topics = Topic.objects.filter(topic__icontains=search)
    return render(
        request,
        "fileManager/topics.html",
        {"topics": topics},
    )
