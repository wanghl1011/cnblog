from django.contrib import admin
from blog.models import *
# 111
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Article)
admin.site.register(ArticleDetail)
admin.site.register(Cate)
admin.site.register(Tag)
admin.site.register(Article_Tag)
admin.site.register(Articlepoll)
admin.site.register(Comment)
admin.site.register(CateWebsite)
admin.site.register(CateWebsiteDetail)
