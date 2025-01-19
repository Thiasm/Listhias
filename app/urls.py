from django.urls import path
from .views import ItemList, add_note, rate_item, display_rate, add_task, complete_task, add_item, edit_item, edit_task, delete_item, CategoryList, add_category, edit_category, delete_category, search_items

urlpatterns = [
    path('', CategoryList.as_view(), name='categories'),
    
    path('add_category/', add_category, name='add_category'),
    path('<category>/edit_category/', edit_category, name='edit_category'),
    path('<category>/delete_category/', delete_category, name='delete_category'),

    # Remove Category
    # Edit Category

    path('<category>/', ItemList.as_view(), name='items'),

    # path('<category>/open_modal/<action>', open_modal, name='open_modal'),
    path('<category>/search_items/', search_items, name='search_items'),

    path('<category>/add_task/', add_task, name='add_task'),
    path('<category>/edit_task/<int:id>', edit_task, name='edit_task'),
    path('<category>/complete_task/<int:id>', complete_task, name='complete_task'),

    path('<category>/add_item/', add_item, name='add_item'),
    path('<category>/edit_item/<int:id>', edit_item, name='edit_item'),
    path('<category>/delete_item/<int:id>', delete_item, name='delete_item'),
    path('<category>/display_rate/<int:id>', display_rate, name='display_rate'),
    path('<category>/rate_item/<int:id>', rate_item, name='rate_item'),
    path('<category>/add_note/<int:id>', add_note, name='add_note'),
]
