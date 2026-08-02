from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import (


UserProfile, Message, Order, 
Service, MasterProfile, ClientProfile, 
Review, ClientReview
)
# создаём форму регистрации
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)

        return redirect("login")

    return render(request, "register.html")
# создаём форму входа
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")
# создаём личный кабинет
def dashboard(request):
    return render(request, "dashboard.html")

# создаём обработчик выбора роли
def choose_role(request):
    if request.method == "POST":
        role = request.POST.get("role")
        profile = UserProfile.objects.get(user=request.user)

        if role == "client":
            profile.is_client = True
            profile.is_master = False
        elif role == "master":
            profile.is_master = True
            profile.is_client = False

        profile.save()

        return redirect("dashboard")

    return render(request, "choose_role.html")

# Создаём view для списка услуг мастера
def master_services(request):
    profile = MasterProfile.objects.get(user=request.user)
    services = Service.objects.filter(master=profile)
    return render(request, "master_services.html", {"services": services})

# Создаём view для добавления услуги
def add_service(request):
    profile = MasterProfile.objects.get(user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        Service.objects.create(
            master=profile,
            title=title,
            description=description,
            price=price
        )

        return redirect("master_services")

    return render(request, "add_service.html")

# Список всех услуг (для клиента)
def all_services(request):
    services = Service.objects.all()
    return render(request, "all_services.html", {"services": services})

# Страница создания заказа
def create_order(request, service_id):
    service = Service.objects.get(id=service_id)
    client = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":
        details = request.POST.get("details")

        Order.objects.create(
            client=client,
            master=service.master,
            service=service,
            details=details,
        )

        return redirect("client_orders")

    return render(request, "create_order.html", {"service": service})

# список заказов клиента
def client_orders(request):
    client = ClientProfile.objects.get(user=request.user)
    orders = Order.objects.filter(client=client)
    return render(request, "client_orders.html", {"orders": orders})

# создаём view чата клиент
def chat(request, order_id):
    order = Order.objects.get(id=order_id)
    messages = Message.objects.filter(order=order).order_by("timestamp")

    if request.method == "POST":
        text = request.POST.get("text")
        Message.objects.create(
            order=order,
            sender=request.user,
            text=text
        )
        return redirect(f"/chat/{order_id}/")

    return render(request, "chat.html", {"order": order, "messages": messages})

# создаём view чата мастер
def master_orders(request):
    master = MasterProfile.objects.get(user=request.user)
    orders = Order.objects.filter(master=master)
    return render(request, "master_orders.html", {"orders": orders})

# Создаём view профиля мастера
def master_profile(request, master_id):
    master = MasterProfile.objects.get(id=master_id)
    reviews = Review.objects.filter(master=master).order_by("-timestamp")
    services = Service.objects.filter(master=master)

    return render(request, "master_profile.html", {
        "master": master,
        "reviews": reviews,
        "services": services
    })

# View для добавления отзыва
def add_review(request, master_id):
    master = MasterProfile.objects.get(id=master_id)
    client = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":
        rating = request.POST.get("rating")
        text = request.POST.get("text")

        Review.objects.create(
            master=master,
            client=client,
            rating=rating,
            text=text
        )

        # Пересчёт рейтинга мастера
        all_reviews = Review.objects.filter(master=master)
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        master.rating = round(avg_rating, 1)  # округляем до 1 знака
        master.save()
        return redirect(f"/master/{master_id}/")

    return render(request, "add_review.html", {"master": master})

# View для добавления отзыва о клиенте
def add_client_review(request, order_id):
    order = Order.objects.get(id=order_id)
    master = MasterProfile.objects.get(user=request.user)
    client = order.client

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        text = request.POST.get("text")

        ClientReview.objects.create(
            client=client,
            master=master,
            rating=rating,
            text=text
        )

        # Пересчёт рейтинга клиента
        all_reviews = ClientReview.objects.filter(client=client)
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        client.rating = round(avg_rating, 1)
        client.save()

        return redirect("/master/orders/")

    return render(request, "add_client_review.html", {
        "order": order,
        "client": client
    })









