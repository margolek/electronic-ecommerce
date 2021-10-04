from django.template.defaulttags import register


@register.filter
def get_position_upper(d, key):
    return d[2*key]


@register.filter
def get_position_bottom(d, key):
    if len(d) % 2 != 0 and d[2*key] == d[-1]:
        return
    return d[2*key+1]


@register.filter
def put_variable(d, key):
    return d[key]

# This filter is not used (check if call query is faster than for loop)
# @register.filter
# def default_image_url(item, pk):
#     return Images.objects.filter(product_id=pk).filter(default=True).get().image.url
