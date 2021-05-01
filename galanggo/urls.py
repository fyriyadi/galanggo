from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from search import views as search_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from gallery import views as gallery_views
from wagtail.wagtailimages import urls as wagtailimages_urls
from wagtail.wagtailimages.views.serve import ServeView

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^register/', gallery_views.register_view),
    url(r'^login/', gallery_views.login_view),
    url(r'^login_token/', gallery_views.login_token_view),
    # url(r'^logout/', gallery_views.logout_view),
    # url(r'^profile/', gallery_views.profile_view),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),

    url(r'^api/profile/$', gallery_views.get_profile, name="profile_rest"),
    url(r'^api/profile/update/$', gallery_views.update_profile_view, name="update_profile"),
    url(r'^api/projects/$', gallery_views.get_projects, name="projects_rest"),
    url(r'^api/project/(?P<project_id>.*.)/$', gallery_views.get_project, name="get_project"),
    #url(r'^api/events/$', gallery_views.get_events, name="events_rest"),
    url(r'^api/qnas/$', gallery_views.get_qnas, name="qnas_rest"),
    url(r'^api/subscribe/$', gallery_views.subscribe, name="subscribe"),
    #url(r'^api/donations/$', gallery_views.donations_list, name="donations_list"),
    #url(r'^api/project/(?P<projectid>.*.)/$', gallery_views.get_donation, name="donation"),
    #url(r'^api/project/confirmation/(?P<projectid>.*.)/$', gallery_views.get_donation_confirmation, name="detail_donation"),
    #url(r'^api/donate/(?P<projectid>.*.)/$', gallery_views.temp_donation, name="donate"),
    url(r'^api/donate_pay/(?P<project_id>.*.)/(?P<amount>.*.)/$', gallery_views.pay_donate_view, name="donate_pay"),
    url(r'^snap_finish/$', gallery_views.snap_finish_view, name="snap_finish"),
    
    #url(r'^confirm_donation/(?P<projectid>.*.)/$', gallery_views.confirm_donation, name="confirm_donation"),
    
    url(r'^api/priority/$', gallery_views.get_priority, name="priority_project"),
    url(r'^api/statistics/$', gallery_views.get_statistics, name="statistics"),
    url(r'^api/request/$', gallery_views.request_project, name="request_project"),
    url(r'^api/projects/req/(?P<requirement>.*.)/$', gallery_views.get_reqprojects, name="project_requirement"),
    url(r'^api/volunteer/history/$', gallery_views.get_volunteer_history, name="get_volunteer_history"),
    url(r'^api/volunteer/register/(?P<project_id>.*.)/$', gallery_views.register_volunteer, name="register_volunteer"),
    url(r'^api/volunteer/status/$', gallery_views.get_volunteer_status, name="get_volunteer_status"),
    url(r'^api/donatur/history/$', gallery_views.get_donatur_history, name="get_volunteer_history"),
    url(r'^api/history/$', gallery_views.get_history, name="get_history"),

    # url(r'^api/responses/$', gallery_views.get_responseCodeList, name="get_responseCodeList"),

    url(r'', include(wagtail_urls)),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
