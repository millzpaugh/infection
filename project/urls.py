from django.conf.urls import patterns, include, url
from django.contrib import admin
from infection import urls as infection_urls


urlpatterns = patterns('',
    # Examples:
    url(r'', include(infection_urls)),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
