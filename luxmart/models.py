from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user type model
class UserType(models.Model):
    type_name = models.CharField(verbose_name="Type Name", max_length=150, unique=True, null=True, blank=True)
    is_active = models.BooleanField(blank=False, null=True)

    class Meta:
        db_table = 'tbl_usertype'
        verbose_name = 'User Type'
        verbose_name_plural = 'Users Type'

    def __str__(self) -> str:
        return self.type_name


# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    user_type = models.ForeignKey(UserType, verbose_name='User Type', on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField(upload_to='media', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)

    class Meta:
        db_table = 'tbl_customuser'

    def __str__(self) -> str:
        return self.username


# Category model for product categorization
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_category'

    def __str__(self) -> str:
        return self.name


# Product model for e-commerce products
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_product'

    def __str__(self) -> str:
        return self.name


# Cart item model for shopping cart items
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


# Order model for customer orders
class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='OrderDetail', related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        ordering = ('-created',)


# Order detail model for order-specific product details
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value set

    class Meta:
        db_table = 'tbl_orderdetail'
        unique_together = ('order', 'product', 'cart_item')


# Model for user sign-up (if needed separately)
class SignUp(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
