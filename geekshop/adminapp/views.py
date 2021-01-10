from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.models import ShopUser
from authapp.views import ShopUserRegisterForm
from mainapp.models import ProductCategory, Product


#    @user_passes_test(lambda u: u.is_superuser)
#    def users(request):
#    title = 'админка/пользователи'
#    user_list = ShopUser.objects.all()
#    content = {
#        'title': title,
#        'objects': user_list,
#    }
#    return render(request, 'adminapp/users.html', content)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def user_create(request):
#        title = 'пользователи/создание'
#
#        if request.method == 'POST':
#            user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#            if user_form.is_valid():
#                user_form.save()
#                return HttpResponseRedirect(reverse('admin:users'))
#        else:
#            user_form = ShopUserRegisterForm()
#
#        content = {'title': title, 'update_form': user_form}
#        return render(request, 'adminapp/user_update.html', content)


class UsersCreateView(CreateView):
    model = ShopUserRegisterForm
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin: users')
    #    fields = '__all__'
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователь/создание'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def users_update(request, pk):
#        title = 'пользователи/редактирование'
#        edit_user = get_object_or_404(ShopUser, pk=pk)
#        if request.method == 'POST':
#            edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#            if edit_form.is_valid():
#                edit_form.save()
#                return HttpResponseRedirect(reverse('admin:users'))
#            else:
#                edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#            content = {'title': title, 'update_form': edit_form}
#            return render(request, 'adminapp/user_update.html', content)


class UsersUpdateView(UpdateView):
    model = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin: users')
    #    fields = '__all__'
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/обновление'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def users_delete(request, pk):
#        title = 'пользователи/удаление'
#        user_item = get_object_or_404(ShopUser, pk=pk)
#        if request.method == 'POST':
#            if user_item.is_active:
#                user_item.is_active = False
#            else:
#                user_item.is_active = True
#            user_item.save()
#            return HttpResponseRedirect(reverse('admin:users'))
#
#        content = {'title': title, 'user_to_delete': user_item}
#        return render(request, 'adminapp/user_delete.html', content)


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin: users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def categories(request):
#        title = 'админка/категории'
#        categories_list = ProductCategory.objects.all()
#        content = {
#            'title': title,
#            'objects': categories_list,
#        }
#        return render(request, 'adminapp/categories.html', content)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def category_create(request):
#       title = 'категории/создание'
#       if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#
#          if category_form.is_valid():
#              category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin: categories')
    #    fields = '__all__'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/создание'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def category_update(request, pk):
# title = 'категории/редактирование'
# edit_category = get_object_or_404(ProductCategory, pk=pk)
#
# if request.method == 'POST':
#   category_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#
#   if category_form.is_valid():
#       category_form.save()
#       return HttpResponseRedirect(reverse('admin:categories'))
# else:
#   category_form = ProductCategoryEditForm(instance=edit_category)
#
# content = {'title': title, 'update_form': category_form}
# return render(request, 'adminapp/category_update.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    #    fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/обновление'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount}% к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


#    @user_passes_test(lambda u: u.is_superuser)
#     def category_delete(request, pk):
#         title = 'категории/удаление'
#        category_item = get_object_or_404(ProductCategory, pk=pk)
#         if request.method == 'POST':
#            if category_item.is_active:
#                category_item.is_active = False
#            else:
#               category_item.is_active = True
#           category_item.save()
#            return HttpResponseRedirect(reverse('admin:categories'))
#
#         content = {'title': title, 'category_to_delete': category_item}
#        return render(request, 'adminapp/category_delete.html', content)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/удаление'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def products(request, pk):
#        title = 'админка/продукты'
#        category_item = get_object_or_404(ProductCategory, pk=pk)
#        products_list = Product.objects.filter(category=category_item)
#        content = {
#            'title': title,
#            'objects': products_list,
#            'category': category_item,
#        }
#        return render(request, 'adminapp/products.html', content)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты'
        return context


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)

#    @user_passes_test(lambda u: u.is_superuser)
#    def product_create(request):
#        title = 'продукты/создание'
#
#        if request.method == 'POST':
#            product_form = ProductEditForm(request.POST, request.FILES)
#
#            if product_form.is_valid():
#                product_form.save()
#                return HttpResponseRedirect(reverse('admin:products'))
#        else:
#            product_form = ProductEditForm()
#
#        content = {'title': title, 'update_form': product_form}
#        return render(request, 'adminapp/product_create.html', content)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin: products')
    #    fields = '__all__'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def product_read(request, pk):
#        title = 'продукт/чтение'
#        product_item = get_object_or_404(Product, pk=pk)
#        content = {'title': title, 'object': product_item}
#        return render(request, 'adminapp/product_read.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/чтение'
        return context


#    @user_passes_test(lambda u: u.is_superuser)
#    def product_update(request, pk):
#        title = 'продукт/редактирование'
#        edit_product = get_object_or_404(Product, pk=pk)
#
#        if request.method == 'POST':
#            edit_form = ProductEditForm(request.POST, instance=edit_product)
#
#            if edit_form.is_valid():
#                edit_form.save()
#                return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
#        else:
#            edit_form = ProductEditForm(instance=edit_product)
#
#        content = {'title': title, 'update_form': edit_form, 'category': edit_product.category}
#        return render(request, 'adminapp/product_update.html', content)


class ProductUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


#    @user_passes_test(lambda u: u.is_superuser)
#    def product_delete(request, pk):
#        title = 'продукт/удаление'
#        product = get_object_or_404(Product, pk=pk)
#        if request.method == 'POST':
#            product.is_active = False
#            product.save()
#            return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
#
#        content = {'title': title, 'product_to_delete': product}
#        return render(request, 'adminapp/product_delete.html', content)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin: products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        return context


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)
