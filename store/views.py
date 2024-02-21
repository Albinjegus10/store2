from django.contrib.auth import logout
from . import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from decimal import Decimal  # Add this import
from django.views import View
from .models import Productmaster, offers,YOrder
from django.utils import timezone
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import SignupForm,PriceFilterForm
from .models import Categorymaster, Myfeatureditems
from .models import Blg

def hello(request):

    products = Productmaster.objects.all()
    categories = Categorymaster.objects.all()
    featured = Myfeatureditems.objects.all()
    try:
        # Assuming you have an 'id' field for ordering
        latest_offers = offers.objects.all().order_by('-id')[:5]  # Fetching the latest 5 offers, adjust as needed
        product_details_list = []
        for offer in latest_offers:
            product_details = {
                'productid': offer.product.product_id,
                'salesprice': offer.product.sales_price,
                'image': offer.product.image_1.url,  # Assuming 'image_1' is an ImageField
                'imagename': offer.product.product_name,
                'discountprice': offer.discountprice,
                'discount_percentage': offer.discount_percentage,
            }
            product_details_list.append(product_details)
    except offers.DoesNotExist:
        product_details_list = None
    # Filter products based on criteria
    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)
    # Create a dictionary to pass to the template
    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,
        'featured': featured,
        'product_details_list': product_details_list,
    }
    return render(request, 'index.html', context)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def Shop(request, *args, **kwargs):
    form = PriceFilterForm(request.GET)

    if form.is_valid():
        min_amount = form.cleaned_data.get('minamount')
        max_amount = form.cleaned_data.get('maxamount')

        try:
            # Validate that min_amount is less than or equal to max_amount
            if min_amount is not None and max_amount is not None and min_amount > max_amount:
                raise ValidationError('Min amount must be less than or equal to max amount.')

            # Filtering products based on the price range
            if min_amount is not None and max_amount is not None:
                products = Productmaster.objects.filter(sales_price__range=(min_amount, max_amount))
            else:
                products = Productmaster.objects.all()
        except (ValueError, InvalidOperation, ValidationError):
            return HttpResponseBadRequest("Invalid input for minamount or maxamount")
    else:
        # If form is not valid or no filtering criteria, display all products
        products = Productmaster.objects.all()

    # Pagination
    paginator = Paginator(products, 15)  # Show 15 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page.

    top_three_products = Productmaster.objects.order_by('-product_discount')[:6]
    categories = Categorymaster.objects.all()
    featured = Myfeatureditems.objects.all()
    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)

    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,
        'featured': featured,
        'product_list': top_three_products,
        'form': form,  # Add the form to context to render it in the template
    }

    return render(request, "shop.html", context=context)
def Shop_low(request):
    products = Productmaster.objects.all().order_by("sales_price")
    top_three_products = Productmaster.objects.order_by('-product_discount')[:6]

    categories = Categorymaster.objects.all()
    featured = Myfeatureditems.objects.all()

    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)
    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,
        'featured': featured,
        'product_list': top_three_products,

    }
    print("low")
    return render(request, "filter.html", context=context)



def Shop_top(request):
    products = Productmaster.objects.all().order_by("-sales_price")
    top_three_products = Productmaster.objects.order_by('-product_discount')[:6]

    categories = Categorymaster.objects.all()
    featured = Myfeatureditems.objects.all()

    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)
    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,
        'featured': featured,
        'product_list': top_three_products,

    }
    print("top")
    return render(request, "filter.html", context=context)



def is_customer(user):
    return user.groups.filter(name='UserProfile').exists()

def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('shop')



class Login(View):
    def get(self, request):
        return render(request, 'customerlogin.html')
  # Import the Category model

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.name = form.cleaned_data['name']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.image = form.cleaned_data['image']
            profile.address = form.cleaned_data['address']
            profile.save()

            return redirect('login')  # Replace with your success page name
    else:
        form = SignupForm()

    # Fetch categories
    categories = Categorymaster.objects.all() # Or you can apply filters or sorting as needed

    return render(request, 'signup.html', {'form': form, 'categories': categories})

def search_view(request):
    query = request.GET.get('query', '')
    category_id = Categorymaster.objects.filter(category_name__icontains=query).values('category_id').first()
    if category_id:
        category_id = category_id['category_id']

    else:
        category_id = None
    products = Productmaster.objects.filter(
        Q(product_name__icontains=query) | Q(product_cat_id=category_id)
    )
    categories = Categorymaster.objects.all()
    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)
    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,

    }
    return render(request,'search.html',context)


def search_cat_view(request, category_id):
    products = Productmaster.objects.filter(product_cat_id=category_id)
    categories = Categorymaster.objects.all()
    top_rated_products = Productmaster.objects.filter(top_rate_product=1)
    latest_products = Productmaster.objects.filter(latest_product=1)
    reviewed_products = Productmaster.objects.filter(review_product=1)

    context = {
        'products': products,
        'categories': categories,
        'top_rated_products': top_rated_products,
        'latest_products': latest_products,
        'reviewed_products': reviewed_products,

    }

    return render(request,'search_cat.html',context)


from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                return redirect('home')  # Replace with the desired dashboard or home page name
            else:
                # Invalid login
                form.add_error(None, 'Invalid login credentials')
    else:
        form = LoginForm()

    categories = Categorymaster.objects.all()  # Retrieve all categories
    context = {
        'form': form,
        'categories': categories,  # Include the categories in the context dictionary
    }

    return render(request, 'login.html', context)
def logout_view(request):
    # Use the built-in logout function
    logout(request)
    # Redirect to a page after logout (you can specify a different page or leave it empty for the home page)
    return redirect('home')

@login_required
def index(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

from .models import AboutUs
from .forms import ContactForm
from django import forms
from .models import ContactMessage
from django.contrib import messages
def aboutus(request):
    about_us_content = AboutUs.objects.first()
    return render(request, 'aboutus.html', {'about_us_content': about_us_content})


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class Contact(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Saved Successfully...!')
            return redirect('success_page')

        return render(request, self.template_name, {'form': form})
def success_page(request):
    return render(request, 'success_page.html')



class cusser(View):
    def get(self, request):
        return render(request, 'customerservice.html')

def shop_details(request, product_id):
    try:
        # Retrieve the product from the database based on the product_id
        product = Productmaster.objects.get(pk=product_id)
        # Check if there is an offer for the product
        try:
            # If an offer exists, use the discount price
            offer = offers.objects.get(product=product)
            discount_price = offer.discountprice
        except offers.DoesNotExist:
            # If no offer exists, use the regular sales price
            discount_price = None
        # Now, you can use the 'product' object and 'discount_price' in your template or perform other actions
        return render(request, 'shop-details.html', {'product': product, 'discount_price': discount_price})
    except Productmaster.DoesNotExist:
        # Handle the case where the product with the given product_id does not exist
        return HttpResponse("Product not found", status=404)


class Shopping_cart(View):
    @staticmethod
    def get(request):
        cart = Cart(request)
        cart_items = cart.get_cart_items()

        # Calculate the subtotal for each item in the cart
        for item in cart_items:
            # Check if the product has a discount price
            product_id = item['product'].product_id
            offer = offers.objects.filter(product_id=product_id).first()
            discount_price = offer.discountprice if offer else None

            # Calculate total using Decimal for precision
            item['total'] = Decimal(discount_price) * Decimal(item['quantity']) if discount_price else Decimal(item['product'].sales_price) * Decimal(item['quantity'])

            # Set the price to the discount price if available, otherwise use the sales price
            item['display_price'] = Decimal(discount_price) if discount_price else Decimal(item['product'].sales_price)

        # Calculate the overall subtotal and total
        subtotal = sum(item['total'] for item in cart_items)
        total = subtotal  # You can add tax, shipping, etc., as needed

        context = {
            'cart_items': cart_items,
            'cart': cart,
            'subtotal': subtotal,
            'total': total,
        }

        return render(request, 'shopping-cart.html', context)

    @staticmethod
    def post():
        # Handle form submissions or updates here if needed
        return redirect('shopping_cart')

@login_required(login_url='login')


def AddToCart(request, product_id):
    product = get_object_or_404(Productmaster, product_id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product, quantity)

    # Get discount price from the Offer database
    offer = offers.objects.filter(product=product).first()
    discount_price = offer.discountprice if offer else None

    # Calculate the total based on the discount price or sales price
    total_price = quantity * (Decimal(discount_price) if discount_price else Decimal(product.sales_price))

    # Save cart item information to the database
    if request.user.is_authenticated:
        # Assuming UserProfile is related to the User model through a one-to-one relationship
        user_profile = request.user.userprofile
        CartItemlist.objects.create(
            user=user_profile,
            product=product,
            quantity=quantity,
            total=total_price,
            created_at=timezone.now()  # Set the created_at field
        )

    # Redirect to the shopping cart page after adding to cart
    return redirect('shopping_cart')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'cart_count': cart_count})


print("commit")

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        cart = Cart(request)
        cart.update(product_id, quantity)
        # Update the corresponding CartItemlist record
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            product = get_object_or_404(Productmaster, product_id=product_id)
            cart_item = CartItemlist.objects.get(user=user_profile, product=product)
            cart_item.quantity = quantity
            cart_item.total = quantity * product.sales_price
            cart_item.save()
    return redirect('shopping_cart')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    # Remove the corresponding CartItemlist record
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        product = get_object_or_404(Productmaster, product_id=product_id)
        try:
            # Ensure the condition matches the records you want to delete
            cart_item = CartItemlist.objects.filter(user=user_profile, product=product)
            cart_item.delete()
        except CartItemlist.DoesNotExist:
            raise "CartItemlist not found for the given user and product"
    return redirect('shopping_cart')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from django.contrib.auth.models import User
def order_payment(request):
    if request.method == 'POST':
        # Fetch user instance using user ID
        user_id = request.user.id
        print(user_id)# Assuming you have the user ID available
        user_instance = User.objects.get(pk=user_id)
        # Fetch cart items associated with the user
        cart_items = CartItemlist.objects.filter(user=user_id)
        print(cart_items)
        # Extract product IDs from cart items
        product_ids = [item.product_id for item in cart_items]
        print(product_ids)
        # Convert product IDs to string and join them with commas
        products_str = ','.join(map(str, product_ids))
        # Fetch other form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        town = request.POST.get('town')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        status = 'pending'  # Set the desired status
        # Create a Checkout instance
        checkout_instance = Checkout.objects.create(
            first_name=first_name,
            last_name=last_name,
            country=country,
            state=state,
            town_city=town,
            street_address=street_address,
            apartment=apartment,
            postcode=postcode,
            phone=phone,
            email=email,
            user_id=user_id,  # Associate the user instance
            status=status,
            products=products_str  # Set the products field with the extracted product IDs
        )
        # Your remaining code for Razorpay payment and rendering payment.html

        checkout_instance.save()
        get_amount = request.GET.get('total')
        amount=float(get_amount)
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        # Create a Razorpay order
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_amount': razorpay_order['amount'],
            'razorpay_currency': razorpay_order['currency'],
            'razorpay_key': settings.RAZORPAY_API_KEY,
        }
        return render(request, 'payment.html', context)

from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from .models import Orderlistdetails, CartItemlist

def payment_success(request):
    subject = 'Payment Successful'
    message = 'Thank you for your order. Your payment has been successfully processed.'

    # Assuming you have a user logged in
    user_id = request.user.id

    # Fetch cart items associated with the user
    cart_items = CartItemlist.objects.filter(user_id=user_id)

    # Create instances of Orderlistdetails for each product bought by the user
    for cart_item in cart_items:
        Orderlistdetails.objects.create(
            date=date.today(),
            payment_method='Razorpay',
            user_id=user_id,  # Use the correct field name without _id suffix
            status='order confirmed',
            product_id=cart_item.product  # Assign the product instance directly
        )


    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]  # Assuming the user is authenticated, and you have their email address

    send_mail(subject, message, from_email, recipient_list)

    return render(request, 'payment_sucess.html')


@login_required(login_url='login')
def my_order_view(request):
    user_id = request.user.id
    print("user_id", user_id)

    # Fetch all orders for the user
    orders = Orderlistdetails.objects.filter(user_id=user_id)

    # Fetch checkout details for the user
    details = Checkout.objects.filter(user_id=user_id)
    print("orders", orders)
    print("details", details)

    # List to store ordered products with details
    ordered_products = []

    # Iterate over each order to fetch the products
    for order in orders:
        # Fetch all products associated with the current order
        ordered_product = Productmaster.objects.filter(product_id=order.product_id_id).first()
        ordered_products.append({'product': ordered_product, 'order': order, 'detail': details.first()})
        # Append a dictionary with product, order, and detail to the list

    return render(request, 'my_order.html', {'data': ordered_products})

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def download_invoice_view(request, orderID, productID):
    print("orderID", orderID)
    print("productID", productID)

    # Fetch all Orderlistdetails objects corresponding to the orderID
    orders = models.Orderlistdetails.objects.filter(user_id=orderID)

    # Select the first Orderlistdetails object (you may need to adjust this logic)
    if orders.exists():
        order = orders.first()
    else:
        # If no Orderlistdetails objects are found, return a 404 error
        raise Http404("Orderlistdetails not found for the specified user ID.")

    # Fetch the Productmaster object corresponding to the productID
    product = get_object_or_404(models.Productmaster, product_id=productID)

    mydict = {
        'orderDate': order.date,
        'orderStatus': order.status,
        'productName': product.product_name,
        'productImage': product.image_1,
        'productPrice': product.sales_price,
    }

    return render_to_pdf('download_invoice.html', mydict)



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    user_id = request.user.id
    customer=models.userprofile.objects.get(user_id=request.user.id)
    return render(request,'my_profile.html',{'customer':customer})


# 
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# import numpy as np
# from keras.models import load_model
# import random
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# 
# import os
# import json
# 
# json_filename = 'intents.json'  # Replace with your actual JSON filename
# json_data = os.path.join(settings.MEDIA_ROOT, json_filename)
# model_filename = 'chatbot_model_lstm.h5'
# 
# our_model = os.path.join(settings.MEDIA_ROOT, model_filename)
# 
# data_file = open(str(json_data), 'r',encoding='utf-8').read()
# data = json.loads(data_file)  # Replace with your actual JSON data
# inten = json.loads(open(str(json_data),'r', encoding='utf-8').read())
# # Extract patterns and intents from the data
# patterns = []
# intents = []
# for intent in data['intents']:
#     for pattern in intent['patterns']:
#         patterns.append(pattern)
#         intents.append(intent['tag'])
# 
# # Tokenize the text patterns
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(patterns)
# 
# def predict_class(sentence):
#     input_sequence = get_input_sequence(sentence)
#     input_sequence = pad_sequences([input_sequence], padding='post', maxlen=10)  # Adjust maxlen as needed
#     prediction = model.predict(input_sequence)
#     return prediction
# 
# 
# def get_input_sequence(text):
#     input_sequence = tokenizer.texts_to_sequences([text])[0]
#     return input_sequence
# 
# model = load_model(str(our_model))
# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
# 
#         user_message = data.get('message')
# 
#         prediction = predict_class(user_message)
#         confidence_threshold = 0.5
# 
#         if np.max(prediction) < confidence_threshold:
#             result = "I'm sorry, but I couldn't understand your request. Could you please provide more information?"
#         else:
#             intent_index = np.argmax(prediction)
#             selected_intent = intents[intent_index]  # Make sure to define intents
#             list_of_intents = inten['intents']
#             for i in list_of_intents:
#                 if (i['tag'] == selected_intent):
#                     result = random.choice(i['responses'])
#                     break
#         response_data = {"message": result}
#         return JsonResponse(response_data)



from django.shortcuts import render, redirect
from .models import Checkout,Return
class CheckoutView(View):
    def post(self, request):

        return render(request, 'checkout.html')


def sucessuser1(request):
    # If it's a GET request, just render the checkout page
    return render(request, 'sucess.html')

def sucessuser2(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        print("first_name-scuss2", first_name)
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        town = request.POST.get('town')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user_id = request.user.id
        status = 'pending'  # Set the desired status
        products = 5  # Set the desired products

        checkout_instance = Checkout(
            first_name=first_name,
            last_name=last_name,
            country=country,
            state=state,
            town_city=town,
            street_address=street_address,
            apartment=apartment,
            postcode=postcode,
            phone=phone,
            email=email,
            user_id=user_id,
            status=status,
            products=products
        )

        checkout_instance.save()
        return redirect('sucessuser1')

    return render(request, 'checkout.html')

def my_wish_view(request):
    user_id = request.user.id
    orders = Checkout.objects.filter(user_id=user_id)
    ordered_products = []
    for order in orders:
        ordered_product = models.Productmaster.objects.all().filter(product_id=order.products)
        ordered_products.append(ordered_product)


    return render(request, 'my-wish.html', {'data': zip(ordered_products, orders)})


from django.contrib.auth import logout
from . import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from decimal import Decimal  # Add this import
from django.views import View
from .models import Productmaster, offers,YOrder
from django.utils import timezone
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import SignupForm,CancelForm,ReturnForm
from .models import Categorymaster, Myfeatureditems
from .models import Blg

from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@require_POST
def return_order(request, product_id):
    try:
        product = Checkout.objects.get(pk=product_id)
        if product.return_status == 'Return Order':
            # Only update the order_status to 'Pending' if it was 'Return Order'
            product.return_status = 'Return successfull'
            product.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid order status'})
    except Checkout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})



@login_required
def returnorder(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            checkout_instance = form.save(commit=False)
            checkout_instance.user_id = request.user.id
            # Set the user_id field
            checkout_instance.save()
            return redirect('yourorder')  # Redirect to a success URL
    else:
        form = ReturnForm()
        user_id = request.user.id
        orders = Orderlistdetails.objects.filter(user_id=user_id)
        details = Checkout.objects.filter(user_id=user_id)

        ordered_products = []
        return_statuses = []

        for detail in details:  # Fetch cancel status for each detail
            return_statuses.append(detail.return_status)

        for order in orders:
            ordered_product = Productmaster.objects.filter(product_id=order.product_id_id)
            ordered_products.append(ordered_product)

        context = {
            'data': zip(ordered_products, orders, details, return_statuses),
            'checkout_ids': [checkout.id for checkout in details],
            'form': form,# List of checkout IDs
        }

        return render(request, 'returnorder.html', context)




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Checkout
@csrf_exempt  # Use this decorator if you want to disable CSRF protection for simplicity
@require_POST
def cancel_order(request, product_id):
    try:
        product = Checkout.objects.get(pk=product_id)
        if product.cancel_status == 'Cancel Order':
            # Only update the order_status to 'Pending' if it was 'Return Order'
            product.cancel_status = 'Order Cancelled'
            product.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid order status'})
    except Checkout.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})





@login_required
def yourorder(request):

    if request.method == 'POST':
        form = CancelForm(request.POST)
        if form.is_valid():
            checkout_instance = form.save(commit=False)
            checkout_instance.user_id = request.user.id
            # Set the user_id field
            checkout_instance.save()
            return redirect('yourorder')  # Redirect to a success URL
    else:
        form = CancelForm()



    user_id = request.user.id
    orders = Orderlistdetails.objects.filter(user_id=user_id)
    details = Checkout.objects.filter(user_id=user_id)

    ordered_products = []
    cancel_statuses = []  # List to hold cancel statuses

    for detail in details:  # Fetch cancel status for each detail
        cancel_statuses.append(detail.cancel_status)

    for order in orders:
        ordered_product = Productmaster.objects.filter(product_id=order.product_id_id)
        ordered_products.append(ordered_product)

    context = {
        'data': zip(ordered_products, orders, details, cancel_statuses),
        'checkout_ids': [checkout.id for checkout in details] ,
        'form': form,# List of checkout IDs
    }

    return render(request, 'yourorder.html', context)

class cusser(View):
    @staticmethod
    def get(request):
        return render(request, 'customerservice.html')

from .models import UserProfile

from .forms import UserProfileForm

@login_required(login_url='login')
def update_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})


class Privacy(View):
    @staticmethod
    def get(request):
        return render(request, 'privacy_policy.html')

def aboutus(request):
    about_us_content = AboutUs.objects.first()
    return render(request, 'aboutus.html', {'about_us_content': about_us_content})


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class Contact(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Saved Successfully...!')
            return redirect('success_page')

        return render(request, self.template_name, {'form': form})


def success_page(request):
    return render(request, 'success_page.html')

def blog(request):
    print("kkkkkk")
    products = Blg.objects.all()

    context = {'products': products,}
    print("hhhh",products)

    return render(request, "blog.html", context)



