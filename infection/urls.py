from django.conf.urls import patterns, url
from views import *
from django.conf.urls.static import static
from project import settings

urlpatterns = patterns(
    '',
    url(r'^full_infection/$', FullInfectionView.as_view(), name="full_infection"),
    url(r'^limited_infection/$', LimitedInfection.as_view(), name="limited_infection"),
    url(r'^', HomeView.as_view(), name="home"),
)