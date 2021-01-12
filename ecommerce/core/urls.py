from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
#from .views import ItemDetailView
from django.conf import settings
from django.conf.urls.static import static

from .views import PrezzoDecrescente, PrezzoCrescente, CondizioneUsata, CondizioneNuova, CategoryFilter, \
    OrderSummary, CheckoutView, AllItemView, AcquistiView, OrderDisplay

urlpatterns = [
    path('item_page/', AllItemView.as_view(), name='item-page'),
    path('', views.homeview, name='home'),
    path('user/<username>/', views.userProfileView, name='user_profile'),
    path('altriuser/<username>/', views.altriuserProfileView, name='altriuser-profile'),
    path('nuovo-item/', login_required(views.AggiungiItem.as_view()), name="aggiungi_item"),
    #path('item/<int:pk>/', login_required(views.visualizzaItem), name="item_view"),
    #path('item/<int:pk>/',ItemDetailView.as_view(), name="item_view"),
    path('products/<slug>', views.ItemDetailView.as_view(), name='item_view'),
    path('item/<int:pk>/delete/', login_required(views.ItemDelete.as_view()),  name='item-delete'),
    path('item/<int:pk>/modifica/', login_required(views.ItemChange.as_view()), name="item-modifica"),
    path('cerca/', views.cerca, name='cerca'),
    path('decrescenteprezzo/', PrezzoDecrescente.as_view(), name="decrescente-prezzo" ),
    path('crescenteprezzo/', PrezzoCrescente.as_view(), name ="crescente-prezzo" ),
    path('categorie/<str:cat>', views.CategoryFilter, name ="categorie" ),
    path('condizione/usata',CondizioneUsata.as_view(), name ="condizione-usata" ),
    path('condizione/nuova', CondizioneNuova.as_view(), name="condizione-nuova"),
    path('user/<username>/vendite/', login_required(views.venditeview), name='user-vendite'),
    path('user/<username>/grafico/', login_required(views.venditegraf), name='user-grafico-vendite'),
    path('user/<username>/address_page/', login_required(views.addressview), name = 'address-page'),
    path('user/address/<int:pk>', login_required(views.address_detail), name="address"),
    path('user/address/<int:pk>/delete/', login_required(views.AddressDelete.as_view()), name="address-delete"),
    path('user/address/<int:pk>/modifica/', login_required(views.AddressChange.as_view()), name="address-modifica"),
    path('user/acquisti', login_required(views.AcquistiView.as_view()), name='acquisti'),
    #ordine
    path('add-to-cart/<slug>', login_required(views.add_to_cart), name="add-to-cart"),
    path('remove-from-cart/<slug>',login_required(views.remove_from_cart), name="remove-from-cart"),
    path('checkout/', login_required(CheckoutView.as_view()), name='checkout'),
    path('order-summary/',login_required(OrderSummary.as_view()), name ='order-summary'),
    path('order-display/<pk>',login_required(OrderDisplay.as_view()), name ='order-display')
]

