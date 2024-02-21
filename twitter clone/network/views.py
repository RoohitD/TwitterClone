from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like


def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()

    p = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    postsPerPage = p.get_page(page_number)

    allLikes = Like.objects.all()

    likedPosts = []

    try:
        for like in allLikes:
            if like.likingUser.id == request.user.id:
                likedPosts.append(like.likedPost.id)
    except: 
        likedPosts = []

    print(f"Length of liked{len(likedPosts)}")
    return render(request, "network/index.html", {
        "allPosts": postsPerPage,
        "likedPosts": likedPosts
    })

def likePost(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    newLike = Like(likingUser=user, likedPost=post)
    newLike.save()
    
    return JsonResponse({"message": "Like added succesfully"})

def unlikePost(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    removeLike = Like.objects.filter(likingUser=user, likedPost=post)
    removeLike.delete()

    return JsonResponse({"message": "Like removed succesfully"})

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(following=currentUser)
    allPosts = Post.objects.all().order_by("id").reverse()
    followingPosts = []

    for post in allPosts:
        for follow in following:
            if post.postUser == follow.followed:
                followingPosts.append(post)
    
    p = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    postsPerPage = p.get_page(page_number)

    return render(request, "network/following.html", {
        "allPosts": postsPerPage
    })

def editPost(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        editingPost = Post.objects.get(pk=post_id)
        editingPost.postContent = data["content"]
        editingPost.save()
        return JsonResponse({"message": "Successfully Edited Content", "data": data["content"]})

def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(postContent=content, postUser=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def profilePage(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.all().order_by("id").filter(postUser=user).reverse()
    following = Follow.objects.filter(following=user)
    follower = Follow.objects.filter(followed=user)
    p = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    postsPerPage = p.get_page(page_number)

    try:
        checkFollow = follower.filter(following=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else: 
            isFollowing = False
    except:
        isFollowing = False

    return render(request, "network/profilePage.html", {
        "allPosts": postsPerPage,
        "username": user.username,
        "following": following,
        "follower": follower,
        "isFollowing": isFollowing,
        "user_profile": user
    })

def follow(request):
    print("I was here follow")
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userfollow)
    f = Follow(following=currentUser, followed=userFollowData)
    f.save()
    user_id = userFollowData.id
    return HttpResponseRedirect(reverse(profilePage, kwargs={'user_id': user_id}))
 
def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(following=currentUser, followed=userFollowData)
    f.delete()
    user_id = userFollowData.id
    return HttpResponseRedirect(reverse(profilePage, kwargs={'user_id': user_id}))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
