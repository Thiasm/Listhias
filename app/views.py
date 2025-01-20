from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from .models import Item, Category
from django.db.models.functions import Lower
from .utils import Utils, ApiRequest
from django.http import JsonResponse
from django.urls import reverse

class CategoryList(ListView):
    model = Category
    template_name = 'app/pages/categories/category_page.html'
    context_object_name = 'categories'
    ordering = ['-created']

    def filter_queryset(self, queryset):
        search = self.request.GET.get("research")
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            return render(request, "app/pages/categories/category_list.html", context)
        return render(request, self.template_name, context)
    
@require_http_methods(['GET', 'POST'])
def add_category(request):
    if request.method == 'GET':
        return render(request, 'app/modals/add_category_modal.html', { 'category_types': Category.CategoryTypes })
    
    if request.method == 'POST':
        category_type = request.POST.get('category_type')
        category_title = request.POST.get('category_title')
        if Category.objects.filter(title = category_title).exists():
            # Update target to error badge
            return_view = render(request, 'app/error/error_badge.html', { 'error_message': 'Category already exists.' })
            return_view['HX-Retarget'] = '#error-content'
            return return_view
        Category.objects.create(title = category_title, type = category_type)
        categories = Category.objects.order_by('-created')
        result = render(request, 'app/pages/categories/category_list.html', { 'categories': categories })
        result['HX-Trigger'] = "closeModal"
        return result
    return JsonResponse({"error": "Invalid request."}, status=400)

@require_http_methods(['GET', 'POST'])
def edit_category(request, category):
    category = get_object_or_404(Category, title = category)
    if request.method == 'GET':
        return render(request, 'app/modals/edit_category_modal.html', { 'category': category })

    if request.method == 'POST':
        category_title = request.POST.get('category_title')
        if Category.objects.filter(title = category_title).exists():
            return render(request, 'app/error/error_badge.html', { 'error_message': 'Category already exists.' })
        category.title = category_title
        category.save()
        # Reload page with updated category
        return JsonResponse({"success": True}, headers={"HX-Redirect": reverse("items", args=[category])})
    return JsonResponse({"error": "Invalid request."}, status=400)

@require_http_methods(['DELETE'])
def delete_category(request, category):
    category = get_object_or_404(Category, title = category)
    category.delete()
    # Reload page in category list
    return JsonResponse({"success": True}, headers={"HX-Redirect": reverse("categories")})

class ItemList(ListView):
    model = Item
    template_name = 'app/pages/template_page.html'
    context_object_name = 'items'

    def filter_queryset(self, queryset):
        category = get_object_or_404(Category, title=self.kwargs.get("category"))
        if category:
            queryset = queryset.filter(category=category)

        search = self.request.GET.get("research")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = self.request.GET.get("ordering")
        if ordering:
            if ordering == 'title' or ordering == '-title':
                ordering = 'lower_title'
                queryset = queryset.annotate(lower_title=Lower('title'))
            queryset = queryset.order_by(ordering)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, title=self.kwargs.get("category"))
        context["category"] = category
        context["item_type"] = Utils.get_item_type(category.type)

        # FOR WHAT ?
        context["order"] = self.request.GET.get("ordering", "")
        context["search_query"] = self.request.GET.get("research", "")
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            item_type = context['item_type']
            return render(request, f"app/pages/{item_type}s/{item_type}_list.html", context)
        return render(request, self.template_name, context)

@require_http_methods(['GET'])
def search_items(request, category):
    category = get_object_or_404(Category, title=category)
    query = request.GET.get('item_title')
    if not query:
        return render(request, 'app/modals/modal.html', { 'category': category })
    results = ApiRequest.get_api_search(query, category)
    return render(request, 'app/partials/search_results.html', { 'results': results, 'category': category })

def add_note(request, category, id):
    category = get_object_or_404(Category, title=category)
    item = get_object_or_404(Item, id=id)
    return render(request, 'app/modals/add_note_modal.html', { 'category': category, 'item': item })

@require_http_methods(['GET'])
def display_rate(request, id, category):
    item = get_object_or_404(Item, id=id)
    checkbox_checked = request.GET.get("item_complete")
    return render(request, "app/modals/edit_item_modal.html" , {
            'category': category,
            'item': item,
            'checkbox_checked': checkbox_checked, 
            'stars_range': range(1, 6)
        })

@require_http_methods(['POST'])
def rate_item(request, id, category):
    item = get_object_or_404(Item, id=id)
    rating = request.POST.get('rating')
    item.user_grade = int(rating)
    item.save()
    return render(request, "app/partials/rate_item.html" , {
        'stars_range': range(1, 6),
        'category': category,
        'item': item
    })

@require_http_methods(['POST'])
def add_task(request, category):
    category = get_object_or_404(Category, title=category)
    item_title = request.POST.get('task_title')
    Item.objects.create(title = item_title, category=category)
    items = Item.objects.filter(category=category)
    return render(request, 'app/pages/tasks/task_list.html', {'items': items, 'category': category})

@require_http_methods(['POST'])
def complete_task(request, id, category):
    category = get_object_or_404(Category, title=category)
    item = get_object_or_404(Item, id=id)
    item.complete = not item.complete
    item.save()
    items = Item.objects.filter(category=category)
    return render(request, 'app/pages/tasks/task_list.html', {'items': items, 'category': category})

@require_http_methods(['GET', 'POST'])
def add_item(request, category):
    category = get_object_or_404(Category, title=category)
    item_type = Utils.get_item_type(category.type)
    
    if request.method == 'GET':
        return render(request, f'app/modals/add_{item_type}_modal.html', {'category': category})

    if request.method == 'POST':
        item_id = request.POST.get('result_id')
        if not item_id:
            return JsonResponse({"error": "Item ID not provided."}, status=400)

        if Item.objects.filter(category=category, api_id=item_id).exists():
            response = render(request, 'app/error/error_badge.html', { 'error_message': 'Item already exists.' })
            response['HX-Retarget'] = "#error-content"
            return response
            
        item_data = Utils.fetch_and_prepare_item_data(item_id, category)
        if not item_data:
            return JsonResponse({"error": "Failed to fetch item data."}, status=400)
        Item.objects.create(**item_data)
        items = Item.objects.filter(category=category)
        response = render(request, 'app/pages/items/item_list.html', {'items': items, 'category': category })
        response['HX-Trigger'] = "closeModal"
        return response

@require_http_methods(['DELETE'])
def delete_item(request, id, category):
    category = get_object_or_404(Category, title=category)
    item_type = Utils.get_item_type(category.type)
    item = get_object_or_404(Item, id = id)
    item.delete()
    items = Item.objects.filter(category=category)
    return render(request, f'app/pages/{item_type}s/{item_type}_list.html', {'items': items, 'category': category})

@require_http_methods(['GET', 'POST'])
def edit_item(request, id, category):
    category = get_object_or_404(Category, title=category)
    item = get_object_or_404(Item, id = id)
    if request.method == 'GET':
        return render(request, 'app/modals/edit_item_modal.html', {
            'item': item,
            'category': category, 
            'checkbox_checked': item.complete, 
            'stars_range': range(1, 6)
        })
    if request.method == 'POST':
        item.complete = 'item_complete' in request.POST
        if not item.complete and (item.user_grade or item.user_note):
            item.user_grade = None
            item.user_note = ""
        elif item.complete:
            item.user_note = request.POST.get('item_note')
        item.save()
        return render(request, 'app/pages/items/item.html', {'item': item, 'category': category})

@require_http_methods(['GET', 'POST'])
def edit_task(request, id, category):
    category = get_object_or_404(Category, title=category)
    item = get_object_or_404(Item, id = id)
    if request.method == 'GET':
        return render(request, 'app/modals/edit_task_modal.html', {'item': item, 'category': category})
    if request.method == 'POST':
        item.title = request.POST.get('task_title')
        item.description = request.POST.get('task_description')
        item.complete = 'task_complete' in request.POST
        item.save()
        return render(request, 'app/pages/tasks/task.html', {'item': item, 'category': category})

def custom_page_not_found_view(request, exception):
    response = render(request, 'app/404.html', {})
    response.status_code = 404
    return response