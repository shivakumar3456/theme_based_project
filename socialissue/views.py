from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lg, logout 
from .models import Profile, Post, Votes_Comments, Photos , Only_votes
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.db.models import CharField, Case, Value, When

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
            profile = Profile(user=user, mobile_no=mobile_number, designation='n',address=address, constituency=constituency, location="")
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
def newscontent(request):
    if request.user.is_authenticated:
        '''
        pv1 = request.POST['probview']
        pv2 = request.POST['probview1']
        postareaobj=None
        if pv1 == 'area' and pv2 != '':
            try:
                postareaobj = Post.objects.filter(constituency=pv2)
            except:
                pass
                
            return render(request,"newspage.html",{'post_data':postareaobj})
        elif pv1 == 'problem' and pv2 !='':
            try:
                postareaobj = Post.objects.filter(problem_statement=pv2)
            except:
                pass
            return render(request,"newspage.html",{'post_data':postareaobj})
        else:
            return redirect('newsfeed')
        '''
        print(request.POST)
        return HttpResponse("ss")
    else:
        return render(request,'user_login.html')

@csrf_exempt
def comment(request):
    if request.user.is_authenticated and request.method == "POST":
        comm = request.POST['comment']
        postid=request.POST['postid']
        profileobj= Profile.objects.get(user=request.user)
        postobj= Post.objects.get(id=int(postid))
        vandc= Votes_Comments(user_post=postobj,user_vote=profileobj,comment=comm)
        vandc.save()
        return redirect('/newsdata/'+postid+'/')

    else:
        return redirect('login')
       
@csrf_exempt
def vote(request,postid,voted):
    if request.user.is_authenticated:
        profileobj= Profile.objects.get(user=request.user)
        postobj= Post.objects.get(id=int(postid))
        try:
            if voted == 'u':
                vandc= Only_votes(user_post=postobj,user_vote=profileobj,upordown=voted)
                postobj.upvote_count=postobj.upvote_count+1
            else:
                vandc=Only_votes(user_post=postobj,user_vote=profileobj,upordown=voted)
                postobj.downvote_count=postobj.downvote_count+1
            vandc.save()
            postobj.save()
        except:
            pass            
        
        return redirect('/newsdata/'+str(postid)+'/')
    else:
        return redirect('login')
    


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
'''
def newsfeed(request):
    if request.user.is_authenticated:
        postdata = Post.objects.all()
        return render(request,"newspage.html",{'post_data':postdata})
    else:
        return redirect('user_login')
'''

def dashboard(request):
    pass

def newsfeed(request):
    if request.user.is_authenticated:
        proobj=Profile.objects.get(user=request.user)
        if proobj.designation=='n': 
            postdata = Post.objects.exclude(status_of_post='nv').exclude(status_of_post='s')
            return render(request,"newspage.html",{'post_data':postdata})
        elif proobj.designation=='p':
            postdata = Post.objects.filter(status_of_post='p',constituency=proobj.constituency)
            return render(request,"polnewspage.html",{'post_data':postdata}) 
        else:
            postdata1 = Post.objects.filter(status_of_post='nv')
            post1=Post.objects.filter(status_of_post='v')
            l=[]
            for i in postdata1:
                l.append(i)
            for i in post1:
                if i.alloted_time.date() < date.today():
                    l.append(i) 
            print(l)
            return render(request,"adminnewspage.html",{'post_data':l})  
    else:
        return redirect('user_login')


def newsdata(request,name):
    if request.user.is_authenticated:
        proobj=Profile.objects.get(user=request.user)
        print(request.POST)
        postdata = Post.objects.get(id=name)
        obj=''
        conval=False
        if postdata.status_of_post=='v':
            conval=True
            obj='due date to raise the issue '+str(postdata.alloted_time)
        else:
          
            obj='your problem will be solved by '+str(postdata.alloted_time)
        try:
            votecomm= Votes_Comments.objects.filter(user_post=name)
        except:
            print('e')
            votecomm=[]
    
        ovobj = Only_votes.objects.filter(user_vote=proobj.id,user_post=postdata.id)
        if ovobj is None:
            ovobj=[]
        photodata=Photos.objects.filter(user_post=name)
        print(ovobj,name,postdata,proobj.id,postdata.id)
        if proobj.designation=='n': 
            return render(request,"newsdata.html",{'somedata':obj,'ov_obj':ovobj,'post_data':postdata,'vote_comm':votecomm,'photo_data':photodata})
        elif proobj.designation=='p':
            return render(request,"polnewsdata.html",{'ov_obj':ovobj,'post_data':postdata,'vote_comm':votecomm,'photo_data':photodata})
        else:
            return render(request,"adminnewsdata.html",{'cval':conval,'ov_obj':ovobj,'post_data':postdata,'vote_comm':votecomm,'photo_data':photodata})

    else:
        return redirect('user_login')
@csrf_exempt
def accept(request,postid):
    if request.user.is_authenticated:
        proobj = Profile.objects.get(user=request.user)
        postobj= Post.objects.get(id=postid)
        if proobj.designation=='a':
            postobj.status_of_post='v'
            postobj.alloted_time=request.POST['time']
            postobj.save()
            return redirect('all_news')
        if proobj.designation=='p':
            postobj.alloted_time=request.POST['time']
            postobj.save()
            return redirect('all_news')

    else:
        return redirect('login')
@csrf_exempt
def reject(request,postid):
    if request.user.is_authenticated:
        proobj = Profile.objects.get(user=request.user)
        postobj= Post.objects.get(id=postid)
        if proobj.designation=='a':
            postobj.status_of_post='r'
            postobj.save()
            return redirect('all_news')
    else:
        return redirect('login')

def posted(request,postid):
    if request.user.is_authenticated:
         postobj=Post.objects.get(id=postid)
         postobj.status_of_post='p'
         postobj.save()
         return redirect('all_news')
    else:
        return redirect('login')         


@csrf_exempt
def viewfile(request,postid):
    if request.user.is_authenticated:
        postobj=Post.objects.get(id=postid)
        return redirect(postobj.file_data.url)
    else:
        return redirect('login')

def solved(request,postid):
    if request.user.is_authenticated:
        postobj=Post.objects.get(id=postid)
        postobj.status_of_post='s'
        postobj.save()
        return redirect("all_news")
    else:
        return redirect("login")


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





