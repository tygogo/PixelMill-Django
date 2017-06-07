from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .decorators import api_post_only, api_get_only, api_login_required
from django.contrib.auth.models import User
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Paint, Comment, UserProfile, RelationShip, Message
from django.db.models import Count


from django.db.models.signals import post_save
from django.dispatch import receiver

# from rest_framework import viewsets
# from .serializers import PaintSerializer
# Create your views here.


# 登陆相关
@csrf_exempt
@api_get_only
def api_logout(request):
    print("api_logout")
    logout(request)
    return JsonResponse({'status': '1'})


@csrf_exempt
# @api_post_only
def api_login(request):
    # 0 用户名和密码错误
    # 1 登陆成功
    # 2 未填写
    r_dict = {}
    username = request.POST['username']
    password = request.POST['password']
    if (username is not None and
            password is not None):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            sessionid = request.session.session_key
            r_dict['sessionid'] = sessionid
            r_dict['status'] = 1
            r_dict['text'] = '登陆成功'
        else:
            r_dict['text'] = '用户名或密码错误'
            r_dict['status'] = 0
    else:
        r_dict['text'] = '未填写'
        r_dict['status'] = 2
    return JsonResponse(r_dict)


@csrf_exempt
@api_post_only
def api_regist(request):
    # 0 已存在
    # 1 注册成功
    # 2 未填写
    r_dict = {}
    username = request.POST['username']
    password = request.POST['password']
    if (username is not None and
            password is not None):
        user = User.objects.filter(username=username).first()
        # 已存在
        if user is not None:
            r_dict['text'] = '用户名已存在'
            r_dict['status'] = 0
        else:
            user = User.objects.create_user(username, None, password)
            user.profile = UserProfile()
            user.profile.save()
            user.save()
            r_dict['text'] = '注册成功'
            r_dict['status'] = 1
    else:
        r_dict['text'] = '未填写'
        r_dict['status'] = 2
    return JsonResponse(r_dict)


# 功能相关
@csrf_exempt
@api_post_only
@api_login_required
def api_post_paint(request):
    r_dict = {}
    image = request.FILES['image']
    describe = request.POST['describe']
    if image is not None and describe is not None:
        # TODO 效验DATA
        paint = Paint(image=image, describe=describe, author=request.user)
        paint.save()
        r_dict['text'] = 'SUCCESS'
        r_dict['status'] = 1
    else:
        r_dict['text'] = 'FAIL'
        r_dict['status'] = 0
    return JsonResponse(r_dict)


@csrf_exempt
@api_post_only
@api_login_required
def api_change_avatar(request):
    r_dict = {}
    image = request.FILES['image']
    user = request.user
    if image is not None:
        # TODO 效验DATA
        user.profile.avatar = image
        user.profile.save()
        r_dict['text'] = 'SUCCESS'
        r_dict['status'] = 1
    else:
        r_dict['text'] = 'FAIL'
        r_dict['status'] = 0
    return JsonResponse(r_dict)



@csrf_exempt
@api_post_only
@api_login_required
def api_delete_paint(request):
    r_dict = {}
    data = request.POST['data']
    describe = request.POST['describe']
    if data is not None and describe is not None:
        # TODO 效验DATA
        paint = Paint(data=data, describe=describe, author=request.user)
        paint.save()
        r_dict['text'] = 'SUCCESS'
        r_dict['status'] = 1
    else:
        r_dict['text'] = 'FAIL'
        r_dict['status'] = 0
    return JsonResponse(r_dict)


@csrf_exempt
@api_post_only
@api_login_required
def api_comment(request):
    r_dict = {}
    paint_id = request.POST['paint_id']
    to_user_id = request.POST['to_user_id']
    text = request.POST['text']
    paint = Paint.objects.filter(pk=paint_id).first()

    to_user = User.objects.filter(pk=to_user_id).first()
    if paint is None:
        r_dict['text'] = 'PAINT NOT EXIST'
        r_dict['status'] = 0
    else:
        comment = Comment(text=text, paint=paint,
                          from_user=request.user,
                          to_user=to_user)
        comment.save()
        r_dict['text'] = 'SUCCESS'
        r_dict['status'] = 1
    return JsonResponse(r_dict)


@csrf_exempt
@api_post_only
@api_login_required
def api_delete_paint(request):
    r_dict = {}
    paint_id = request.POST['paint_id']
    paint = Paint.objects.filter(pk=paint_id).first()
    if paint is not None:
        if paint.author.pk == request.user.pk:
            paint.delete()
            r_dict['text'] = 'SUCCESS'
            r_dict['status'] = 1
    else:
        r_dict['text'] = 'FAIL'
        r_dict['status'] = 0
    return JsonResponse(r_dict)


# user1 是否关注 user2
def is_follow(user1, user2):
    rs = RelationShip.objects.filter(from_rs=user1, to_rs=user2).first()
    if rs is not None:
        return True
    else:
        return False


# 关注相关
@csrf_exempt
@api_post_only
@api_login_required
def api_follow(request):
    r_dict = {}

    user_id = request.POST['user_id']
    t = User.objects.filter(pk=user_id).first()
    if t is not None:
        f = request.user
        rs = RelationShip.objects.filter(from_rs=f, to_rs=t).all().first()

        if rs is None:
            r = RelationShip()
            r.from_rs = f
            r.to_rs = t
            r.save()
            r_dict['status'] = 1
            r_dict['text'] = 'SUCCESS'
            # 通知有人关注你...
            add_message(paint=None, from_user=f, to_user=t, comment=None, message_type=4)

        else:  # 已经关注
            r_dict['status'] = 0
            r_dict['text'] = 'EXIST'
    else:
        r_dict['status'] = 0
        r_dict['text'] = 'USER NOT EXIST'

    return JsonResponse(r_dict)


@csrf_exempt
@api_post_only
@api_login_required
def api_unfollow(request):
    r_dict = {}

    user_id = request.POST['user_id']
    t = User.objects.filter(pk=user_id).first()
    if t is not None:
        f = request.user
        r = RelationShip.objects.filter(from_rs=f, to_rs=t)
        if r is not None:
            r.delete()
            r_dict['status'] = 1
            r_dict['text'] = 'SUCCESS'
        else:  # 没有关注
            r_dict['status'] = 0
            r_dict['text'] = 'RELATIONSHIP NOT EXIST'
    else:
        r_dict['status'] = 0
        r_dict['text'] = 'USER NOT EXIST'

    return JsonResponse(r_dict)


# 所有收到的信息
@csrf_exempt
@api_get_only
@api_login_required
def api_msgreceive(request):
    msgs = request.user.send_to_me.all()
    # TODO


# 所有发出的信息
@csrf_exempt
@api_get_only
@api_login_required
def api_msgsend(request):
    msgs = request.user.send_by_me.all()
    # TODO


@csrf_exempt
@api_get_only
def api_getComment(request):
    paint_id = request.GET['id']
    paint = Paint.objects.filter(pk=paint_id).first()
    comments = Comment.objects.filter(paint=paint)

    paginator = Paginator(comments, 10)

    page = request.GET['page']

    follow = 0
    if is_follow(request.user, paint.author):
        follow = 1

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    a = []
    for comment in comments:
        from_user_avatar = " "
        if comment.from_user.profile.avatar:
            from_user_avatar = comment.from_user.profile.avatar.url
        else:
            from_user_avatar = " "

        dd = {
            "comment_id": comment.pk,
            "from_user": comment.from_user.username,
            "to_user": comment.to_user.username,
            "from_user_id": comment.from_user.pk,
            "to_user_id": comment.to_user.pk,
            "text": comment.text,
            "from_user_avatar": from_user_avatar
        }
        a.append(dd)

    return JsonResponse({'comments': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages,
                         "followed": follow
                         }
                        )


# 返回paint 的dict 数组
def get_paints_jsonarray(paints, user):
    a = []
    for paint in paints:
        u = paint.liker.filter(pk=user.pk).first()

        like = 0
        if u is not None:
            like = 1

        follow = 0
        if is_follow(user, paint.author):
            follow = 1

        dd = {
            "image": paint.image.url,
            "describe": paint.describe,
            "id": paint.pk,
            "author": paint.author.username,
            "author_id": paint.author.pk,
            "like": like,
            "like_count": paint.liker.all().count(),
            "follow": follow
        }
        a.append(dd)
    return a


# 最新的作品
@csrf_exempt
@api_login_required
@api_get_only
def api_timeLine(request):
    paints = Paint.objects.all()

    paginator = Paginator(paints, 20)

    page = request.GET['page']

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    a = get_paints_jsonarray(paints, request.user)

    return JsonResponse({'paints': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages
                         }
                        )


# 关注人的作品
@csrf_exempt
@api_login_required
@api_get_only
def api_followsTimeLine(request):
    paints = Paint.objects.filter(author__follower__from_rs=request.user)

    paginator = Paginator(paints, 20)

    page = request.GET['page']

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    a = get_paints_jsonarray(paints, request.user)
    return JsonResponse({'paints': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages
                         }
                        )


# 我的作品
@csrf_exempt
@api_login_required
@api_get_only
def api_mywork(request):
    user = request.user
    paints = Paint.objects.filter(author=user)

    paginator = Paginator(paints, 20)

    page = request.GET['page']

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    a = get_paints_jsonarray(paints, request.user)

    return JsonResponse({'paints': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages
                         }
                        )


# 我喜欢的作品
@csrf_exempt
@api_login_required
@api_get_only
def api_likestimeline(request):
    user = request.user
    paints = Paint.objects.filter(liker__pk=user.pk)

    paginator = Paginator(paints, 20)

    page = request.GET['page']

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    a = get_paints_jsonarray(paints, request.user)

    return JsonResponse({'paints': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages
                         }
                        )


# 热门作品
@csrf_exempt
@api_login_required
@api_get_only
def api_hottimeline(request):
    user = request.user
    # 喜欢人数最多的排前面啊
    paints = Paint.objects.annotate(num_liker=Count('liker'))\
        .order_by('-num_liker', '-pub_date')

    paginator = Paginator(paints, 20)

    page = request.GET['page']

    try:
        paints = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    a = get_paints_jsonarray(paints, request.user)

    return JsonResponse({'paints': a,
                         'current_page': page,
                         'num_pages': paginator.num_pages
                         }
                        )


# 点赞
@csrf_exempt
@api_post_only
@api_login_required
def api_like(request):
    r_dict = {}

    paint_id = request.POST['paint_id']
    p = Paint.objects.filter(pk=paint_id).first()
    if p is not None:
        user = request.user
        user.likes.add(p)
        user.save()
        r_dict['status'] = 1
        r_dict['text'] = 'SUCCESS'
        r_dict['new_count'] = p.liker.count()

        #通知有人喜欢你...
        add_message(paint=p, from_user=user, to_user=p.author, comment=None, message_type=3)
    else:
        r_dict['status'] = 0
        r_dict['text'] = 'PAINT NOT EXIST'

    return JsonResponse(r_dict)

@csrf_exempt
@api_post_only
@api_login_required
def api_dislike(request):
    r_dict = {}

    paint_id = request.POST['paint_id']
    p = Paint.objects.filter(pk=paint_id).first()
    if p is not None:
        user = request.user
        user.likes.remove(p)
        user.save()
        r_dict['status'] = 1
        r_dict['text'] = 'SUCCESS',
        r_dict['new_count'] = p.liker.count()
    else:
        r_dict['status'] = 0
        r_dict['text'] = 'PAINT NOT EXIST'

    return JsonResponse(r_dict)


@csrf_exempt
@api_get_only
@api_login_required
def api_myinfo(request):
    r_dict = {}
    print(1)
    user = request.user
    print(2)

    r_dict["pid"] = user.pk
    print(3)

    r_dict["username"] = user.username
    print(4)

    if user.profile.avatar:
        r_dict["avatar"] = user.profile.avatar.url
        print(5)

    else:
        r_dict["avatar"] = ""
        print(6)

    r_dict["profile"] = user.profile.profile
    print(7)

    r_dict["followCount"] = user.follow.count()
    print(8)

    r_dict["followerCount"] = user.follower.count()
    print(9)

    return JsonResponse(r_dict)


@csrf_exempt
@api_get_only
@api_login_required
def api_get_messages(request):
    r_dict = {}
    user = request.user
    messages = Message.objects.filter(send_to=user).all()

    a = []
    for message in messages:
        dd = {
            "from_user": message.send_by.username,
            "from_user_id": message.send_by_id,
            "type": message.type,
            "paint_id": message.paint.pk
        }

        if message.comment:
            dd['text'] = message.comment.text

        a.append(dd)

    r_dict = {
        "status": 1,
        "messages": a,
        "count": len(a)
    }
    return JsonResponse(r_dict)


# type:
def add_message(paint, from_user, to_user, message_type, comment):

    msg = Message(send_to=to_user, send_by=from_user, type=message_type, paint=paint)
    if comment:
        msg.comment = comment
    msg.save()




# @receiver(post_save, sender=Comment, dispatch_uid="comment_saved_signal")
def comment_saved_signal(sender, instance, created, **kwargs):
    #更新的评论不提醒
    if not created:
        return

    add_message(paint=instance.paint,
                from_user=instance.from_user,
                to_user=instance.to_user,
                message_type=0,
                comment=instance)

post_save.connect(comment_saved_signal,sender=Comment)


