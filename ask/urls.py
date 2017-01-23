from django.conf.urls import url
from django.conf.urls.static import static

from hw import settings
from . import views

urlpatterns = [
    url(r'^$', views.empty, name='empty'),
    url(r'^ask$', views.ask, name='ask'),
    url(r'^(?P<sort>\w\w\w)$', views.index, name='index'),
    url(r'^tag/(?P<tag>\w+)/(?P<sort>\w\w\w)$', views.tag, name='tag'),
    url(r'^question/(?P<id>\d+)$', views.QuestionView.as_view(), name='question'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^rate$', views.rate, name='rate'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
