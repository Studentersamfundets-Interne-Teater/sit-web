"""SITnett URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('',views.view_hoved,name='hoved'),
    path('info/',views.view_info,name='info'),
    path('opptak/',views.view_opptak,name='opptak'),
    path('kontakt/',views.view_kontakt,name='kontakt'),
    path('medlemmer/',views.view_medlemmer,name='medlemmer'),
    path('medlem/ny/',views.view_medlem_ny,name='medlem_ny'),
    path('medlem/<int:mid>/',views.view_medlem_info,name='medlem_info'),
    path('medlem/<int:mid>/endre/',views.view_medlem_endre,name='medlem_endre'),
    path('medlem/<int:mid>/slett/',views.view_medlem_slett,name='medlem_slett'),
    path('utmerkelse/<int:uid>/fjern/',views.view_utmerkelse_fjern,name='utmerkelse_fjern'),
    path('produksjoner/',views.view_produksjoner,name='produksjoner'),
    path('produksjon/ny/',views.view_produksjon_ny,name='produksjon_ny'),
    path('produksjon/<int:pid>/',views.view_produksjon_info,name='produksjon_info'),
    path('produksjon/<int:pid>/endre/',views.view_produksjon_endre,name='produksjon_endre'),
    path('produksjon/<int:pid>/slett/',views.view_produksjon_slett,name='produksjon_slett'),
    path('forestilling/<int:fid>/fjern/',views.view_forestilling_fjern,name='forestilling_fjern'),
    path('anmeldelse/<int:aid>/fjern/',views.view_anmeldelse_fjern,name='anmeldelse_fjern'),
    path('verv/',views.view_verv,name='verv'),
    path('verv/ny/',views.view_verv_ny,name='verv_ny'),
    path('verv/<int:vid>/',views.view_verv_info,name='verv_info'),
    path('verv/<int:vid>/endre/',views.view_verv_endre,name='verv_endre'),
    path('verv/<int:vid>/slett/',views.view_verv_slett,name='verv_slett'),
    path('erfaring/<int:eid>/fjern/',views.view_erfaring_fjern,name='erfaring_fjern'),
    path('uttrykk/',views.view_uttrykk,name='uttrykk'),
    path('arkiv/',views.view_arkiv,name='arkiv'),
    path('dokumenter/',views.view_dokumenter,name='dokumenter'),
    path('ar/<int:arstall>/',views.view_ar_info,name='ar_info'),
    path('ar/<int:arstall>/endre/',views.view_ar_endre,name='ar_endre'),
    path('ar/<int:arstall>/nyttkull/',views.view_ar_nyttkull,name='ar_nyttkull'),
    path('konto/',include('django.contrib.auth.urls')),
    path('admin/',admin.site.urls)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)