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
    url(r'^lastmessage', chatbot.views.last_messages, name='lastmessages'),
    url(r'^admin/', include(admin.site.urls)),
]
