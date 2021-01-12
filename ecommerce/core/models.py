
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone

CATEGORY_CHOICES = (
    ('N', 'Nike'),
    ('A', 'Adidas'),
    ('J', ' Air Jordan'),
    ( 'L', 'Luxury Brands'),
    ('O',  'Altri Brands')
)

LABEL_CHOICES = (
    ('N', 'Deadstock(New)'),
    ('U', 'Used')
)




# Create your models here.
class Item(models.Model):
    nome = models.CharField(max_length=100)
    prezzo = models.FloatField(validators = [MinValueValidator(0.0)])
    categoria = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = AutoSlugField(populate_from='nome', unique=True)   #chiave primaria
    descrizione = models.TextField()
    immagine = models.ImageField()
    tagliaEU = models.FloatField(validators = [MinValueValidator(35.0), MaxValueValidator(47.0)],)
    condizioni = models.CharField(choices=LABEL_CHOICES, max_length=1)
    autore_vendita = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scarpe")
    data = models.DateTimeField(auto_now_add=True) # data in cui avviene l'ordine
    ordered = models.BooleanField(default=False)  # identifica se l'item è  stato acquistato
    compratore = models.CharField (null=True,max_length=50) #identifica chi ha comprato l'item
    address = models.CharField(null=True, max_length=100)
    def __str__(self):
        return self.nome

    def get_absolute_url( self ):
        return reverse('item_view', kwargs={'slug': self.slug})

    def get_add_to_cart_url( self ):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url( self ):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})




class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    is_ordered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(default=timezone.now)
    consigliato =models.BooleanField(default=False)
    def __str__( self ):
        return self.product.nome

    def get_tot_price(self):
        return self.product.prezzo * self.quantity

    def get_final_price(self):
        return self.get_tot_price()


class Order(models.Model):
    #ref_code = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField()
    shopping_address = models.ForeignKey('ShoppingAddress',on_delete=models.SET_NULL,blank=True, null=True)

   # def get_cart_items( self ):
    #    return self.items.all()
    #def get_cart_total( self ):
     #   return sum([item.product.prezzo for item in self.items.all()])



    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def __str__(self):
     #return  '{0} - {1}'.format(self.owner,self.ref_code)
     return self.user.username

    def get_username( self ):
        # return  '{0} - {1}'.format(self.owner,self.ref_code)
        return self.user.username

    def get_address( self ):
        # return  '{0} - {1}'.format(self.owner,self.ref_code)
        return self.shopping_address.città + " " + self.shopping_address.via



class ShoppingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stato = models.CharField(max_length=30)
    città = models.CharField(max_length=50)
    cap = models.CharField(max_length=5)
    via = models.CharField(max_length=50)
    interno = models.CharField(max_length=30, blank=True)
    note = models.TextField(blank=True)
    default = models.BooleanField(default=False)

    def __str__(self):
     return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ItemConsigliato(models.Model):
    num_item = models.PositiveIntegerField(default=0)
    condizioneN = models.PositiveIntegerField(default=0)
    condizioneU = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prezzo = models.FloatField(validators=[MinValueValidator(0.0)] , default=0)
    sum_prezzo = models.FloatField(default=0)



    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'ItemConsigliati'



