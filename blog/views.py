import random
from io import BytesIO
import json
import os
import datetime
from PIL import Image, ImageFont, ImageDraw
from django.contrib import auth
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from blog.forms import *
from blog.models import *
from django.db.models import Count
from django.db import transaction
from django.db.models import F, Q
from version2 import settings
from bs4 import BeautifulSoup
# Create your views here.
def index(request):
    article_list=Article.objects.all()
    catewebsite_list=CateWebsite.objects.all()

    return render(request, 'first_page.html',{"article_list":article_list,"catewebsite_list":catewebsite_list})

def logout(request):
    auth.logout(request)
    return redirect('/blog/index/')

def login_confirm(request):
    """
    带验证码图片的
    :param request:
    :return:
    """
    if request.is_ajax():
        username=request.POST.get("username")
        password=request.POST.get("password")
        check_code=request.POST.get("check_code")
        # if check_code.upper()==request.session["check_str"].upper():
        user=auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            ret={"sta":1,"msg":"success","name":username}
            return JsonResponse(ret)
        else:
            ret={"sta":0,"msg":"username or password error"}
            return JsonResponse(ret)
        # else:
        #     ret={"sta":0,"msg":"check_code error"}
        #     return JsonResponse(ret)
    else:
        return render(request,'login_confirm.html')

def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def get_random_char():
    num=str(random.randint(0,9))
    char_upper = chr(random.randint(65, 90))
    char_lower = chr(random.randint(97, 122))
    return random.choice([num,char_lower,char_upper])

def get_check_img(request):
    img=Image.new(
        mode="RGB",
        size=(260,40),
        color=get_random_color()
    )

    draw=ImageDraw.Draw(
        img,
        mode="RGB"
    )
    font=ImageFont.truetype("blog/static/kumo.ttf",30)
    check_str=""
    for i in range(1,6):
        random_char=get_random_char()
        check_str+=random_char
        draw.text(
            (40*i,2*random.randint(1,5)),
            random_char,
            font=font,
            fill=get_random_color()
        )
    # for i in range(100):
    #     draw.point(
    #         (random.randint(0,260),random.randint(1,40)),
    #         fill=get_random_color()
    #     )
    # for i in range(1,9):
    #     draw.line(
    #         (random.randint(1,260),random.randint(1,40),random.randint(1,260),random.randint(1,40),),
    #         fill=get_random_color()
    #     )
    f = BytesIO()
    img.save(f, "png")
    data=f.getvalue()
    request.session["check_str"]=check_str
    return HttpResponse(data)

def reg_check(request):
    if request.is_ajax():
        reg_form_bind = Regform(request.POST)
        reg_form_bind.whl = request.session["check_str"]
        print(reg_form_bind.whl)
        if reg_form_bind.is_valid():
            username = reg_form_bind.cleaned_data.get("username")
            password = reg_form_bind.cleaned_data.get("password")
            email = reg_form_bind.cleaned_data.get("email")
            # telphone=reg_form_bind.cleaned_data.get("telphone")
            file=request.FILES.get("file")
            if file:
                UserInfo.objects.create_user(username=username, password=password, email=email,avatar=file)
            else:
                UserInfo.objects.create_user(username=username, password=password, email=email)
            ret = {"sta": 1, "msg": "successful"}
            # print("++++++++++++++++++++++")
            return JsonResponse(ret)
        else:
            error=reg_form_bind.errors
            ret={"sta":0,"msg":error}
            # print("===========================")
            # print(error)
            return JsonResponse(ret)
    else:
        reg_form = Regform()
        return render(request, 'reg_check.html', locals())

def set_pwd(request,username):
    if request.method=='POST':
        # print(1111111111111)
        # set_form_bind = Regform(request.POST)
        username = request.POST.get("username")
        oldpwd = request.POST.get("oldpwd")
        newpwd = request.POST.get("newpwd")
        repeatpwd = request.POST.get("repeatpwd")
        # print(username,oldpwd)
        # reg_form_bind = Regform(request,request.POST)
        # if set_form_bind.is_valid():
        #     print("=====================")
        #     newpwd = set_form_bind.cleaned_data.get("password")
        #     repeatpwd = set_form_bind.cleaned_data.get("repassword")
            # user=auth.authenticate(username=username,password=oldpwd)
            # print(username,oldpwd,newpwd,repeatpwd)
        user=auth.authenticate(username=username,password=oldpwd)
        if user:
            if newpwd==repeatpwd:
                user.set_password(newpwd)
                user.save()
                return redirect("/blog/login_confirm/")
            else:
                errors_msg_repeatpwd='密码输入不一致'
                return render(request,'setpwd.html',locals())
        else:
            errors_msg_oldpwd='原密码输入不正确'
            return render(request,'setpwd.html',locals())
            # else:
                # errors_msg="原密码输入错误"
                # return render(request,'setpwd.html',{"username":username,"errors_msg":errors_msg,"setform":set_form_bind})
        # else:
            # print("++++++++++++++++++++++++++")
            # errors = set_form_bind.errors
            # print(errors)
            # if set_form_bind.errors.get("__all__"):
            #     print(3333333333333)
            #     errors_all=set_form_bind.errors.get("__all__")[0]
            #     return render(request,'setpwd.html',{"setform":set_form_bind,"errors":errors,"errors_all":errors_all})
            # return render(request, 'setpwd.html', {"setform":set_form_bind,"errors":errors})
    else:
        print(2222222222222222)
        username=username
        # setform = Regform(request)
        return render(request,'setpwd.html',locals())

def select_catewebsite(request,catename):
    article_list=CateWebsiteDetail.objects.filter(name=catename).first().article_set.all()
    catewebsite_list = CateWebsite.objects.all()

    return render(request,'first_page.html',locals())

def home_site(request,username,**kwargs):

    #当前点击的用户对象
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,'error.html')
    #当前用户的个人站点对象
    blog=user.user_blog

    # 当前个人站点的标签
    tag_list = blog.tag_set.all()
    # 当前个人站点的分类
    cate_list = blog.cate_set.all()
    # 当前个人站点的文章日期分类和文章个数
    date_list1 = user.article_set.all()
    date_list2 = date_list1.extra(select={"date_cate": "strftime('%%Y&%%m',create_time)"}).values("date_cate", "title")
    date_list = date_list2.values("date_cate").annotate(c=Count("nid")).values("date_cate", "c")
    for item in date_list:
        a=item.get("date_cate")
        new_date_cate=a.replace("&","年")+"日"
        item["new_date_cate"]=new_date_cate

    #当前用户对象的文章列表
    if not kwargs:
        article_list=user.article_set.all()
    else:
    #查询文章
        if kwargs.get("select_name")=="cate":
            cate_id=kwargs.get("keyword")
            cate=Cate.objects.filter(nid=cate_id).first()
            article_list=cate.article_set.all()
        elif kwargs.get("select_name")=="tag":
            tag_id=kwargs.get("keyword")
            tag=Tag.objects.filter(nid=tag_id).first()
            article_list=tag.article_set.all()
        elif kwargs.get("select_name")=="date":
            date_time = kwargs.get("keyword")
            date=date_time.split("&")
            # print(date)
            article_list=user.article_set.filter(create_time__year=date[0],create_time__month=date[1])
        elif kwargs.get("select_name")=="p":
            article_id=kwargs.get("keyword")
            # print(type(article_id))
            article=UserInfo.objects.get(username=username).article_set.filter(nid=article_id).first()
            page_title = article.title
            return render(request,'personal_article.html',{"page_title":page_title,"user":user,"blog":blog,"article":article,"tag_list":tag_list,"cate_list":cate_list,"date_list":date_list})
    page_title = username + "--" + "博客园"
    return render(request,'personal_index.html',{"page_title":page_title,"user":user,"blog":blog,"article_list":article_list,"tag_list":tag_list,"cate_list":cate_list,"date_list":date_list})

def home_site_article(request,username,keyword):
    # 当前点击的用户对象
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,'error.html')
    # 当前用户的个人站点对象
    blog = user.user_blog

    # 当前个人站点的标签
    tag_list = blog.tag_set.all()
    # 当前个人站点的分类
    cate_list = blog.cate_set.all()
    # 当前个人站点的文章日期分类和文章个数
    date_list1 = user.article_set.all()
    date_list2 = date_list1.extra(select={"date_cate": "strftime('%%Y/%%m',create_time)"}).values("date_cate", "title")
    date_list = date_list2.values("date_cate").annotate(c=Count("nid")).values("date_cate", "c")
    for item in date_list:
        a = item.get("date_cate")
        new_date_cate = a.replace("/", "年") + "日"
        item["new_date_cate"] = new_date_cate
    article_id = keyword


    # print(type(article_id))
    article = UserInfo.objects.get(username=username).article_set.filter(nid=article_id).first()
    # 当前文章的评论
    comment_list=article.comment_set.all()
    page_title = article.title
    return render(request, 'personal_article.html',{"page_title":page_title,"user": user,"comment_list":comment_list, "blog": blog,"article": article, "tag_list": tag_list, "cate_list": cate_list,"date_list": date_list})

def up_down(request,username,select_name,keyword):
    # if request.user.nid:


        # 被评价的用户
        user_back=UserInfo.objects.filter(article__nid=keyword).first()

        # 被评价用户的个人站点对象
        blog = user_back.user_blog

        # 被评价用户个人站点的标签
        tag_list = blog.tag_set.all()
        # 被评价用户个人站点的分类
        cate_list = blog.cate_set.all()
        # 被评价用户个人站点的文章日期分类和文章个数
        date_list1 = user_back.article_set.all()
        date_list2 = date_list1.extra(select={"date_cate": "strftime('%%Y-%%m',create_time)"}).values("date_cate","title")
        date_list = date_list2.values("date_cate").annotate(c=Count("nid")).values("date_cate", "c")
        for item in date_list:
            a = item.get("date_cate")
            new_date_cate = a.replace("-", "年") + "日"
            item["new_date_cate"] = new_date_cate
        print(user_back,blog,tag_list,date_list,cate_list)



        # 评价的用户
        user = UserInfo.objects.get(username=username)
        print(user)
        #被评价的文章
        article=Article.objects.get(nid=keyword)
        page_title=article.title
        sta=Articlepoll.objects.filter(user=user,article=article).exists()
        #没有记录
        if not sta:
            if select_name=='up':
                Articlepoll.objects.create(user=user,article=article,is_agree='True')
                article_up_count=article.up_count+1
                Article.objects.filter(nid=keyword).update(up_count=article_up_count)
                article1 = Article.objects.get(nid=keyword)
                return render(request, 'personal_article.html',{"page_title": page_title,"user":user_back,"blog":blog,"article":article1,"tag_list":tag_list,"cate_list":cate_list,"date_list":date_list})
            elif select_name=='down':
                Articlepoll.objects.create(user=user, article=article, is_agree='False')
                article_down_count=article.down_count+1
                Article.objects.filter(nid=keyword).update(down_count=article_down_count)
                article1 = Article.objects.get(nid=keyword)
                return render(request, 'personal_article.html',{"page_title": page_title,"user": user_back, "blog": blog, "article": article1, "tag_list": tag_list,"cate_list": cate_list, "date_list": date_list})
        #有记录
        else:
            obj=Articlepoll.objects.filter(user=user,article=article).first()
            if obj.is_agree==True:
                error_msg='您已经推荐过'
                return render(request, 'personal_article.html',{"page_title": page_title,"error_msg":error_msg,"user": user_back, "blog": blog, "article": article, "tag_list": tag_list,"cate_list": cate_list, "date_list": date_list})
            elif obj.is_agree==False:
                error_msg='您已经反对过'
                return render(request, 'personal_article.html',{"page_title": page_title,"error_msg":error_msg,"user": user_back, "blog": blog, "article": article, "tag_list": tag_list,"cate_list": cate_list, "date_list": date_list})
    # else:
    #     return redirect('/blog/login_confirm/')

def up_down_ajax(request):
    # if request.user.nid:
        if request.is_ajax():
            article_id=request.POST.get("article_id")
            is_up=request.POST.get("is_up")
            print(article_id,is_up)
            obj=Articlepoll.objects.filter(user_id=request.user.nid,article_id=article_id).first()
            ret = {"sta": 0, "msg": None,is_up:None}
            #有记录
            if obj:
                if obj.is_agree==True:
                    ret["msg"]="您已经推荐过"
                    ret["is_up"] = "up"
                    return JsonResponse(ret)
                else:
                    ret["msg"]="您已经反对过"
                    ret["is_up"] = "down"
                    return JsonResponse(ret)
            #无记录
            else:
                with transaction.atomic():
                    if is_up=='up':
                        Articlepoll.objects.create(user_id=request.user.nid,article_id=article_id)
                        Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)
                        ret["sta"]=1
                        ret["is_up"]="up"
                        return JsonResponse(ret)
                    elif is_up=='down':
                        Articlepoll.objects.create(user_id=request.user.nid, article_id=article_id,is_agree=False)
                        Article.objects.filter(nid=article_id).update(down_count=F("down_count") + 1)
                        ret["sta"] = 1
                        ret["is_up"] = "down"
                        return JsonResponse(ret)
    # else:
    #     ret={"sta":0,"msg":"请先登录"}
    #     return JsonResponse(ret)

def comment(request):
        print("+++++++++++++++++++++")
    # if request.user.nid:
        article_id = request.POST.get("article_id")
        content=request.POST.get("content")
        parent_comment_id = request.POST.get("parent_comment_id")
        ret = {}
        # 根评论
        if not parent_comment_id:
            with transaction.atomic():
                print(content)
                Comment.objects.create(parent_comment_id=None,article_id=article_id,content=content,user_id=request.user.nid)
                Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")+1)
                obj=Comment.objects.filter(article_id=article_id,content=content,user_id=request.user.nid).extra(select={"ctime":"strftime('%%Y-%%m-%%d %%H:%%M',create_time)"}).first()
                ret={"sta":1,"nid":obj.nid,"rusername":obj.user.username,"ctime":obj.ctime,"com_content":obj.content}
        # 子评论
        else:
            with transaction.atomic():
                info=content.split("\n")
                print(info)
                obj=Comment.objects.create(parent_comment_id=parent_comment_id,article_id=article_id,content=info[1],user_id=request.user.nid)
                Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")+1)
                ctime=obj.create_time.strftime("%Y-%m-%d %H:%M")
                ret={"sta":1,"parent_comment_user":obj.parent_comment.user.username,"parent_comment_content":obj.parent_comment.content,"nid":obj.nid,"rusername":obj.user.username,"ctime":ctime,"com_content":obj.content}
        return JsonResponse(ret)
    # else:
    #     ret={"sta":0,"msg":"请先登录"}
    #     return JsonResponse(ret)

def get_comment_tree(request,article_id):
    comment_list1=Comment.objects.filter(article__nid=article_id).extra(select={"ctime":"strftime('%%Y-%%m-%%d %%H:%%M',create_time)"})
    # print(comment_list1)
    comment_list=comment_list1.values("nid","content","parent_comment_id","ctime","user")
    for comment in comment_list:
        comment["user"]=Comment.objects.get(nid=comment.get("nid")).user.username
        comment["avatar"]=Comment.objects.get(nid=comment.get("nid")).user.avatar.url
    comment_tree = []
    comment_dict = {}
    for item in comment_list:
        item["child_list"] = []
        comment_dict[item.get("nid")] = item
    for key, comment in comment_dict.items():
        pid = comment.get("parent_comment_id")
        if pid:
            comment_dict.get(pid).get("child_list").append(comment)
        else:
            comment_tree.append(comment)
    print(comment_tree)
    return JsonResponse(comment_tree,safe=False)

def manage(request,username):
    # print(request.path)
    # if request.user.nid:
        user=UserInfo.objects.get(username=username)
        blog=user.user_blog
        cate_list=blog.cate_set.all()
        article_list=user.article_set.all().extra(select={"ctime":"strftime('%%Y-%%m-%%d %%H:%%M',create_time)"})
        return render(request,'manage_index.html',locals())
    # else:
    #     response='/blog/login_confirm?next='+request.path
    #     return redirect(response)

def add_article(request,username):
    if request.method=='POST':
        print(request.POST)
        title=request.POST.get("article_title")
        content=request.POST.get("content")
        article_cate_id=request.POST.get("article_cate")
        article_webcate_id=request.POST.get("article_website")
        article_tags=request.POST.getlist("tag")
        soup=BeautifulSoup(content,'html.parser')
        desc=soup.get_text()[0:200]
        desc=desc.replace(" ","")
        tag_list=["script","style","link"]
        for tag in soup.find_all():
            if tag.name in tag_list:
                tag.decompose()
        with transaction.atomic():
            user=UserInfo.objects.get(username=username)
            article=Article.objects.create(
                title=title,
                create_time=datetime.datetime.now(),
                article_desc=desc,
                article_user=user,
                article_cate_id=article_cate_id,
                catewebsitedetail_id=article_webcate_id,
            )

            ArticleDetail.objects.create(content=content,article=article)
            for i in article_tags:
                Article_Tag.objects.create(article_id=article.nid,tag_id=i)
        response='/blog/manage/'+request.user.username
        return redirect(response)
    else:
        user = UserInfo.objects.get(username=username)
        blog = user.user_blog
        cate_list = blog.cate_set.all()
        webcate_list=CateWebsite.objects.all()
        tag_list=blog.tag_set.all()
        return render(request,'manage_add_article.html',locals())

def upload_img(request):
    img_obj=request.FILES.get("article_img")
    path=os.path.join(settings.MEDIA_ROOT,"upload_img",img_obj.name)
    with open(path,'wb') as doc:
        for line in img_obj:
            doc.write(line)
    ret={
        'error':0,
        "url":"/media/upload_img/"+img_obj.name
    }
    return JsonResponse(ret)

def del_article(request,keyword):
    user=request.user
    blog = user.user_blog
    cate_list = blog.cate_set.all()
    print(Article.objects.filter(nid=keyword))
    print(ArticleDetail.objects.filter(article__nid=keyword))
    with transaction.atomic():
        ArticleDetail.objects.filter(article__nid=keyword).delete()
        Article.objects.get(nid=keyword).article_tags.clear()
        Article.objects.filter(nid=keyword).delete()
    article_list = user.article_set.all().extra(select={"ctime": "strftime('%%Y-%%m-%%d %%H:%%M',create_time)"})
    return render(request, 'manage_index.html', locals())

def edit_article(request,keyword):
    if request.method=='POST':
        print(request.POST)
        title = request.POST.get("article_title")
        content = request.POST.get("content")
        article_cate_id = request.POST.get("article_cate")
        article_webcate_id = request.POST.get("article_website")
        article_tags = request.POST.getlist("tag")
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        desc = soup.get_text()[0:200]
        desc = desc.replace(" ", "")
        tag_list = ["script", "style", "link"]
        for tag in soup.find_all():
            if tag.name in tag_list:
                tag.decompose()
        with transaction.atomic():
            user = request.user
            article=Article.objects.filter(nid=keyword).first()
            Article.objects.filter(nid=keyword).update(
                title=title,
                create_time=datetime.datetime.now(),
                article_desc=desc,
                article_user=user,
                article_cate_id=article_cate_id,
                catewebsitedetail_id=article_webcate_id,
            )
            ArticleDetail.objects.filter(article_id=keyword).update(content=content)
            article.article_tags.clear()
            # article.article_tags.add(*article_tags)
            for i in article_tags:
                Article_Tag.objects.create(article_id=article.nid, tag_id=i)
        response = '/blog/manage/' + request.user.username
        return redirect(response)
    else:
        article = Article.objects.get(nid=keyword)
        blog = request.user.user_blog
        cate_list = blog.cate_set.all()
        webcate_list = CateWebsite.objects.all()
        tag_list = blog.tag_set.all()

        article_tags=Article_Tag.objects.filter(article_id=keyword)
        tags_id=[]
        for item in article_tags:
            tags_id.append(item.tag.nid)

        return render(request, 'manage_edit_article.html', locals())



# def del_comment(request):
#     if request.user.nid:
#         if request.is_ajax():
#             print(111)
#             article_id=request.POST.get("article_id")
#             comment_id=request.POST.get("comment_id")
#             print(article_id,comment_id)
#             with transaction.atomic():
#                 obj=Comment.objects.filter(nid=comment_id)
#                 print(obj)
#                 obj.delete()
#                 Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")-1)
#                 ret={"sta":1,"msg":None}
#                 return JsonResponse(ret)
#     else:
#         ret={"sta":0,"msg":"请先登录"}
#         return JsonResponse(ret)












from blog.geetest import GeetestLib
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"
def pcajax_validate(request):
    if request.method == "POST":
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')  #FN_CHALLENGE = "geetest_challenge"
        validate = request.POST.get(gt.FN_VALIDATE, '')   # FN_VALIDATE = "geetest_validate"
        seccode = request.POST.get(gt.FN_SECCODE, '')    #FN_SECCODE = "geetest_seccode"
        status = request.session[gt.GT_STATUS_SESSION_KEY]   #GT_STATUS_SESSION_KEY = "gt_server_status"
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        ret={"sta":None,"msg":None}
        username = request.POST.get("username")
        password = request.POST.get("password")
        if result:
            check_code = request.POST.get("check_code")
            # if check_code.upper()==request.session["check_str"].upper():
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                ret = {"sta": 1, "msg": "success", "name": username}
                return JsonResponse(ret)
            else:
                ret = {"sta": 0, "msg": "username or password error"}
        else:
            ret={"sta": 0, "msg": "valid error"}
        return HttpResponse(json.dumps(ret))
    return HttpResponse("error")

def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)
