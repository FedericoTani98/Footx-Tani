from django.test import TestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase



from django.test import TestCase
from django.contrib.auth.models import User


from accounts.models import UserProfile
from core.models import Item, ShoppingAddress


class CoreCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='dummy', email='dummy@dummy.com', password='dummypassword')
        self.credential = {'username': 'dummy', 'password': 'dummypassword'}
        self.item = Item.objects.create(nome="Nome Test",
                                        prezzo="30",
                                        categoria="A",
                                        descrizione="Descrizione Test",
                                        immagine="n",
                                        tagliaEU="42",
                                        condizioni='N',
                                        autore_vendita=self.user)

        self.address = ShoppingAddress.objects.create(user=self.user,
                                        città="Del Sole",
                                        stato="O",
                                        cap="45667",
                                        via="n",
                                        interno="3",
                                        note="ciao")
        self.user2 = User.objects.create_user(username='dummy2', email='dummy@dummy.com', password='dummypassword')
        self.credential2 = {'username': 'dummy2', 'password': 'dummypassword'}




    def test_visualizzaItem(self):
        '''
        controllo  che l'utente riesca a visualizzare il suo annuncio dell'item appena  creato
        '''
        self.client.login(**self.credential)
        response = self.client.get('/products/' + self.item.slug)
        self.assertTemplateUsed(response , 'core/item.html')
        self.assertEqual(response.status_code, 200)

    def test_CreaItem( self ):
        '''
        Verifico che nella creazione dell'item  i campi obbligatori siano rispettati
        '''
        self.client.login(**self.credential)
        response = self.client.post('/nuovo-item/', {})
        self.assertFormError(response, 'form', 'nome', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'prezzo', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'categoria', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'descrizione', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'immagine', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'tagliaEU', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'condizioni', 'Questo campo è obbligatorio.')

        self.assertTemplateUsed(response, 'core/aggiungi_prodotto.html')
        self.assertEqual(response.status_code, 200)  # verifica per capire se il template utilizzato è quello corretto

        response = self.client.post('/nuovo-item/',
                                    {'nome': 'J4', 'prezzo': '50', 'categoria': 'A', 'descrizione': 'v',
                                     'immagine': 's',
                                     'tagliaEU': '45', 'condizioni': 'U'})
        self.assertTemplateUsed(response,  'core/aggiungi_prodotto.html')
        self.assertEqual(response.status_code, 200)


    def test_item_change(self):
        # con utente autenticato
        self.client.login(**self.credential)
        response = self.client.get('/item/' + str(self.item.id) + '/modifica/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/item/' + str(self.item.id) +'/modifica/', {})
        self.assertFormError(response, 'form', 'nome', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'prezzo', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'tagliaEU', 'Questo campo è obbligatorio.')
        response = self.client.post('/item/' + str(self.item.id) + '/modifica/',
                                    {'nome':'mod' , 'prezzo':'50' , 'tagliaEU':'38'})
        self.assertRedirects(response, '/user/' + self.user.username + '/')
        self.client.logout()

        # con utente  autenticato ma non creatore
        self.client.login(**self.credential2)
        response = self.client.get('/item/' + str(self.item.id) +'/modifica/')
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertTemplateNotUsed(response, 'core/modifica_item.html')

    def test_item_delete(self):
        # con utente autenticato
        self.client.login(**self.credential)
        response = self.client.get('/item/' + str(self.item.id) +'/delete/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/item/' + str(self.item.id) + '/delete/', {})
        self.assertRedirects(response, '/user/' + self.user.username + '/')
        self.client.logout()

        # con utente autenticato ma non creatore
        self.client.login(**self.credential2)
        response = self.client.get('/item/' + str(self.item.id) +'/delete/')
        self.assertTemplateNotUsed(response, 'core/deleteitem.html')

    def test_login_required( self ):
        '''test on login_required sulla creazione di un item'''
        response = self.client.get('/nuovo-item/')
        self.assertRedirects(response, '/accounts/login/?next=/nuovo-item/')
        # 302 --> FOUND: pagina esiste ma non puoi entrarci
        self.assertEqual(response.status_code, 302)

    def test_new_item(self):
        self.client.login(**self.credential)
        response = self.client.get('/nuovo-item/')
        self.assertEqual(response.status_code, 200)

    def test_userProfileView( self ):
        # con utente autenticato
        # su il tuo profilo
        self.client.login(**self.credential)
        response = self.client.get('/user/' + self.user.username + '/')
        self.assertTemplateUsed(response, 'core/profilo.html')
        self.assertTrue(response.status_code, 200)

        # sul profilo degli altri
        response = self.client.get('/altriuser/' + self.user2.username + '/')
        self.assertTemplateNotUsed(response, 'core/profilo.html')
        self.assertTemplateUsed(response, 'core/user_profile.html')

        # con utente non autenticato
        self.client.logout()
        response = self.client.get('/altriuser/' + self.user.username + '/')
        self.assertTemplateUsed(response, 'core/user_profile.html')
        self.assertTrue(response.status_code, 200)

    def test_address_change( self ):
        # con utente autenticato
        self.client.login(**self.credential)
        response = self.client.get('/user/address/' + str(self.address.id) + '/modifica/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/user/address/' + str(self.address.id) + '/modifica/', {})
        self.assertFormError(response, 'form', 'città', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'via', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'stato', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'cap', 'Questo campo è obbligatorio.')
        response = self.client.post('/user/address/' + str(self.address.id) + '/modifica/',
                                    {'città': 'modena', 'via': 'S50', 'stato': 'it','cap':'3434'})
        self.assertRedirects(response, '/user/' + self.user.username + '/address_page/')
        self.client.logout()

        # con utente  autenticato ma non creatore
        self.client.login(**self.credential2)
        response = self.client.get('/user/address/' + str(self.address.id) + '/modifica/')
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertTemplateNotUsed(response, 'accounts/modifica_address.html')

    def test_address_delete( self ):
        # con utente autenticato
        self.client.login(**self.credential)
        response = self.client.get('/user/address/' + str(self.address.id) + '/delete/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/user/address/' + str(self.address.id) + '/delete/', {})
        self.assertRedirects(response, '/user/' + self.user.username + '/address_page/')
        self.client.logout()

        # con utente autenticato ma non creatore
        self.client.login(**self.credential2)
        response = self.client.get('/user/address/' + str(self.address.id) + '/delete/')
        self.assertTemplateNotUsed(response, 'accounts/address_delete.html')

