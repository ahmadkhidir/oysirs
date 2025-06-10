from django.db import models


class Bank(models.Model):
    """
    Bank model class
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
        ordering = ['name']


class Customer(models.Model):
    """
    Customer model class
    """
    def __str__(self):
        return f"CUST-{self.id}"

    def bvn(self):
        return self.bvns.first().bvn if self.bvns.exists() else None
    
    def nuban(self):
        return self.nubans.first().nuban if self.nubans.exists() else None

    def email(self):
        return self.emails.first().email if self.emails.exists() else None
    
    def mobile(self):
        return self.mobiles.first().mobile if self.mobiles.exists() else None
    
    def tin(self):
        return self.tins.first().tin if self.tins.exists() else None
    
    def name(self):
        return self.names.first().name if self.names.exists() else None


class CustomerName(models.Model):
    """
    CustomerName model class
    """
    name = models.CharField(max_length=255, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='names', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'customer'], name='unique_name_customer')
        ]


class CustomerAddress(models.Model):
    """
    CustomerAddress model class
    """
    address = models.TextField()
    customer = models.ForeignKey(
        Customer, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return self.address
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address', 'customer'], name='unique_address_customer')
        ]


class CustomerNUBAN(models.Model):
    """
    CustomerNUBAN model class
    """
    nuban = models.CharField(max_length=10, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='nubans', on_delete=models.CASCADE)

    def __str__(self):
        return self.nuban
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nuban', 'customer'], name='unique_nuban_customer')
        ]


class CustomerMobile(models.Model):
    """
    CustomerMobile model class
    """
    mobile = models.CharField(max_length=15, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='mobiles', on_delete=models.CASCADE)

    def __str__(self):
        return self.mobile
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mobile', 'customer'], name='unique_mobile_customer')
        ]


class CustomerBVN(models.Model):
    """
    CustomerBVN model class
    """
    bvn = models.CharField(max_length=11, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='bvns', on_delete=models.CASCADE)

    def __str__(self):
        return self.bvn
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bvn', 'customer'], name='unique_bvn_customer')
        ]


class CustomerEmail(models.Model):
    """
    CustomerEmail model class
    """
    email = models.EmailField(db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='emails', on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'customer'], name='unique_email_customer')
        ]


class CustomerTIN(models.Model):
    """
    CustomerTIN model class
    """
    tin = models.CharField(max_length=15, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='tins', on_delete=models.CASCADE)

    def __str__(self):
        return self.tin
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tin', 'customer'], name='unique_tin_customer')
        ]


class CustomerPassport(models.Model):
    """
    CustomerPassport model class
    """
    passport = models.CharField(max_length=20, db_index=True)
    customer = models.ForeignKey(
        Customer, related_name='passports', on_delete=models.CASCADE)

    def __str__(self):
        return self.passport
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['passport', 'customer'], name='unique_passport_customer')
        ]


class BankTransaction(models.Model):
    """
    BankTransaction model class
    """
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(
        max_length=6, choices=TRANSACTION_TYPE_CHOICES, default=None, null=True, blank=True)
    narration = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    bank = models.ForeignKey(
        Bank, related_name='transactions', on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, related_name='transactions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"

    class Meta:
        verbose_name = "Bank Transaction"
        verbose_name_plural = "Bank Transactions"
        ordering = ['-date']
