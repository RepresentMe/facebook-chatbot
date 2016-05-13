from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()

import chatbot.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', chatbot.views.index, name='index'),
    url(r'^webhook', chatbot.views.webhook, name='webhook'),
    url(r'^lastmessages/(?P<id>\d+)', chatbot.views.last_messages_by_id, name='lastmessages_by_id'),
    url(r'^lastmessages$', chatbot.views.last_messages, name='lastmessages'),
    url(r'^testmessage', chatbot.views.test_message, name='testmessage'),
    url(r'^admin/', include(admin.site.urls)),
]
