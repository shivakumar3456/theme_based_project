from django.shortcuts import render
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        print(username)
        emailid = request.POST.get("email")
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        user = None
        try:
            user = User.objects.get(email=emailid)
            try:
                participant = User.objects.get(user=user)
                return HttpResponse('User already exists please try logging in')
            except:
                pass
        except:
            user = User.objects.create_user(username=emailid, email=emailid, password=password,first_name=username)
        print(user)
        user.save()
        profile = Profile(user=user, phone_number=mobile_number, qr_code= emailid[:-10])
        profile.save()
        login(request, user)
        return redirect(reverse("dashboard"))


#login Page
def registration(request):
    return render(request,"acumenapp/registration.html")





def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

def login_view(request):
    if request.method == 'POST':
        # user = User.objects.create_user(**request.POST)
        #print(request.POST['email'],request.POST.get('password'))
        mail=request.POST.get('email')
        pw=request.POST.get('loginpassword')
        user = authenticate(username=mail, password=pw)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return render(request,"acumenapp/registration.html",{"loggedin" :False})


# Create your views here.
