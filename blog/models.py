from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
class UserInfo(AbstractUser):
     """
     用户信息表
     实现登录和注册
     和个人站点是一对一的关系
     和推荐反对是一对多的关系
     和评论是一对多的关系
     """
     #用户名
     # username=models.CharField(max_length=50)
     # 密码
     # password=models.CharField(max_length=100)
     # 邮箱
     # email=models.EmailField(max_length=20)
     nid = models.AutoField(primary_key=True)
     #注册时间
     reg_time=models.DateField(verbose_name='创建时间', auto_now_add=True)
     #头像
     avatar = models.FileField(upload_to='user_head_picture/', default="user_head_picture/default.png")
     #电话
     telephone = models.CharField(max_length=11, null=True, unique=True)
     #昵称
     nickname = models.CharField(verbose_name='昵称', max_length=32)

     #和个人站点是一对一的关系
     user_blog=models.OneToOneField(to='Blog', to_field='nid',null=True,on_delete=None)

     def __str__(self):
         return self.username
class Blog(models.Model):
    """
    个人站点表
    和文章是一对多的关系
    和用户是一对一的关系
    和分类是一对多的关系
    和标签是一对多的关系
    """
    nid = models.AutoField(primary_key=True)
    #站点名称
    title = models.CharField(verbose_name = '个人博客标题', max_length = 64)
    #后缀
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    #博客主题
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    #站点的形式
    style=models.CharField(max_length=50)
    def __str__(self):
        return self.title
class Article(models.Model):
    """
    文章表
    和个人站点是一对多的关系
    和用户是一对多的关系
    和分类是一对多的关系
    和标签是多对多的关系
    和推荐与反对是一对多的关系
    和评论是一对多的关系
    """
    nid = models.AutoField(primary_key=True)
    # 文章标题
    title=models.CharField(max_length=50, verbose_name='文章标题')
    # 文章创建时间
    create_time=models.DateTimeField(verbose_name='创建时间')
    # 文章摘要
    article_desc=models.CharField(max_length=255, verbose_name='文章描述')
    # 评论数
    comment_count = models.IntegerField(default=0)
    # 推荐数
    up_count = models.IntegerField(default=0)
    # 反对数
    down_count = models.IntegerField(default=0)

    # 和用户是一对多的关系，用户是一，文章是多
    article_user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid',on_delete=None)
    # 和分类是一对多的关系，分类是一，文章是多
    article_cate = models.ForeignKey(to='Cate', to_field='nid', null=True,on_delete=None)
    # 和标签是多对多的关系
    article_tags = models.ManyToManyField(
        to="Tag",
        through='Article_Tag',
        through_fields=('article', 'tag'),
    )
    # 和网站具体分类表是一对多的关系，具体分类是一，文章是多
    catewebsitedetail=models.ForeignKey(verbose_name='网站分类', to='CateWebsiteDetail', to_field='id',on_delete=None,null=True)
    # 和个人站点是一对多的关系，个人站点是一，文章是多,这一个老师的model没有写
    # article_blog=models.ForeignKey("Blog",on_delete=None)

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()

    article = models.OneToOneField(to='Article', to_field='nid',on_delete=None)



class Cate(models.Model):
    """
    分类表
    和个人站点是一对多的关系
    和文章是一对多的关系
    """
    nid = models.AutoField(primary_key=True)
    # 分类名称
    cate_name=models.CharField(verbose_name='分类标题', max_length=32)
    # 对分类的描述
    cate_desc=models.CharField(max_length=50)

    # 和个人站点是一对多的关系，站点是一，分类是多
    cate_blog=models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=None)
    def __str__(self):
        return self.cate_name

class Tag(models.Model):
    """
    标签表
    和个人站点是一对多的关系
    和文章是多对多的关系
    """
    nid = models.AutoField(primary_key=True)
    # 标签名称
    tag_name=models.CharField(verbose_name='标签名称', max_length=32)
    # 标签描述
    tag_desc=models.CharField(max_length=50)

    # 和个人站点是一对多的关系，标签是多，个人站点是一
    tag_blog=models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=None)
    def __str__(self):
        return self.tag_name

class Article_Tag(models.Model):
    """
    文章和标签的关系表
    和文章是一对多的关系
    和标签是一对多的关系
    """
    nid = models.AutoField(primary_key=True)
    # 和文章是一对多的关系，文章是一
    article=models.ForeignKey(verbose_name='文章', to="Article", to_field='nid',on_delete=None)
    # 和标签是一对多的关系，标签是一
    tag=models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid',on_delete=None)
    #联合唯一
    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class Articlepoll(models.Model):
    """
    文章推荐和反对表
    和用户是一对多的关系
    和文章是一对多的关系
    """
    nid = models.AutoField(primary_key=True)
    # 是推荐还是反对,true代表推荐，false代表反对
    is_agree=models.BooleanField(default=True)

    # 和用户是一对多的关系，用户是一
    user=models.ForeignKey("UserInfo",null=True,on_delete=None)
    # 和文章是一对多的关系，文章是一
    article=models.ForeignKey("Article",null=True,on_delete=None)
    #联合唯一
    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Comment(models.Model):
    """
    评论表
    和用户是一对多的关系
    和文章是一对多的关系
    并且和自身做关联
    """
    nid = models.AutoField(primary_key=True)
    # 评论时间
    create_time=models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 评论内容
    content=models.CharField(verbose_name='评论内容', max_length=255)

    # 和用户是一对多的关系
    user=models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid',on_delete=None)
    # 和文章是一对多的关系
    article=models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid',on_delete=None)
    # 属于哪条评论的评论，是文章的评论默认为None，和评论表做自关联
    parent_comment=models.ForeignKey('self', null=True,on_delete=None)


class CateWebsite(models.Model):
    """
    网站分类表
    和网站具体的分类是一对一的关系
    """
    name=models.CharField(verbose_name='分类名称', max_length=50)
    def __str__(self):
        return self.name
class CateWebsiteDetail(models.Model):
    """
    网站具体分类表
    和网站分类表是一对一的关系
    和文章表是一对多的关系
    """
    name=models.CharField(verbose_name='分类名称',max_length=50)
    #和文章分类表是一对一的关系
    catewebsite=models.ForeignKey("CateWebsite",on_delete=None)
    def __str__(self):
        return self.name