import string
import datetime
from random import random
import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView, DetailView, FormView, CreateView
from django.views.generic.base import View
from django.views.generic.list import ListView

from accounts.models import UserProfile

# Create your views here.
# def homepage(request):
#   return render(request, 'core/homepage.html')
from core.forms import CheckoutForm
from core.models import Item, OrderItem, Order, ShoppingAddress, Payment, ItemConsigliato

#def homepage (request):
#return render(request ,'core/homepage.html')
class AllItemView(ListView):
    model = Item
    paginate_by = 4
    template_name = "core/item_page.html"
    queryset = Item.objects.filter(ordered = False).order_by("-pk")




def homeview(request):

    object_list = Item.objects.filter( ordered=False).order_by("-pk")
    #paginator = Paginator(object_list, 4)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    #print(context)
    if(request.user.is_authenticated):
        item_consigliati = ItemConsigliato.objects.filter( user = request.user)
        for racc in item_consigliati:
            racc.save()
        if item_consigliati.exists() :
            order_qs = Order.objects.filter(user=request.user, is_ordered=True,)
            order_item_qs = OrderItem.objects.filter(user=request.user, is_ordered=True , consigliato=False)

            for item in order_item_qs:
                    for racc in item_consigliati:

                        if(item.product.condizioni == 'N'):
                            racc.condizioneN +=1
                        if(item.product.condizioni == 'U'):
                            racc.condizioneU +=1
                        racc.num_item +=1
                        racc.sum_prezzo += item.product.prezzo
                        racc.prezzo = racc.sum_prezzo/racc.num_item
                        item.consigliato = True
                        item.save()
                #print(item.product.tagliaEU)
                #print(item.product.categoria)
                #print(item.product.condizioni)
            for racc in item_consigliati:
                print(racc.prezzo)
               # print(racc.categoriaN)
                print(racc.num_item)
                racc.save()
                print(racc.num_item)


        else:
            item_consigliati = ItemConsigliato.objects.create(user = request.user)
            order_qs = Order.objects.filter(user=request.user, is_ordered=True, )
            order_item_qs = OrderItem.objects.filter(user=request.user, is_ordered=True, consigliato=False)

            for item in order_item_qs:
                    if (item.product.condizioni == 'N'):
                        item_consigliati.condizioneN += 1
                    if (item.product.condizioni == 'U'):
                        item_consigliati.condizioneU += 1
                    item_consigliati.num_item += 1
                    item_consigliati.sum_prezzo += item.product.prezzo
                    item_consigliati.prezzo = item_consigliati.sum_prezzo / item_consigliati.num_item
                    item.consigliato = True
                    item.save()
            item_consigliati.save()
            print('da creare')

          #print(order_item_qs)
    recommendation_list = []
    convenientinew_list = []
    convenientiused_list = []
    if (request.user.is_authenticated):
        item_consigliati = ItemConsigliato.objects.filter(user=request.user)
        for it in object_list:
            #gli item consigliati derivano dalla combinazione della condizione con il prezzo
            for consigliato in item_consigliati:
                if(it.autore_vendita != request.user):
                    if((it.prezzo>=consigliato.prezzo and it.prezzo<=consigliato.prezzo + 100) or (it.prezzo<=consigliato.prezzo and it.prezzo >=consigliato.prezzo -100)):
                        if((consigliato.condizioneN == consigliato.condizioneU) and (consigliato.condizioneN >= 2 or consigliato.condizioneU >= 2)):
                            if (it not in recommendation_list):
                                 recommendation_list.append(it)
                        if ((consigliato.condizioneN > consigliato.condizioneU) and (consigliato.condizioneN >= 2 or consigliato.condizioneU >= 2)):
                            if (it.condizioni == 'N'):
                                if (it not in recommendation_list):
                                    recommendation_list.append(it)
                        else:
                            if((consigliato.condizioneN< consigliato.condizioneU)and (consigliato.condizioneN>=2 or consigliato.condizioneU>=2)):
                                if(it.condizioni == 'U'):
                                    if (it not in recommendation_list):
                                        recommendation_list.append(it)

                #recommendation_list.append(it)
    for it in object_list:
        if (it.prezzo <= 300 and it.condizioni == 'N'):
            convenientinew_list.append(it)
        if (it.prezzo <= 300 and it.condizioni == 'U'):
            convenientiused_list.append(it)


    recommendation_list = sorted(recommendation_list[:4], key=lambda item: (item.prezzo)) #ordino gli item consigliati da quello con prezzo minore
    convenientinew_list = sorted(convenientinew_list[:4], key=lambda item: (item.prezzo))
    convenientiused_list = sorted(convenientiused_list[:4], key=lambda item: (item.prezzo))

    context = {
        'object_list': object_list,
        "recommendation_list":recommendation_list,
        "convenientinew_list":convenientinew_list,
        "convenientiused_list":convenientiused_list
    }
    print(recommendation_list)
    return render(request, 'core/homepage.html', context,)



def userProfileView (request, username ):
    '''
    Visualizza la pagina del profilo utente
    :param username: nome dell'utente
    :return: rotorna la pagina del profilo utente
    '''
    if request.user.username != username:
        return altriuserProfileView(request, username)
    user = get_object_or_404(User, username=username)
    items_utente = Item.objects.filter(autore_vendita=user.pk , ordered=False).order_by("-pk")
    paginator = Paginator(items_utente, 3)  # Show 4 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"user": user, "items_utente": page_obj, "page_obj": page_obj}
    return render(request, 'core/profilo.html', context)


class AggiungiItem(CreateView):
    '''
    tramite la CreateView di Django, permette la creazione dell'item
    '''
    model = Item
    fields = ["nome", "prezzo", "categoria", "descrizione", "immagine", "tagliaEU",
              "condizioni"]
    template_name = "core/aggiungi_prodotto.html"

    def form_valid( self, form ):
        form.instance.autore_vendita_id = self.request.user.pk
        print(form.instance.nome)
        return super(AggiungiItem, self).form_valid(form)

    def get_success_url( self ):
        #pk = self.object.id
        #success_url = reverse_lazy("home", kwargs={'pk': pk})
        success_url = reverse_lazy("home")
        return success_url

    #def visualizzaItem(request, pk):
    '''
    :param pk: id dell'item di cui visualizzare i dettagli
    '''
    #item = get_object_or_404(Item, pk=pk)
    #utente = request.user.profile

    #context = {"item": item , "utente": utente}
    #return render(request, "core/item.html", context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "core/item.html"



def altriuserProfileView(request, username, ):
    '''
    Visualizza profilo utente esterno
    :param username: nome utente esterno da visualizzare
    '''
    user = get_object_or_404(User, username=username)

    items_utente = Item.objects.filter(autore_vendita=user.pk, ordered=False).order_by("-pk")
    paginator = Paginator(items_utente, 3)  # Show 3 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"user": user,"items_utente":page_obj, "page_obj": page_obj}
    return render(request, 'core/user_profile.html', context)

class ItemDelete(DeleteView):
    '''
    Eliminazione di un item
    '''
    model = Item
    template_name = 'core/deleteitem.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        itemid = self.kwargs['pk']
        item = get_object_or_404(Item, id=itemid)

        if user.id is not item.autore_vendita.id:
            messages.info(request, "Non puoi accedere a questa pagina!")
            return homeview(request)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        itemid = self.kwargs['pk']
        item = get_object_or_404(Item, id=itemid)
        user = get_object_or_404(User, username=item.autore_vendita)
        return reverse_lazy('user_profile', kwargs={'username': user})


class ItemChange(UpdateView):
    '''
    Modifica il nome, la taglia e il prezzo  dell'item
    '''
    model = Item
    fields = ('nome','prezzo','tagliaEU')
    template_name = 'core/modifica_item.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        itemid = self.kwargs['pk']
        item = get_object_or_404(Item, id=itemid)

        if user.id is not item.autore_vendita.id:
            messages.info(request, "Non puoi accedere a questa pagina!")
            return homeview(request)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        itemid = self.kwargs['pk']
        item = get_object_or_404(Item, id=itemid)
        user = get_object_or_404(User, username=item.autore_vendita)
        return reverse_lazy('user_profile', kwargs={'username': user})


class PrezzoCrescente(ListView):
    model = Item
    paginate_by = 4
    template_name = "core/item_page.html"
    queryset = Item.objects.filter(ordered=False).order_by("prezzo")

class PrezzoDecrescente(ListView):
    model = Item
    paginate_by = 4
    template_name = "core/item_page.html"
    queryset = Item.objects.filter(ordered=False).order_by("-prezzo")



class CondizioneUsata(ListView):
    model = Item
    paginate_by = 4
    template_name = "core/item_page.html"
    queryset = Item.objects.filter(condizioni='U' , ordered=False).order_by("-pk")

class CondizioneNuova(ListView):
    model = Item
    paginate_by = 4
    template_name = "core/item_page.html"
    queryset = Item.objects.filter(condizioni='N', ordered=False).order_by("-pk")





def cerca( request, ):
    '''
    Barra di ricerca

    :return: ritorna la pagina che mostra i risultati della ricerca
    '''
    if "q" in request.GET:
        querystring = request.GET.get("q")
        # print(querystring)
        if len(querystring) == 0:
            return redirect("/cerca/")
        items = Item.objects.filter(nome__icontains=querystring ,ordered=False).order_by("-pk")
        users = User.objects.filter(username__icontains=querystring)
        # print(users)
        context = {"items": items, "users": users}
        return render(request, 'core/cerca.html', context)
    else:
        return render(request, 'core/cerca.html')



def CategoryFilter(request,cat):
    #print(cat)
    object_list = Item.objects.filter(categoria=cat , ordered=False).order_by("-pk")
    paginator = Paginator(object_list, 3)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': object_list , "object_list": page_obj, "page_obj": page_obj
    }
    #print(context)
    return render(request, 'core/homepageCat.html', context,)

#def per verificare che i campi del form siano compilati
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get( self,*args,**kwargs ):
        form = CheckoutForm()
        context = {
            'form': form
        }

        shipping_address_qs = ShoppingAddress.objects.filter(user = self.request.user, default=True)
        if shipping_address_qs.exists():
            context.update({'default_shipping_address': shipping_address_qs[0]})
        return  render(self.request,"core/ordine/checkout.html",context)

    def post( self, *args, **kwargs ):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            if form.is_valid():
                # print(form.cleaned_data)
                # print("form valido")
                form.use_default_shipping = form.cleaned_data.get('use_default_shipping')
                #form.save_info = form.cleaned_data.get('save_info')
                if form.use_default_shipping:
                    print('uso indirizzo di default')
                    address_qs = ShoppingAddress.objects.filter(user=self.request.user, default=True)
                    if address_qs.exists():
                        shopping_address = address_qs[0]
                        order_items = order.items.all()
                        order_items.update(is_ordered=True)
                        order.shopping_address = shopping_address
                        for item in order_items:
                            item.product.ordered = True
                            item.product.compratore = order.get_username()
                            item.product.address = order.get_address()
                            item.product.data = timezone.now()
                            item.product.save()
                            item.save()

                        order.shopping_address = shopping_address
                        order.is_ordered = True
                        order.ordered_date = timezone.now()
                        order.save()
                        payment = Payment()
                        payment.user = self.request.user
                        payment.amount = order.get_total()
                        payment.order = order
                        payment.save()
                    else:
                        messages.info(self.request,"Nessun indirizzo di default")
                        return redirect('checkout')
                else:
                    form. stato = form.cleaned_data.get('stato')
                    form.città = form.cleaned_data.get('città')
                    form.via = form.cleaned_data.get('via')
                    form.cap = form.cleaned_data.get('cap')
                    form.interno = form.cleaned_data.get('interno')
                    form.note = form.cleaned_data.get('note')

                    #form.save_info = form.cleaned_data.get('save_info')
                    form.opzioni_pagamento = form.cleaned_data.get('opzioni_pagamento')
                    if is_valid_form([form.stato,form.città,form.via,form.cap]):
                        shopping_address = ShoppingAddress(
                            user=self.request.user,
                            stato=form.stato,
                            città=form.città,
                            cap=form.cap,
                            via=form.via,
                            interno=form.interno,
                            note=form.note
                        )
                        shopping_address.save()
                        order_items = order.items.all()
                        order_items.update(is_ordered=True)
                        order.shopping_address = shopping_address
                        for item in order_items:
                            item.product.ordered = True
                            item.product.compratore = order.get_username()
                            item.product.data = timezone.now()
                            item.product.address = order.get_address()
                            item.product.save()
                            item.save()

                        order.shopping_address= shopping_address
                        order.is_ordered = True
                        order.ordered_date = timezone.now()
                        order.save()
                        payment = Payment()
                        payment.user = self.request.user
                        payment.amount = order.get_total()
                        payment.order = order
                        payment.save()

                        form.save_info = form.cleaned_data.get('save_info')
                        if form.save_info:
                            shopping_address.default = True
                            shopping_address.save()
                    else:
                        messages.info( self.request, "Compila i campi obbligatori per continuare")
                        return redirect('checkout')

            messages.info(self.request,"l'ordine è stato ricevuto con successo")
            return redirect('home')

            messages.warning(self.request, "il checkout non è andato a buon fine ")
            return redirect('checkout')
            return render(self.request, 'core/ordine/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Non hai nessun ordine in corso")
            return redirect('order-summary')




class OrderSummary(View):
    def get( self,*args,**kwargs ):
        try:
            order = Order.objects.get(user=self.request.user,is_ordered=False)
            context = { 'object': order}
            return render(self.request, 'core/ordine/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"Non hai nessun ordine in corso")
            return redirect('home')


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(product=item , user = request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user , is_ordered=False)
    if order_qs.exists() :
        order = order_qs[0]
        if order.items.filter(product__slug =item.slug).exists():
            order_item.quantity = 1
            order_item.save()
            messages.info(request,"Hai già aggiunto questo prodotto  al carrello!")
        else:
            order.items.add(order_item)
            messages.info(request,"l'item è stato aggiunto con successo al carrello")
            return redirect('home')
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(user=request.user,date_ordered=date_ordered)
        #order_item.ordered_date = date_ordered
        #order_item.save()
        order.items.add(order_item)
        messages.info(request,"l'item è stato aggiunto con successo al carrello")

    return redirect('home')


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(product=item, user=request.user, is_ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request,"l'item è stato rimosso correttamente dal carrello")
            return redirect(reverse_lazy('order-summary'))
        else:
            messages.info(request, "l'item non è nel carrello")
            return redirect(reverse_lazy('item_view', kwargs={
                'slug': slug}))
    else:
        messages.info(request, "non hai un ordine attivo")
        return redirect(reverse_lazy('item_view', kwargs={
            'slug': slug}))





def venditeview (request, username ):
    '''
    Visualizza gli item venduti dall'utente
    '''
    if request.user.username != username:
        messages.info(request, "Non puoi accedere a questa pagina!")
        return homeview(request)
    user = get_object_or_404(User, username=username)
    items_utente = Item.objects.filter(autore_vendita=user.pk , ordered=True).order_by('-data')
    paginator = Paginator(items_utente, 10)  # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"user": user, "items_utente": page_obj, "page_obj": page_obj,}
    return render(request, 'core/vendite_utente.html', context)



def addressview(request, username):
    if request.user.username != username:
        messages.info(request, "Non puoi accedere a questa pagina!")
        return homeview(request)
    user = get_object_or_404(User, username=username)
    address_utente = ShoppingAddress.objects.filter(user =user.pk)
    context = {"user": user, "address_utente": address_utente}
    return render(request, 'accounts/address_page.html', context)


def address_detail(request, pk):

    address = ShoppingAddress.objects.get(pk=pk)
    if request.user.id != address.user.id:
        messages.info(request, "Non puoi accedere a questa pagina!")
        return homeview(request)
    #user = get_object_or_404(User, username=address.user)
    return render(request, 'accounts/address.html', context={'object': address})



class AddressDelete(DeleteView):
    '''
    Eliminazione di un indirizzo
    '''
    model = ShoppingAddress
    template_name = 'accounts/address_delete.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        addressid = self.kwargs['pk']
        address = get_object_or_404(ShoppingAddress, id=addressid)

        if user.id is not address.user.id:
            messages.info(request, "Non puoi accedere a questa pagina!")
            return homeview(request)

        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        addressid = self.kwargs['pk']
        address= get_object_or_404(ShoppingAddress, id=addressid)
        user = get_object_or_404(User, username=address.user)
        #user = get_object_or_404(User, username=self.username)
        #address_utente = ShoppingAddress.objects.filter(user=user.pk)
        return reverse_lazy('address-page' , kwargs = {'username': user})


class AddressChange(UpdateView):
    '''
    Modifica l'indirizzo, serve principalmente per decidere che indirizzo utilizzare come default
    '''
    model = ShoppingAddress
    fields = ('città','via','stato','cap','default')
    template_name = 'accounts/modifica_address.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        addressid = self.kwargs['pk']
        address = get_object_or_404(ShoppingAddress, id=addressid)

        if user.id is not address.user.id:
            messages.info(request, "Non puoi accedere a questa pagina!")
            return homeview(request)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        addressid = self.kwargs['pk']
        address = get_object_or_404(ShoppingAddress, id=addressid)
        user = get_object_or_404(User, username=address.user)
        return reverse_lazy('address-page', kwargs={'username': user})



class AcquistiView(View):
    model = User
    template_name = '/core/acquisti.html'

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        acquisti = Payment.objects.filter(user=user).order_by("-pk")
        paginator = Paginator(acquisti, 10)  # Show 10 contacts per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'User': user,
            'listacquisti': page_obj,
            'page_obj': page_obj
        }
        return render(self.request, 'core/acquisti.html', context)


class OrderDisplay(View):
    model = Order
    template_name = '/core/ordine/orderdisplay.html'

    def get(self, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id, is_ordered = True)
        context = {
            'User': self.request.user,
            'listacquisti': order.items.all()
        }

        return render(self.request, 'core/ordine/orderdisplay.html', context)
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        orderid = self.kwargs['pk']
        order = get_object_or_404(Order, id=orderid)

        if user.id is not order.user.id:
            messages.info(request, "Non puoi accedere a questa pagina!")
            return homeview(request)

        return super().dispatch(request, *args, **kwargs)



def venditegraf(request,username):
    now = datetime.datetime.now()
    start_date = int(now.strftime("%m"))
    #start_date = str(int(start_date) - 1)
    print(start_date)
    if request.user.username != username:
        messages.info(request, "Non puoi accedere a questa pagina!")
        return homeview(request)
    user = get_object_or_404(User, username=username)
    items_utente = Item.objects.filter(autore_vendita=user.pk, ordered=True, data__month=start_date)
    items = {}
    for x in items:
        items[x] = 0;
    for x in items_utente:
        items[int(x.data.strftime("%d"))] = 0
    for x in  items_utente:
        if(x.data):
            items[int(x.data.strftime("%d"))] += 1
        #print( items[int(x.data.strftime("%d"))])
        #print(x.data.strftime("%d"))
    list = [(k, v) for k, v in items.items()]
    print(list)



    context = {'items': list,}
    return render(request, 'core/grafvendite.html', context)