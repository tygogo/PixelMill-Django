from django.http import JsonResponse


def api_login_required(view):
    """登陆认证装饰器，若未登录返回状态0
    :param view:
    :return:
    """

    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            print("yes")
            return view(request, *args, **kwargs)
        else:
            print("no")
            return JsonResponse({'status': '2000asd',
                                 'text': 'NOT LOGIN'}
                                )
    return decorator


def api_post_only(view):
    """非post返回2001
    :param view:
    :return:
    """
    def decorator(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)
        else:
            return JsonResponse({'status': '2001',
                                 'text': 'POST ONLY'}
                                )
    return decorator


def api_get_only(view):
    """非get返回2002
    :param view:
    :return:
    """
    def decorator(request, *args, **kwargs):
        if request.method == 'GET':
            return view(request, *args, **kwargs)
        else:
            return JsonResponse({'status': '2002',
                                 'text': 'GET ONLY'}
                                )
    return decorator
