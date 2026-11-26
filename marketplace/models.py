from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def average_rating(self):
        reviews = self.user.reviews_received.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0

class Review(models.Model):
    reviewee = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='reviews_given', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} Stars for {self.reviewee.username}"

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Food', '🍱 Food'),
        ('Utensils', '🍳 Utensils'),
        ('Furniture', '🛋️ Furniture'),
        ('Toys', '🧸 Toys'),
        ('Books', '📚 Books'),
        ('Tools', '🛠️ Tools'),
        ('Pet Supplies', '🐱 Pet Supplies'),
        ('Other', '✨ Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    expiry_date = models.DateField(null=True, blank=True, help_text="Optional: When does this expire or need to be picked up by?")
    status = models.CharField(max_length=20, default='Available') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category}"

class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name="conversations", on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buyer_conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.buyer.username} & {self.item.owner.username} about {self.item.title}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False) # <-- NEW: Tracks unread status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username}"