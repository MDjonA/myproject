from django.db import models
from django.contrib.auth.models import User


# Общий профиль пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    # Роли
    is_master = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# Категории услуг (швея, сантехник, электрик, ремонт, уборка и т.д.)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Профиль мастера
class MasterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    rating = models.FloatField(default=0)  # ← добавили рейтинг

    def __str__(self):
        return f"Мастер: {self.user.username}"


# Профиль клиента
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Клиент: {self.user.username}"
# добавь ниже существующих моделей вот этот код:
class Service(models.Model):
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.master.user.username})"

#  СОЗДАЁМ МОДЕЛЬ ЗАКАЗОВ
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принят мастером'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='orders')
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ от {self.client.user.username} → {self.master.user.username}"
    
#  Добавляем модель Message
class Message(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.sender.username} в заказе {self.order.id}"
    
#  СОЗДАЁМ МОДЕЛЬ ОТЗЫВОВ (Review).
class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.client.user.username} → {self.master.user.username}"

# СОЗДАЁМ МОДЕЛЬ ИЗБРАННОГО (Favorites)
class FavoriteMaster(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='favorite_masters')
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.username} → {self.master.user.username}"


class FavoriteService(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='favorite_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.username} → {self.service.title}"

# Добавляем фото работ мастера
class WorkPhoto(models.Model):
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='works/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Фото работы мастера {self.master.user.username}"
# Создаём модель отзыва о клиенте
class ClientReview(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв о клиенте {self.client.user.username} — {self.rating}"
