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
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('',views.hoved,name='hoved'),
	path('info/',views.info,name='info'),
	path('opptak/',views.opptak,name='opptak'),
	path('kontakt/',views.kontakt,name='kontakt'),
	path('medlemmer/',views.medlemmer,name='medlemmer'),
	path('medlem/ny/',views.medlem_ny,name='medlem_ny'),
	path('medlem/<int:mid>/',views.medlem_info,name='medlem_info'),
	path('medlem/<int:mid>/redi',views.medlem_redi,name='medlem_redi'),
	path('medlem/<int:mid>/slett',views.medlem_slett,name='medlem_slett'),
	path('utmerkelse/<int:uid>/fjern',views.utmerkelse_fjern,name='utmerkelse_fjern'),
	path('produksjoner/',views.produksjoner,name='produksjoner'),
	path('produksjon/ny/',views.produksjon_ny,name='produksjon_ny'),
	path('produksjon/<int:pid>/',views.produksjon_info,name='produksjon_info'),
	path('produksjon/<int:pid>/redi',views.produksjon_redi,name='produksjon_redi'),
	path('produksjon/<int:pid>/slett',views.produksjon_slett,name='produksjon_slett'),
	path('forestilling/<int:fid>/fjern',views.forestilling_fjern,name='forestilling_fjern'),
	path('verv/',views.verv,name='verv'),
	path('erfaring/<int:eid>/fjern',views.erfaring_fjern,name='erfaring_fjern'),
	path('uttrykk/',views.uttrykk,name='uttrykk'),
	path('dokumenter/',views.dokumenter,name='dokumenter'),
	path('arkiv/',views.arkiv,name='arkiv'),
	path('produksjoner/',views.produksjoner,name='produksjoner'),
	path('admin/',admin.site.urls)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

