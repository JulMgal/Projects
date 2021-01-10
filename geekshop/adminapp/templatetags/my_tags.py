from django import template
from django.conf import settings

register = template.Library()


def media_folder_products(string):
    if not string:
        string = 'products_images/product-1.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_products', media_folder_products)


@register.filter(name='media_folder_products')
def media_folder_products(string):
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'



