from apps.wallet.models import Wallet, Transaction
from django.db import transaction
from apps.users.models import User


class WalletCore:

    @staticmethod
    def increase_balance(user:User, pk:str, amount:float):
        if amount <= 0:
            return False, "Invalid amount"
        
        try:
            wallet = Wallet.objects.get(id=pk)
        except Exception as e:
            return False, str(e)

        with transaction.atomic():
            wallet.balance += amount
            wallet.save()
            

            trans = Transaction.objects.create(
                user = user,
                from_wallet = wallet,
                to_wallet = wallet,
                action = 'charge', 
                amount = amount
            )

        return True, wallet.balance
    
    @staticmethod
    def decrease_balance(user:User, pk:str, amount:float):
        if amount <= 0:
            return False, "Invalid amount"
        
        try:
            wallet = Wallet.objects.get(id=pk)
        except Exception as e:
            return False, str(e)

        if wallet.balance < amount:
            return False, "Insufficient Balance"
        
        with transaction.atomic():
            wallet.balance -= amount
            wallet.save()
            
            trans = Transaction.objects.create(
                user = user,
                from_wallet = wallet,
                to_wallet = wallet,
                action = 'spend', 
                amount = amount
            )
        
        return True, wallet.balance
    
    @staticmethod
    def transaction(user:User, from_pk:str, to_pk:str, amount: float):
        if amount <= 0:
            return False, "Invalid amount"
        
        try:
            from_wallet = Wallet.objects.get(id=from_pk)
            to_wallet = Wallet.objects.get(id=to_pk)
        except Exception as e:
            return False, str(e)

        if from_wallet.balance < amount:
            return False, "Insufficient Balance"
        
        with transaction.atomic():
            from_wallet.balance -= amount
            to_wallet.balance += amount

            from_wallet.save()
            to_wallet.save()

            trans = Transaction.objects.create(
                user = user,
                from_wallet = from_wallet,
                to_wallet = to_wallet,
                action = 'exchange', 
                amount = amount
            )
        
        return True, (from_wallet.balance, to_wallet.balance)

