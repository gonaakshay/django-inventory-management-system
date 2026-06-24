from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('products/',views.product_list,name='product_list'),

    path('create/',views.product_create,name='product_create'),

    path('update/<int:id>/',views.product_update,name='product_update'),

    path('delete/<int:id>/',views.product_delete,name='product_delete'),

    path('deleted-products/', views.deleted_products,name='deleted_products'),

    path('restore/<int:id>/',views.restore_product,name='restore_product'),

    path('export-excel/',views.export_products_excel,name='export_products_excel'),

    path('login/',views.user_login,name='login'),

    path('logout/',views.user_logout,name='logout'),

]