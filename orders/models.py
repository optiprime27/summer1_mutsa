from django.db import models
from members.models import Member
from items.models import Item

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('주문성공', '주문_성공'),
        ('주문취소', '주문_취소'),
    ]
    order_date = models.DateTimeField(auto_now_add=True) 
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='Order_Item')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='주문성공')

    class Meta:
        db_table = 'orders'

class Order_Item(models.Model):
    count = models.IntegerField(default=0)
    order_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_item'
