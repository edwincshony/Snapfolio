from django.urls import path
from . import views

urlpatterns = [
    path('create-portfolio/', views.create_portfolio, name='create_portfolio'),
    path('edit-portfolio/', views.edit_portfolio, name='edit_portfolio'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('respond-to-feedback/<int:feedback_id>/', views.respond_to_feedback, name='respond_to_feedback'),
    path('edit-image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
]
