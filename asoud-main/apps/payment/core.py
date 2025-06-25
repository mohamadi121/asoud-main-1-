import requests, os
from uuid import UUID
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.payment.models import Payment, Zarinpal
from apps.advertise.models import Advertisement
from apps.wallet.models import Wallet
from apps.wallet.core import WalletCore
from apps.cart.models import Order

class PaymentCore:
    def pay(self, user, data):
        
        model = None
        match data.get('target'):
            
            case "advertisement":
                model = Advertisement
            case "wallet":
                model = Wallet
            case "order":
                model = Order
            case "market":
                model = Market

            case _:
                return False, "Incorrect taget Value"

        try:

            target_content_type = ContentType.objects.get_for_model(model)
            gateway_content_type = ContentType.objects.get_for_model(Zarinpal)

            payment = Payment.objects.create(
                user = user,
                amount = data['amount'],
                target_content_type = target_content_type,
                target_id = UUID(data['target_id']),
                gateway_content_type = gateway_content_type,
                status = Payment.PENDING
            )

            zarinpal = Zarinpal.objects.create(
                payment=payment,  
                authority=''
            )

            payment.gateway_id = zarinpal.id
            payment.save()

        except:
            return False, 'Payment Creation Failed'

        data = {
            'merchant_id': os.environ.get("ZARINPAL_MERCHANT_ID"),
            'amount': int(payment.amount),
            'currency': 'IRT',
            'description': 'text',
            'callback_url': ["http://asoud.ir/api/v1/user/payments/verify/",'https://google.com'][0], 
            'meta_data': {'payment': str(payment.id)}
        }

        url = f'https://{settings.ZARINPAL_URL}.zarinpal.com/pg/v4/payment/request.json'
        response = requests.post(url=url, json=data)

        jsonRes = response.json()
        try:
            authority = jsonRes['data']['authority']
        except:
            return False, 'an error occured during connecting to zarinpal'
        
        # update zarinpal instance
        zarinpal.payment=payment
        zarinpal.authority=authority
        zarinpal.save()

        return True, zarinpal
    
    def verify(self, request):
        try:
            authority = request.GET.get('Authority')
            stat = request.GET.get('Status')
        except:
            return False, 'no data is provided'
        
        if stat == "NOK":
            return False, 'status not OK'

        try:
            zarin = Zarinpal.objects.get(authority=authority)
        except:
            return False, 'no payment found'

        if zarin.transaction_id:
            return False, 'already validated'
        
        if zarin.payment.status != Payment.PENDING:
            return False, 'Payment already processed'
        
        data = {
            'merchant_id': os.environ.get("ZARINPAL_MERCHANT_ID"),
            'amount': int(zarin.payment.amount),
            'authority': authority,
        }

        url = f'https://{settings.ZARINPAL_URL}.zarinpal.com/pg/v4/payment/verify.json'
        response = requests.post(url=url, json=data)
        jsonRes = response.json()

        with transaction.atomic():
            try:
                print(jsonRes['data'])
                code = jsonRes['data']['code']
                ref_id = jsonRes['data']['ref_id']
            except:
                zarin.payment.status = Payment.FAILED
                zarin.payment.save()
                return False, "Verification Failed From Gateway"
            
            if code != 100:
                zarin.payment.status = Payment.FAILED
                zarin.payment.save()
                return False, "Verification Failed"
                
            # go for post payment processes
            post_payment = PostPaymentCore(zarin.payment.user)
            try:
                post_payment.payment_process(zarin.payment)
            except Exception as e:
                return False, str(e)
            
            # save ref_id to transaction_id
            zarin.transaction_id = ref_id
            zarin.verification_data = jsonRes
            zarin.save()

            zarin.payment.status = Payment.COMPLETE
            zarin.payment.save()

        return True, "Payment Successfull"
    

class PostPaymentCore:
    def __init__(self, user):
        self.user = user

    def payment_process(self, payment: Payment):
        target_model = payment.target_content_type.model_class()

        if target_model == Advertisement:
            self.update_advertisement(
                payment.target_id
            )
        
        elif target_model == Wallet:
            self.create_wallet_transaction(
                payment.target_id,
                payment.amount
            )

        elif target_model == Market:
            self.update_market(
                payment.target_id
            )

        else :
                self.complete_order(
                    payment.target_id
                )    

    def wallet_process(self, target:str, pk:str, amount:float = None, wallet_id:str = None):
        if target == 'advertisement':
            self.update_advertisement(
                pk
            )
            WalletCore.decrease_balance(
                self.user, 
                wallet_id,
                amount
            )

        elif target == 'wallet':
            WalletCore.transaction(
                self.user, 
                wallet_id,
                pk,
                amount
            )
        
        else :
            self.complete_order(
                pk
            )
            WalletCore.decrease_balance(
                self.user, 
                wallet_id,
                amount
            )


    def update_advertisement(self, pk:str):
        ad = Advertisement.objects.get(id=pk)
        
        ad.is_paid = True
        ad.save()

    def create_wallet_transaction(self, pk:str, amount: float):
        success, data = WalletCore.increase_balance(self.user, pk, amount)
        if not success:
            raise Exception(data)

    def update_market(self, target_id):
        obj = Market.objects.get(id=target_id)
        obj.status = 'queue'
        obj.is_paid = True
        obj.save()

    def complete_order(self, pk:str):
        order = Order.objects.get(id=pk)
        order.status = Order.COMPLETED
        order.is_paid = True
        order.save()

