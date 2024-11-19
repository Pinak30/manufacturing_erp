from django.urls import path
from .views import *

urlpatterns = [
    path('production/', production, name='production'),
    path('master_production_scheduling/', masterproduction, name='masterproduction'),
    path('bom/', bommanagement, name='bommanagement'),
    path('bom/add/', bom_add, name='add_bom'),  # For adding a new BOM
    path('bom/update/<int:bom_id>/', bom_update, name='update_bom'),  # For updating an existing BO
    path('bom/view/<int:bom_id>/', viewbom, name='viewbom'),  # For viewing a specific BOM
    path('material_requirement_planning/', materialreqplan, name='materialreqplan'),
    path('material_requirement_planning/batchview/<str:plan_id>/', batchview, name='batchview'),
    path('material_requirement_planning/deleteplan/<str:plan_id>/', deleteplan, name='deleteplan'),
    path('work_order_management/', workordermanage, name='workordermanage'),
]