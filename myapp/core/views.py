from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import profile, Posts, Postlike, Followers
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_obj = User.objects.get(username=request.user)
    profile_obj = profile.objects.get(user = user_obj, user_id = user_obj.id)

    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(follower = request.user.username)
    for users_ in user_following:
        user_following_list.append(users_.user)
    
    for username in user_following_list:
        feed_list = Posts.objects.filter(user = username)
        feed.append(feed_list)

    feed_list = list(chain(*feed))
    isfeed = len(feed_list)

    #user suggestin
    user_all = User.objects.all()
    user_following_all = []
    
    for users in user_following:
        user_list = User.objects.get(username=users.user)
        user_following_all.append(user_list)

    suggestion_list = [x for x in list(user_all) if (x not in list(user_following_all)) ]
    current_user = User.objects.filter(username = request.user.username)
    final_suggesstion_list = [x for x in list(suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggesstion_list)

    username_profile = []
    username_profile_list = []
    for user_s in list(final_suggesstion_list):
        username_profile.append(user_s.id)
    
    for ids in list(username_profile):
        profile_list = profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_list)

    
    # post_obj = Posts.objects.all()
    index_suggestion_list = list(chain(*username_profile_list))
    context = {
        'profile': profile_obj, 
        'Posts':feed_list, 
        'isfeed':isfeed, 
        'suggestions':index_suggestion_list[:4]
        }
    return render(request,'index.html', context)
# the view control login of the signin of the user
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
            
        else:
            messages.info(request,'Wrong password or username')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
# This view control the signup
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, 
                password=password1)
                user.save()

                #rediret user to the setting page
                user_log = auth.authenticate(username=username, password=password1)
                auth.login(request, user_log)
                user_model = User.objects.get(username=username)

                new_profile = profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, "password Not matching")
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')

# The setting 
def settings(request):
    user_p = profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_p.profile_img
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_p.profile_img = image
            user_p.bio = bio
            user_p.location = location
            user_p.save()

            return redirect('settings')
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_p.profile_img = image
            user_p.bio = bio
            user_p.location = location
            user_p.save()

            return redirect('settings')

    else:      
        context = {'user_p': user_p}
        return render(request, 'setting.html',context)

def postupload(request):
    if request.method == 'POST':
        user = request.user.username
        post_img = request.FILES.get('post_img')
        caption = request.POST['post_caption']
        # create a post and add it into the posts model
        new_post = Posts.objects.create(user=user, post_image = post_img, caption = caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


def postlike(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Posts.objects.get(post_id=post_id)
    liked_filter = Postlike.objects.filter(likepost_id = post_id, username=username).first()
    
    if liked_filter == None:
        new_like = Postlike.objects.create(likepost_id = post_id,username=username)
        new_like.save()
        post.likes = post.likes + 1
        post.save()
        return redirect('/')
    else:
        liked_filter.delete()
        post.likes = post.likes - 1
        post.save()
        return redirect('/')


def userprofile(request, pk):

    user_obj = User.objects.get(username = pk)
    Profile_obj = profile.objects.get(user=user_obj)
    Posts_obj = Posts.objects.filter(user=pk)
    user_post_length = len(Posts_obj)

    follower_count = len(Followers.objects.filter(user = pk))
    following_count = len(Followers.objects.filter(follower = user_obj))
    follower = request.user.username

    if Followers.objects.filter(follower = follower, user = pk).first():
        button_text = 'Unfollow'
    else:
        button_text = "Follow"

    context ={
        'users':user_obj,
        'profile':Profile_obj,
        'posts':Posts_obj,
        'likes':user_post_length,
        'btn_text': button_text,
        "followercount":follower_count,
        "followingcount":following_count
    }
    return render(request, 'profile.html', context)


def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if Followers.objects.filter(follower = follower, user = user).first():
            delete_follow = Followers.objects.get(follower = follower, user = user)
            delete_follow.delete()
            return redirect('/profile/'+user)
        else:
            new_follow = Followers.objects.create(follower = follower, user = user)
            new_follow.save()
            return redirect('/profile/'+user)
    else:
        messages.info(request, "Unable to proceed with request")
        return redirect('/')