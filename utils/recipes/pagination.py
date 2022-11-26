import math

from django.core.paginator import Paginator


def make_pagination_range(page_range: list, qty_pages: int, current_page: int) -> dict:
    middle_range: int = math.ceil(qty_pages / 2)
    start_range: int = current_page - middle_range
    stop_range: int = current_page + middle_range
    total_pages: int = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination: list = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, queryset, per_page: int, qty_pages: int = 4) -> tuple:
    try:
        current_page: int = int(request.GET.get('page', 1))
    except:
        current_page: int = 1

    # Criando a paginação, passando o QUERYSER (recipes) e o numero de itens que será exibido por páginas
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)
    print(paginator.page_range)
    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return (page_obj, pagination_range,)
