"""smedialink_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from partymaker.views import AuthView, OrderView, DeleteOrderView, OrderListView

urlpatterns = [
    url(r'^$', login_required(OrderView.as_view()), name='order'),
    url(r'^delete/$', login_required(DeleteOrderView.as_view()), name='delete'),
    url(r'^list/$', login_required(OrderListView.as_view()), name='list'),
    url(r'^auth/$', AuthView.as_view(), name='auth'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]
