"""iMooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include, handler404, handler500
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from iMooc.settings import MEDIA_ROOT

from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, ResetPwdView, HomeView,\
    LoginOutView

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LoginOutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active'),
    url(r'^forget/$', ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^resetpwd/$', ResetPwdView.as_view(), name='resetpwd'),

    # 图片路径处理
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # 静态文件夹 static 处理
    # url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),

    # 加载 organization url路由
    url(r'^org/', include('organization.urls', namespace='org')),

    # 加载 course url路由
    url(r'^course/', include('courses.urls', namespace='course')),

    # 用户信息
    url(r'^user/', include('users.urls', namespace='user')),
    # django ueditor 配置
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]


# 配置全局404
handler404 = 'users.views.page_not_found'
# 500页面
handler500 = 'users.views.page_error'