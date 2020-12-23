from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from .models import UserSession
import requests
# is_authenticated

# Create your views here.
@login_required
def hello(request,template_name='hello.html'):
    is_cookie = request.COOKIES.get('is_cookie','')      
    if request.session.get('login_session_id','') != request.session.session_key:
        response = render(request,template_name,locals()) 
        response.set_cookie('is_cookie','0',max_age=365 * 24 * 60 * 60 )
        logout(request)
        url = reverse('client:sign_in')
        return HttpResponseRedirect(url)      
    user_id = request.user.id
    ##### API CALL ####
    url = 'https://api.imgflip.com/get_memes'
    r = requests.get(url)
    response = r.json()
    response_code = r.status_code
    response_data = response['data']['memes'][:5]
    msg = response['success']
    print('*** response_data ***',response_data)
    ##### API CALL ####
    response = render(request,template_name,locals()) 
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata.get('accept_btn'):
            response = render(request,template_name,locals()) 
            request.COOKIES['is_cookie'] = '1'  
            response.set_cookie('is_cookie','1',max_age=365 * 24 * 60 * 60 )
            try:
                session_obj = get_object_or_404(UserSession,user_id=request.user.id,session_key=request.session.session_key)
            except:
                session_obj = UserSession()
            session_obj.user_id = request.user.id 
            session_obj.session_key = request.session.session_key
            session_obj.allow_cookie = True
            session_obj.save()
            url = reverse('client:hello')
            # return HttpResponseRedirect(url)
            return response
        if postdata.get('decline_btn'):    
            response.set_cookie('is_cookie','0',max_age=365 * 24 * 60 * 60 )
            logout(request)
            url = reverse('client:sign_in')
            return HttpResponseRedirect(url)
    return response

def sign_in(request,template_name='auth/signin.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        username = postdata.get('username','')
        password = postdata.get('password','')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_authenticated:
                    # request.SESSION['login_session_id'] = request.session.session_key
                    login(request, user)
                    request.session['login_session_id'] = request.session.session_key
                    response = render(request,template_name,locals()) 
                    response.set_cookie('is_cookie','0',max_age=365 * 24 * 60 * 60 )
                    return HttpResponseRedirect(reverse('client:hello'))
                else:
                    logout(request)
                    url = reverse('client:sign_in')
                    return HttpResponseRedirect(url)
        else:
            logout(request)
            url = reverse('client:sign_in')
            return HttpResponseRedirect(url)
    response = render(request,template_name,locals())   
    response.set_cookie('is_cookie','0',max_age=365 * 24 * 60 * 60 )         
    return response 

@login_required
def sign_out(request):
    logout(request)
    url = reverse('client:sign_in')
    return HttpResponseRedirect(url)         