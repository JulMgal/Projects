import datetime
import json
import os
import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page, never_cache

from .management.commands.fill_db import JSON_PATH
from .models import Product, ProductCategory

JSON_PATH = 'mainapp/json'


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'products_by_category_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True, category_pk=pk)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True, category_pk=pk)


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)


def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True)
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'главная'
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'продукты'
    if pk:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            #products = Product.objects.all().order_by(is_active=True, category__is_active=True).order_by('price')

        else:
            category = get_category(pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price').order_by('price')
        paginator = Paginator(products, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': get_links_menu(),
            'category': category,
            'products': product_paginator,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'same_products': same_products,
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', content)


@cache_page(3600)
def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk:
            if pk == 0:
                category = {'pk': 0, 'name': 'все'}
                # products = Product.objects.all().order_by(is_active=True, category__is_active=True).order_by('price')
                products = Product.object.filter(Q(category_id=1) | Q(category_id=2))
                print(products)
            else:
                category = get_category(pk)
                products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                    'price').order_by('price')
            paginator = Paginator(products, 2)
            try:
                product_paginator = paginator.page(page)
            except PageNotAnInteger:
                product_paginator = paginator.page(1)
            except EmptyPage:
                product_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': get_links_menu(),
                'category': category,
                'products': product_paginator,
            }

            result = render_to_string('mainapp/includes/inc_products_list_content.html', context=content)
            return JsonResponse({'result': result})


def product(request, pk):
    title = 'продукт'
    product = get_object_or_404(Product, pk=pk)
    links_menu = ProductCategory.objects.filter(is_active=True)
    content = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
    }
    return render(request, 'mainapp/product.html', content)


@never_cache
def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@geekshop.ru',
            'address': 'Близко к центру',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@geekshop.ru',
            'address': 'Близко к океану',
        },
    ]
    content = {'title': title, 'visit_date': visit_date, 'locations': locations, }
    return render(request, 'mainapp/contact.html', content)
