from django.db import models

# Create your models here.
import datetime,random
from django.utils import timezone

class Ticket(models.Model):

       
    def __str__(self):
        return self.sn
    
    def generate_pwd():
        seeds = "1234567890abcdefghijkmnpqrstuvwxyz"
        return "".join(random.sample(seeds,6))
    
    def generate_sn():
        try:
            last_sn = Ticket.objects.order_by('-sn')[0].sn
            return '{:0>8d}'.format( int( last_sn ) + 1)            
        except:
            return '10000000'

    batch = models.PositiveIntegerField(default = 18001)
    sn = models.CharField(max_length=8, default=generate_sn, primary_key=True)
    #sn.short_description = '序列号'
    pwd = models.CharField(max_length=6,default=generate_pwd)
    product = models.PositiveSmallIntegerField(default = 1,choices =(
        (1,'玖玖红颜礼盒装900g'),
        (2,'玖玖红颜礼盒装1800g'),
        (3,'玖玖红颜普通装1300g'),
        )
                                               )
    actived = models.BooleanField(default = False)
    date_creat = models.DateField(auto_now_add = True)
    date_effective = models.DateField(default=datetime.date.today)
    date_expire = models.DateField()
    date_use = models.DateTimeField(blank=True, null=True)
    order_name = models.CharField(max_length = 16,blank=True, null=True)
    order_phone = models.CharField(max_length = 11,blank=True, null=True)
    order_address = models.TextField(blank=True, null=True)
    order_comments = models.CharField(max_length = 20,blank=True, null=True)
    order_completed = models.NullBooleanField(default = None,blank=True, null=True)
 
