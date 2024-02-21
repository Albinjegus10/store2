from django.contrib.auth.models import User
from django.db import models


class Productmaster(models.Model):
    product_id = models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    store_id = models.IntegerField(default=6)
    product_name = models.CharField(max_length=30)
    product_code = models.CharField(max_length=45)
    product_cat_id = models.IntegerField()
    product_subcat_id = models.IntegerField(null=True, blank=True)
    product_unit = models.IntegerField()
    net_quantity = models.CharField(max_length=15)
    product_status = models.CharField(max_length=10)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    tax_system = models.IntegerField(default=0)
    o_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    sale_tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    product_discount = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    d = models.IntegerField(default=0)
    image_1 = models.ImageField(upload_to='category/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='category/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='category/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='category/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='category/', blank=True, null=True)
    latest_product = models.IntegerField(default=0)
    top_rate_product = models.IntegerField(default=0)
    review_product = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    total_ratings = models.IntegerField(default=0)
    reviews = models.TextField(blank=True, null=True)



    def get_additional_images(self):
        return [self.image_2, self.image_3, self.image_4, self.image_5]

    def __str__(self):
        return self.product_name

    def get_reviews_list(self):
        return self.reviews.split('\n') if self.reviews else []

class Inventorymaster(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_id_inv = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    product_status_inv = models.CharField(max_length=10, default='Active')
    admin_id = models.CharField(max_length=45)
    store_id = models.IntegerField()
    a_stock = models.CharField(max_length=50, default='0')
    c_stock = models.CharField(max_length=45, default='0')
    s_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=10, default='0')
    d = models.IntegerField(default=0)

    def __str__(self):
        return f"Inventory ID: {self.inventory_id}, Productmaster: {self.product_id_inv.product_name}"


class Categorymaster(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_code = models.CharField(max_length=45)
    category_name = models.CharField(max_length=20)
    category_status = models.CharField(max_length=10)
    admin_id = models.IntegerField()
    d = models.IntegerField(default=0)
    cat_image_1 = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.category_name

class Customermaster(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    district = models.CharField(max_length=25, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=75, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    Door_no = models.CharField(max_length=10, null=True, blank=True)
    cus_type = models.CharField(max_length=20, null=True, blank=True)
    admin_id = models.IntegerField()
    d = models.IntegerField()
    status = models.CharField(max_length=10, default='Active')
    store_id = models.IntegerField()

    def __str__(self):
        return self.name if self.name else f"Customer ID: {self.customer_id}"



class Subcategorymaster(models.Model):
    subcat_id = models.AutoField(primary_key=True)
    category_id_subcat = models.ForeignKey(Categorymaster, on_delete=models.CASCADE)
    subcategory_code = models.CharField(max_length=45)
    subcategory_name = models.CharField(max_length=30)
    subcat_status = models.CharField(max_length=10)
    admin_id = models.IntegerField()
    d = models.IntegerField(default=0)

    def __str__(self):
        return self.subcategory_name

class Newfeatured(models.Model):
    featured_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    description = models.TextField(max_length=90)
    # Add other fields for your FeaturedList table

    def __str__(self):
        return f"Featured List ID: {self.featured_id} - Product: {self.product.product_name}"


class Myfeatureditems(models.Model):
    featured_id = models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    store_id = models.IntegerField(default=6)
    product = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    description = models.TextField(max_length=90)
    # Add other fields for your FeaturedList table

    def __str__(self):
        return f'Featured Item ID: {self.featured_id}, Product: {self.product}, Description: {self.description}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.username

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = 'store_ContactMessage'

class Billing(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    ship_to_different_address = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=255, choices=[
        ('paypal', 'Paypal'),
        ('gpay', 'Google Pay'),
        ('phonepe', 'PhonePe'),
        ('cash', 'Cash On Delivery'),
    ])

    class Meta:
        db_table = 'store_billing'

from django.db import models
from .models import UserProfile, Productmaster
from decimal import Decimal

class CartItemlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if the product has a related offer
        offer = offers.objects.filter(product=self.product).first()
        discount_price = offer.discountprice if offer else None
        price = Decimal(discount_price) if discount_price else Decimal(self.product.sales_price)

        # Calculate the total based on the discount price or sales price
        self.total = self.quantity * price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} - {self.product.product_name}"


from django.db import models


class offers(models.Model):
    product = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    discountprice = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_discounted_price(self):
        return self.salesprice - (self.salesprice * (self.discount_percentage / 100))

class Order_details(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Productmaster, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    ship_to_different_address = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    payment_method = models.CharField(max_length=255, choices=[
        ('paypal', 'Paypal'),
        ('gpay', 'Google Pay'),
        ('phonepe', 'PhonePe'),
        ('cash', 'Cash On Delivery'),
    ])

    class Meta:
        db_table = 'store_Order_details'
from django.db import models


class YOrder(models.Model):
    Ytitle = models.CharField(max_length=255)
    Yimage = models.ImageField(upload_to='categories/', blank=True, null=True)
    Yprice = models.DecimalField(max_digits=10, decimal_places=2)
    click_count = models.IntegerField(default=0)
    cancel_status = models.CharField(
        max_length=50,
        default='Cancel Order',
        choices=[
            ('Cancel Order','Cancel Order'),
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Canceled Successfully', 'Canceled Successfully'),
            ('On Hold', 'On Hold'),

        ]
    )

    def __str__(self):
        return self.Ytitle

    def cancel_order(self):
        self.click_count += 1
        self.save()

class Return(models.Model):
    Rtitle = models.CharField(max_length=255)
    Rimage = models.ImageField(upload_to='categories/', blank=True, null=True)
    Rprice = models.DecimalField(max_digits=10, decimal_places=2)
    click_count = models.IntegerField(default=0)
    return_status = models.CharField(
        max_length=50,
        default='Return Order',
        choices=[
            ('Return Order', 'Return Order'),
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Request Approved', 'Request Approved'),
            ('On Hold', 'On Hold'),
        ]
    )

    def __str__(self):
        return self.Rtitle

    def return_order(self):
        self.click_count += 1
        self.save()

class Blg(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=300)
    date = models.DateField(default='2024-01-01')
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    retitle = models.CharField(max_length=255,default='')
    recontent = models.CharField(max_length=300,default='')
    redate = models.DateField(default='2024-01-01')
    relink = models.URLField(blank=True, null=True,default='')
    reimage = models.ImageField(upload_to='blog/', blank=True, null=True)

    cate = models.CharField(max_length=255, default='')
    para = models.CharField(max_length=555, default='', null=True, blank=True)

    def __str__(self):
        return self.title

from django.db import models

class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    user_id = models.IntegerField()
    status = models.CharField(max_length=255, blank=True, null=True)
    products = models.CharField(max_length=255)
    cancel_status = models.CharField(
        max_length=500,
        default='Cancel Order',
        choices=[
            ('Cancel Order', 'Cancel Order'),
            ('Order Cancelled', 'Order Canceled'),
            ('Your Order Already Shipped Contact Your Delivery Partner',
             'Your Order Already Shipped Contact Your Delivery Partner'),

        ]
    )
    return_status = models.CharField(
        max_length=500,
        default='Return Order',
        choices=[
            ('Return Order', 'Return Order'),
            ('Return successfull', 'Return successfull'),
            ('Cannot Able to Return Order',
             'Cannot Able to Return Order'),

        ]
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Orderlistdetails(models.Model):
    order_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()  # Assuming you have a valid user ID field
    status = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.ForeignKey(Productmaster, on_delete=models.CASCADE)  # Remove the _id suffix

    def __str__(self):
        return f"{self.date} {self.payment_method}"

class Reason(models.Model):
    user_id = models.IntegerField(null=True)
    cancellation_reason = models.CharField(max_length=100, blank=True, null=True)
    Return_Reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.  Cancellation_Reason