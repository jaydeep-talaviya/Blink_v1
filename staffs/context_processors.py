from django.urls import resolve, reverse


def breadcrumbs(request):
    path_info = request.path_info
    path_items = path_info.strip('/').split('/')
    breadcrumbs = []

    # Add Home breadcrumb
    breadcrumbs.append({'name': 'Home', 'url': '/'})

    # Construct breadcrumbs based on the current URL
    current_url = ''

    for item in path_items:
        current_url += f'/{item}'
        breadcrumbs.append({'name': item.capitalize().replace("_"," "), 'url': current_url})

    return {'breadcrumbs': breadcrumbs}