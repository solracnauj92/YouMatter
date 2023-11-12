from django.shortcuts import render
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'client/index.html')

class community(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'client/community.html')

from django.shortcuts import render
from django.views import View
from .models import Item  # Import the Item model

class Shop(View):
    def get(self, request, *args, **kwargs):  
        clothing = Item.objects.filter(category__name__contains='Clothing')
        office = Item.objects.filter(category__name__contains='Office')  # Correct the model name
        posters = Item.objects.filter(category__name__contains='Posters')  # Correct the model name
        bags = Item.objects.filter(category__name__contains='Bags')

        context = {
            'clothing': clothing,  
            'office': office,  
            'posters': posters,  
            'bags': bags,
        }

        return render(request, 'client/shop.html', context)
        
        # render the template
        return render(request, 'client/order.html', context)

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        county = request.POST.get('county')
        postcode = request.POST.get('postcode')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            item = Item.objects.get(pk__exact=int(item))
            item_data = {
                'id': mitem.pk,
                'name': item.name,
                'price': item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            country=county,
            postcode=postcode
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation to email to the user
        body = ('Thank you for your order. Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'client/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'client/order_pay_confirmation.html')


class Item(View):
    def get(self, request, *args, **kwargs):
        mitems = Item.objects.all()

        context = {
            'items': items
        }

        return render(request, 'client/items.html', context)


class ItemSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'items': items
        }

        return render(request, 'client/items.html', context)