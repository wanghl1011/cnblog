from django.conf.urls import url, include
from django.contrib import admin
from blog import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^pc-geetest/ajax_validate', views.pcajax_validate, name='pcajax_validate'),
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^index/', views.index),
    # url(r'^personal/',views.persional),
    url(r'^logout/', views.logout),
    url(r'^login_confirm/', views.login_confirm),
    url(r'^get_check_img/', views.get_check_img),
    url(r'^reg_check/', views.reg_check),
    url(r'^set_pwd/(?P<username>\w+)/$', views.set_pwd),

    # 博客首页网站分类查询
    url(r'^select/(?P<catename>\w+)/', views.select_catewebsite),

    # 点赞和取消
    url(r'^updown', views.up_down_ajax),
    # url(r'^(?P<username>\w+)/(?P<select_name>up|down)/(?P<keyword>\d+)/',views.up_down),

    # 文章评论
    url(r'^comment', views.comment),

    # 构建评论树
    url(r'^get/comment/tree/(?P<article_id>\d+)$', views.get_comment_tree),

    # 删除文章评论
    # url(r'^del/comment',views.del_comment),


    # 个人后台首页
    url(r'^manage/(?P<username>\w+)', views.manage),

    # 个人后台上传图片
    url(r'^upload_img', views.upload_img),

    #个人后台删除文章
    url(r'^del/article/(?P<keyword>\d+)',views.del_article),

    #个人后台编辑文章
    url(r'^edit/article/(?P<keyword>\d+)',views.edit_article),

    # 个人后台添加文章
    url(r'^(?P<username>\w+)/add/article', views.add_article),





    # 个人站点首页
    url(r'^(?P<username>\w+)/$', views.home_site),

    # 个人站点分类标签日期查询
    url(r'^(?P<username>\w+)/(?P<select_name>tag|cate|date)/(?P<keyword>.+)/', views.home_site),

    # 文章具体内容
    url(r'^(?P<username>\w+)/p/(?P<keyword>\d+)/', views.home_site_article),

]
