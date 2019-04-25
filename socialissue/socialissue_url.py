from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('upload/',views.upload,name="upload"),
    path('upload_data/',views.upload_data ,name="upload_data"),
    path('logout/',views.logout_view ,name="logout"),
    path('login_view/',views.login_view,name="login_view"),
    path(r'newsdata/<int:name>/',views.newsdata,name="newsdata"),
    path('newsfeed/',views.newsfeed,name="newsfeed"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('all_news/',views.newsfeed,name="all_news"),
    path('news_content/',views.newscontent ,name="news_content"),
    path('comment/',views.comment,name='comment'),
    path(r'upvote/<int:postid>/<slug:voted>/',views.vote,name="vote"),
    path('accept/<int:postid>/',views.accept,name="accept"),
    path('reject/<int:postid>/',views.reject,name="reject"),
    path('viewfile/<int:postid>',views.viewfile,name="viewfile"),
    path('posted/<int:postid>/',views.posted,name="posted"),
    path('solved/<int:postid>/',views.solved,name="solved")


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)