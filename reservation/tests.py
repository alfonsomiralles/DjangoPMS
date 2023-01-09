from django.test import TestCase
from .views import process_payment

class PaymentTestCase(TestCase):

    def test_process_payment_at_hotel(self):
        # Testear el caso en el que el pago se realiza en el hotel
        payment_method = "at_hotel"
        payment_details = "Pago en efectivo al llegar al hotel"
        result = process_payment(payment_method, payment_details)
        self.assertEqual(result, "Pago Pendiente")
    
    def test_process_payment_other_method(self):
        # Testear el caso en el que el pago se realiza con otro método
        payment_method = "other"
        payment_details = "Tarjeta de crédito"
        result = process_payment(payment_method, payment_details)
        self.assertEqual(result, "Pagado")
