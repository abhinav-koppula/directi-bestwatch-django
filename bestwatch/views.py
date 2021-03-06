import os, random, hashlib
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db.models import Avg
from bestwatch.models import Shows, Genres, Review_show, Rating_show, Login, Users, RegistrationForm, ProfilePic, ProfilePicForm 

def returnmd5(message):
    m = hashlib.md5()
    m.update(message)
    return m.hexdigest()

def index(request, loginFail = 0):
    
    offset = random.randint(0,Shows.objects.count()-12)
    twelve_random_shows = Shows.objects.all()[offset : offset+12]
    
    top_shows = []
    for show in Shows.objects.all():
        r = show.rating_show_set.aggregate(Avg('rating')).values()[0]
        if r:
            top_shows.append({'id':show.id, 'name':show.name, 'rating': r,})
    top_shows = sorted(top_shows, key = lambda k : k['rating'], reverse = True)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            l = form.save(commit=True)
            user = Users(login = l, name = request.POST.get('name'), profile_pic = 'avatar.jpg')
            saved_user = user.save()
            return redirect('/bestwatch/explore/0')
    else:
        form = RegistrationForm()

    context = {'form' : form, 'twelve_random_shows' : twelve_random_shows, 'top_shows':top_shows}
    if loginFail == '1':
        context['loginFail'] = 1
    else:
        context['loginFail'] = 0
    return render(request, 'home.html', context)

def explore(request, genre_id=0):
    if genre_id == '0':
        shows = Shows.objects.all()
        genre_id = 0
        genre_name = 'all'
    else:
        genre = get_object_or_404(Genres, pk=genre_id)
        genre_shows = genre.shows_genres_set.all()
        shows = []
        for s in genre_shows:
            shows.append(s.show)
        genre_id = genre.id
        genre_name = genre.name
        
    context = {'shows': shows, 'genre_id' : genre_id, 'genre_name': genre_name}
    return render(request, 'explore.html', context)
    
def get_average_rating(show):
    rat = 0
    ratings_count = show.rating_show_set.all().count()
    for r in show.rating_show_set.all():
        rat += r.rating
    if ratings_count>0:
        rat /= ratings_count
    return rat
    
def shows_detail(request, show_id):
    show = get_object_or_404(Shows, pk = show_id)
    genre_shows = show.shows_genres_set.all()
    genres = []
    for g in genre_shows:
        genres.append(g.genre)
    review_shows = show.review_show_set.all()
    reviews = []
    for r in review_shows:
        reviews.append(r)

    ratings_count = show.rating_show_set.all().count()
    rat = get_average_rating(show)

    context = {'show': show, 'genres': genres, 'reviews': reviews, 'ratings_count': ratings_count, 'rating': rat, }
    return render(request, 'shows_detail.html', context)

def set_session(request, login):
    session_dict = { 'login_id':login[0].id, 'email':login[0].email, 'name':login[0].users_set.all()[0].name, 'profile_pic':login[0].       users_set.all()[0].profile_pic }
    request.session['logged_in'] = session_dict

def set_session_obj(request, login):
    session_dict = { 'login_id':login.id, 'email':login.email, 'name':login.users_set.all()[0].name, 'profile_pic':login.           users_set.all()[0].profile_pic }
    request.session['logged_in'] = session_dict

def checkLogin(request):
    c = {}
    
    if request.POST:
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        login = Login.objects.filter(email = username)

    if login and login[0].password == returnmd5(password):
        set_session(request, login)
        return redirect('/bestwatch/explore/0')
    else:
        
        return redirect('/bestwatch/home/1')

def logout(request):
    del request.session['logged_in']
    return redirect('/bestwatch/')

def fblogin(request):
    return render(request, 'fblogin.html', {})

def checkFBLogin(request):
    if request.method == 'POST':
        femail = request.POST.get('email')
        fname = request.POST.get('name')
        fid = request.POST.get('id')
        login = Login.objects.filter(email=femail)
        if login:
            set_session(request, login)
        else:
            login_object = Login(email = femail, password = None)
            login_object.save()
            profile_pic_str = 'http://graph.facebook.com/' + fid + '/picture?type=large'
            user_object = Users(login = login_object, name = fname, profile_pic = profile_pic_str)
            user_object.save()
            set_session_obj(request, login_object)

        return HttpResponse("logged_in")
    else:
         return HttpResponse("not_logged_in")
         
def user_view_detail(request, user_id):
    user = get_object_or_404(Users, login = user_id)
    context = {'name':user.name, 'email':user.login.email, 'profile_pic':user.profile_pic}
    return render(request, 'profile.html', context)

def handle_uploaded_file(f):
    filepath = os.path.join(settings.MEDIA_ROOT, "images/")
    destination = open(filepath, "wb+")

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def user_edit(request):
    temp_path = os.path.join(settings.STATIC_ROOT, "img/temp/profpics")
    login_id = request.session['logged_in']['login_id']
    user = get_object_or_404(Users, login = login_id)
    context = {'name':user.name, 'email':user.login.email, 'profile_pic':user.profile_pic}
    file_exists = request.FILES.get('profpic', False)
    
    form = ProfilePicForm()

    if request.method == 'POST':
        if file_exists:
            file = request.FILES[u'profpic']
            if file.content_type not in ["image/jpeg","image/png",]:
                form.errors['__all__'] = form.error_class(["Only jpg and png supported"])
        
            if file.content_type in ["image/jpeg","image/png",]:
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)
            
                filename = os.path.join(temp_path, file.name)
                destination = open(filename, "wb+")
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()    

                user.profile_pic = file.name
                user.save()
                return redirect('/bestwatch/user/edit')
        else:
            form.errors['__all__'] = form.error_class(["Required"])
     
    context['form'] = form
    return render(request, 'profile.html', context)

def add_rating(request):
    if request.method == 'POST':
        show_id = request.POST.get('show_id')
        user_id = request.session['logged_in']['login_id']
        score = request.POST.get('score')
        s = Shows.objects.get(pk = show_id)
        u = Users.objects.get(login_id = user_id)
        
        r = Rating_show.objects.filter(show = s, user = u)
        if not r:
            rating_obj = Rating_show(show = s, user = u, rating = score)
            rating_obj.save()
            new_rating = get_average_rating(s)
            return HttpResponse(new_rating)
        else:
            return HttpResponse("You have already rated")

def add_review(request):
    user_id = request.session['logged_in']['login_id']
    show_id = request.POST.get('show_id')
    review = request.POST.get('review')
    s = Shows.objects.get(pk = show_id)
    u = Users.objects.get(login_id = user_id)

    r = Review_show(show = s, user = u, review = review)
    r.save()
    if r.pk:
        return HttpResponse("true")
    else:
        return HttpResponse("false")
