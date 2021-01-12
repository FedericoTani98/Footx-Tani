from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from accounts.forms import FormRegistrazione


class LogInTest(TestCase):
    '''
    Per eseguire i test abbiamo bisogno di un utente con credenziali valide
    L'utente viene creato con questa funzione di setup
    '''
    def setUp(self):
        self.dummy_user = User.objects.create_user(username='dummy', password='nothings', email='dummy@dummy.com')

    '''
    Test se tutti i campi per la registrazione sono obbligatori
    e che si rimanga sulla pagina di registrazione
    Inserisco  due password diverse per vedere se il form ritorna un errore
    Infine inserisco  dei valori validi e  controllo  che vengano accettati 
    '''
    def test_registrazione(self):
        # Test POST invalid data
        response = self.client.post('/accounts/registrazione/', {})
        self.assertFormError(response, 'form', 'username', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'email', 'Questo campo è obbligatorio.')
        self.assertFormError(response, 'form', 'password1', 'Questo campo è obbligatorio.')
        self.assertTemplateUsed(response, 'accounts/registrazione.html')
        self.assertEqual(response.status_code, 200) # codice 200: la richiesta ha avuto successso

        response = self.client.post('/accounts/registrazione/', {'username':self.dummy_user.username, 'email':self.dummy_user.email,
                                                                 'password1':'ciaoone', 'password2':'wrong'})

        self.assertFormError(response, 'form', 'password2', 'I due campi password non corrispondono.')

        form_data = {'username':'user', 'email':'mail','password1':'vigorsol', 'password2':'vigorsol'}
        form = FormRegistrazione(data=form_data)
        self.assertTrue(form.is_valid())

    '''
    In questo test si controlla che l'utente creato nel setUp possa fare un login
    Poi inserisco  delle credenziali false per vedere se il sistema rifuta il login
    '''
    def test_login(self):
        fake_credential = {'username':'ciao', 'password':'ciao'}
        true_credential = {'username':'dummy', 'password':'nothings'}
        t_cred = self.client.login(**true_credential)
        f_cred = self.client.login(**fake_credential)

        self.assertTrue(t_cred)
        self.assertFalse(f_cred)
