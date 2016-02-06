from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register_view, name = 'register'),
    url(r'^login/$', views.login_view, name = 'login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^start/$', views.start_view, name='start'),
    url(r'^fetch-questions/$', views.fetch_questions_ajax, name = 'fetch_questions'),
    url(r'^delete/(?P<username>\w+)/$', views.delete_record_view, name='delete'),
    url(r'^answer/$', views.record_answer_view, name = 'answer'),
    url(r'^end/$', views.end_view, name='end'),
    url(r'^report/$', views.report_view, name='report'),
]