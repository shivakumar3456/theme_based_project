from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lg, logout 
from .models import Profile, Post, Votes_Comments, Photos
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        address = request.POST.get("address")
        constituency = request.POST.get("con")
        emailid = request.POST.get("email")
        password = request.POST.get('pass')
        mobile_number = request.POST.get('mbno')
        user = None
        try:
            user = User.objects.get(email=emailid)
            return HttpResponse("user exist")
        except:
            user = User.objects.create_user(username=username, email=emailid, password=password)
            user.is_staff=True
        user.save()
        print(constituency,mobile_number)
        try:
            profile = Profile(user=user, mobile_no=mobile_number, address=address, constituency=constituency, location="")
            profile.save()
        except:
            User.objects.filter(email=user.email).delete()
            return HttpResponse("unable to register")    
        print(user) 
        return redirect("login")


#login Page
def signup(request):
    return render(request,"user_signup.html")

def login(request):
    return render(request,"user_login.html")

def upload(request):
    if request.user.is_authenticated:
        return render(request,"upload.html")
    else:
        return render(request,"user_login.html")

        
@csrf_exempt
def upload_data(request):
    print('shiva')
    if request.user.is_authenticated:
        if request.method == 'POST':
            list_obj=request.POST
            print(request.POST)
            file_obj=request.FILES.getlist('file_data')
            j=0
            for i in range(len(file_obj)-1):
                j=j+1
                if 'application' in file_obj[i].content_type:
                    break
                
            profile_obj=Profile.objects.get(user=request.user)
            print(profile_obj)
            if j==0:
                post_obj=Post(user_post=profile_obj,constituency=list_obj['con'],area=list_obj['area'],description=list_obj['description'],problem_statement=list_obj['problem'],status_of_post='nv')
            else:
                post_obj=Post(user_post=profile_obj,constituency=list_obj['con'],area=list_obj['area'],description=list_obj['description'],problem_statement=list_obj['problem'],status_of_post='nv',file_data=file_obj[j-1])
            print(post_obj)
            post_obj.save()
            file_len=len(file_obj)-1
            if file_len==1:
                pass
            else:    
                for i in range(file_len):
                    if i != (j-1):
                        photos_obj=Photos(user_post=post_obj,photos_post=file_obj[i])
                        photos_obj.save()


            return redirect('upload')

        else:
            print(request.POST)
            return redirect('upload')
    else:
        return render(request,"user_login.html")

def newsfeed(request):
    if request.user.is_authenticated:
        postdata = Post.objects.all()
        return render(request,"newspage.html",{'post_data':postdata})
    else:
        return redirect('user_login')
def dashboard(request):
    pass

def newsfeed(request):
    if request.user.is_authenticated:
        postdata = Post.objects.all()
        return render(request,"newspage.html",{'post_data':postdata})
    else:
        return redirect('user_login')


def newsdata(request,name):
    if request.user.is_authenticated:
        print(name)
        postdata = Post.objects.get(id=name)
        try:
            votecomm= Votes_Comments.objects.filter(user_post=name)
        except:
            votecomm=[]
        photodata=Photos.objects.filter(user_post=name)
    
        return render(request,"newsdata.html",{'post_data':postdata,'vote_comm':votecomm,'photo_data':photodata})
    else:
        return redirect('user_login')



def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def login_view(request):
    if request.method == 'POST':
        # user = User.objects.create_user(**request.POST)
        #print(request.POST['email'],request.POST.get('password'))
        mail=request.POST.get("username")
        pw=request.POST.get("pass")
        user = authenticate(username=mail, password=pw)
        if user is None:
            user = authenticate(mail=mail, password=pw)
        print(user)
        if user is not None:
            lg(request, user)
            return redirect(reverse("all_news"))
        else:
            return HttpResponse("in valid credentials")





