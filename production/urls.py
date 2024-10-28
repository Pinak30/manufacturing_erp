from django.urls import path
from .views import *

urlpatterns = [
    path('production/', production, name='production'),
    path('master_production_scheduling/', masterproduction, name='masterproduction'),
    path('bom_management/', bommanagement, name='bommanagement'),
    path('material_requirement_planning/', materialreqplan, name='materialreqplan'),
    path('work_order_management/', workordermanage, name='workordermanage'),
]