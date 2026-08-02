from django.urls import path

from .views import (
    register, login_view, dashboard, 
    choose_role, master_services, add_service, 
    all_services, create_order, client_orders,
    chat, master_orders, master_profile,
    add_review, add_client_review
    )


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("choose-role/", choose_role, name="choose_role"),
    
    path("master/services/", master_services, name="master_services"),
    path("master/services/add/", add_service, name="add_service"),
    
    path("services/", all_services, name="all_services"),
    path("order/create/<int:service_id>/", create_order, name="create_order"),
    path("orders/", client_orders, name="client_orders"),
    
    path("chat/<int:order_id>/", chat, name="chat"),

    path("master/orders/", master_orders, name="master_orders"),

    path("master/<int:master_id>/", master_profile, name="master_profile"),

    path("review/add/<int:master_id>/", add_review, name="add_review"),

    path("review/client/<int:order_id>/", add_client_review, name="add_client_review"),

]



