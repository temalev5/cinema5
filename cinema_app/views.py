from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from .models import MovieRoom,MovieUser
from django.core import serializers
import json
from threading import Timer

# Create your views here.
def remove_room(movie_room_one):
    movie_room_one.delete()



def movie(request):
    if (request.method == "GET"):
        movie_rooms = MovieRoom.objects.all()
        info = {
            'movie_rooms' : movie_rooms,
        }
        response = render(request,'index.html',info)
        if (request.COOKIES.get('session') is None):
            response.set_cookie(key='session',value=get_random_string(length=32),max_age= (365 * 24 * 60 * 60))
            return response
        else:
            session = request.COOKIES.get('session')
            try:
                user = MovieUser.objects.get(token=session)
                info = {
                    'movie_rooms': movie_rooms,
                    'user_name': user.user_name,
                }
                return render(request, 'index.html', info)
            except:
                return response
    else:
        form = request.POST.get('kino_ID')
        obj = MovieRoom.objects.create(MovieRoom_Name='movie room #1', Movie_ID=form, MovieRoom_playing = False, MovieRoom_timming = 0)
        obj.MovieRoom_Name = 'movie room #'+str(obj.id)
        obj.save()
        return redirect('/room?id='+str(obj.id))


def room(request):
    if (request.method == "GET"):
        if request.is_ajax():
            user = MovieUser.objects.get(token=request.COOKIES.get('session'))
            movie_room_one = MovieRoom.objects.get(id=request.GET.get('id'))
            if (user.movie_room is None):
                user.movie_room = movie_room_one
                user.save()
            data = MovieUser.objects.filter(movie_room=movie_room_one).values('user_name','token','user_status')
            new_data={}
            for i in range(len(data)):
                new_data[i] = data[i]
            return JsonResponse({'room_title':movie_room_one.MovieRoom_Name,'result': new_data})
        else:
            try:
                movie_room_one = MovieRoom.objects.get(id=request.GET.get('id'))
            except:
                return redirect('home')
            if (request.COOKIES.get('session') is None):
                session = get_random_string(length=32)
                response = request.set_cookie(key='session', value=session, max_age=(365 * 24 * 60 * 60))
                user = MovieUser.objects.create(user_name='noname',token=session,user_status=False,movie_room=movie_room_one)
                user.save()
                print(str(user.user_name))
            else:
                try:
                    print('Я try GET')
                    user = MovieUser.objects.get(token=request.COOKIES.get('session'))
                    user.movie_room = movie_room_one
                    user.save()
                    print('Я GET')
                except:
                    user = MovieUser.objects.create(user_name='noname',token=request.COOKIES.get('session'),user_status=False,movie_room=movie_room_one)
                    user.movie_room = movie_room_one
                    user.save()
            room_users = MovieUser.objects.filter(movie_room=request.GET.get('id'))
            info = {
               'movie': movie_room_one,
               'room_users': room_users,
                'user': user,
            }
            return render(request,'room.html',info)
    else:
        if request.is_ajax():
            if (request.POST['type'] == "status"):
                session = request.POST['session']
                user_status = request.POST['user_status']
                print(user_status)
                user = MovieUser.objects.get(token=session)
                if (user_status== 'true'):
                    user.user_status = True
                else:
                    user.user_status = False
                user.save()
                return JsonResponse({'result':'success'})
            elif (request.POST['type'] == "settings"):
                movie_room_one = MovieRoom.objects.get(id=request.GET.get('id'))
                server_title = request.POST['server_title']
                if (movie_room_one.MovieRoom_Name != server_title):
                    movie_room_one.MovieRoom_Name = server_title
                    movie_room_one.save()
                session = request.POST['token']
                user_name = request.POST['user_name']
                user = MovieUser.objects.get(token=session)
                if (user.user_name != user_name):
                    user.user_name = user_name
                    user.save()
                return JsonResponse({'result': 'success'})
            elif (request.POST['type'] == "leave"):
                session = request.POST['session']
                movie_room_one = MovieRoom.objects.get(id=request.GET.get('id'))
                user = MovieUser.objects.get(token=session)
                if (user.movie_room == movie_room_one):
                    user.movie_room = None
                    user.user_status = False
                    user.save()
                    print('я POST')
                user = MovieUser.objects.filter(movie_room=movie_room_one).values('movie_room')
                if (len(user)==0):
                    print('я поппал в таймер и че')
                    Timer(300, remove_room,args=(movie_room_one,)).start()
                print(len(user))
                #if movie_roome_one
                return JsonResponse({'result': 'success'})

