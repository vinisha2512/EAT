"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^signup', views.signup,name='sign-up'),
    url(r'^fileupload', views.fileupload,name='filesupload'),
    url(r'^logout', views.logout, name="logout"),
    url(r'^login', views.login,name='login'),
    url(r'^Login/', views.Login,name='Login'),
    url(r'^Signup', views.Signup,name='Signup'),
    url(r'^Filesupload', views.Filesupload,name='files'),
    url(r'^display/', views.display,name='files'),
    url(r'^semester/', views.semester,name='semester'),
    url(r'^Disp', views.Disp,name='Disp'),
    url(r'^Downloadf', views.Downloadf),
    url(r'^Filedelete', views.Filedelete),

    path('student/', views.student, name="student"),
    # path('Internship/', views.internship),
    path('Internship/', views.internship, name="internship"),
    path('Sell/', views.sell, name="sell"),

    path("products", views.retProd, name="retProd"),
    path(r"^prodDet", views.prodDet, name="prodDet"),

    url(r'^eventdisplay', views.eventdisplay, name='eventsdisplay'),
    url(r'^eventmain', views.eventmain, name='eventmain'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^prof_photo_change/', views.prof_photo_change, name='prof_photo_change'),
    url(r'^schedule', views.adminschedule, name='adminschedule'),
    url(r'^aschedule', views.aschedule, name='aschedule'),
    url(r'^sschedule', views.sschedule, name='sschedule'),
    url(r'^eventschedule', views.studentschedule, name='studentschedule'),
    path("addtocart", views.addtocart, name="addtocart"),
    path("updatecart", views.remprod, name="remprod"),
    path("cart", views.cart, name="cart"),
    path("generateInvoice", views.sendEmailAttach, name="sendEmailAttach"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path("<str:id>", views.prodDet, name="prodDet"),

]
