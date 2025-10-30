from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
import razorpay
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders
from django.contrib import messages
from math import ceil
from ecommerceapp import keys
from django.conf import settings
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
from PayTm import Checksum
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.
def index(request):

    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params)

    
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        try:
            # Get form data
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            amount = request.POST.get('amt')
            email = request.POST.get('email', '')
            address1 = request.POST.get('address1', '')
            address2 = request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')

            # Validate required fields
            if not all([items_json, name, amount, email, address1, city, state, zip_code, phone]):
                messages.error(request, "Please fill all required fields")
                return render(request, 'checkout.html')

            # Create the order
            order = Orders(
                items_json=items_json,
                name=name,
                amount=amount,
                email=email,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                zip_code=zip_code,
                phone=phone
            )
            order.save()

            try:
                # Convert amount to paise for Razorpay
                amount_in_paise = int(float(amount) * 100)
                currency = 'INR'

                # Create Razorpay Order
                razorpay_order = razorpay_client.order.create({
                    'amount': amount_in_paise,
                    'currency': currency,
                    'payment_capture': '1'
                })

                # Update order with Razorpay details
                order.razer_order_id = razorpay_order['id']
                order.save()

                # Create order update
                update = OrderUpdate(
                    order_id=order.order_id,
                    update_desc="Order has been placed and awaiting payment"
                )
                update.save()

                # Prepare payment details for frontend
                callback_url = 'paymenthandler/'
                context = {
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                    'razorpay_amount': amount_in_paise,
                    'currency': currency,
                    'callback_url': callback_url
                }

                return render(request, 'index1.html', context=context)

            except Exception as e:
                # Clean up order if Razorpay integration fails
                order.delete()
                messages.error(request, f"Payment setup failed: {str(e)}")
                return render(request, 'checkout.html')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'checkout.html')
            # Convert amount to paise for Razorpay
            amount_in_paise = int(float(amount) * 100)
            currency = 'INR'

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create({
                'amount': amount_in_paise,
                'currency': currency,
                'payment_capture': '1'  # Auto capture payment
            })

            # Save order ID and create update
            Order.razer_order_id = razorpay_order['id']
            Order.save()
            
            update = OrderUpdate(
                order_id=Order.order_id,
                update_desc="Order has been placed and awaiting payment"
            )
            update.save()
            thank = True
# # PAYMENT INTEGRATION

        # id = Order.order_id
        # oid=str(id)+"ShopyCart"
        # param_dict = {

        #     'MID':keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

            # Prepare payment details for frontend
            callback_url = 'paymenthandler/'
            
            # Pass details to frontend
            context = {
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': amount_in_paise,
                'currency': currency,
                'callback_url': callback_url
            }

        return render(request, 'index1.html', context=context)
        # return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


def initiate_payment(amount, currency='INR'):
   data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': currency,
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
   response = razorpay_client.order.create(data=data)
   return response['id']
@csrf_exempt
def paymenthandler(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        # Get payment details from POST request
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        if not all([payment_id, razorpay_order_id, signature]):
            return HttpResponseBadRequest("Missing payment parameters")

        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            return render(request, 'paymentfail.html', {'error': f'Payment verification failed: {str(e)}'})

        try:
            # Update order status
            order = Orders.objects.get(razer_order_id=razorpay_order_id)
            order.paymentstatus = "PAID"
            order.amountpaid = str(order.amount)
            order.save()

            # Create order update
            update = OrderUpdate(
                order_id=order.order_id,
                update_desc="Payment successful and order confirmed"
            )
            update.save()

            return render(request, 'paymentsuccess.html', {
                'order_id': order.order_id,
                'amount': order.amount
            })

        except Orders.DoesNotExist:
            return render(request, 'paymentfail.html', {'error': 'Order not found'})

    except Exception as e:
        return render(request, 'paymentfail.html', {'error': f'Payment processing error: {str(e)}'})
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("ShopyCart","")
           
            print(rid)
            filter2= Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                post1.oid=a
                post1.amountpaid=b
                post1.paymentstatus="PAID"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    rid=""
    for i in items:
        print(i.oid)
        # print(i.order_id)
        myid=i.oid
        rid=myid.replace("ShopyCart","")
        print(rid)
    
    if rid.isdigit():
        status = OrderUpdate.objects.filter(order_id=int(rid))
    else:
        status =""

        # Handle the error (e.g., log the error, raise an exception, or return a response)
        print("Invalid order ID:", rid)    
    # status=OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)
    context ={"items":items,"status":status}
    # print(currentuser)
    return render(request,"profile.html",context)