def is_mobile(request):
    user_agent = request.META['HTTP_USER_AGENT'].lower()

    if 'iphone' in user_agent or 'android' in user_agent:
        return True

    return False
