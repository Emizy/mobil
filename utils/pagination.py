from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


def paginate(obj, length, page):
    paginator = Paginator(obj, length)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(page)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return obj_list
