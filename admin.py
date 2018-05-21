from django.contrib import admin

# Register your models here.
from .models import Ticket, Notice
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['text', 'create']
    list_editable = ['text']
    list_display_links = None
    

def active_tickets(modeladmin, request, queryset):
    queryset.update(actived=True)
def deactive_tickets(modeladmin, request, queryset):
    queryset.update(actived=False)
def complete_order(modeladmin, request, queryset):
    queryset.update(order_completed=True)
  
active_tickets.short_description = "激活所选券"
deactive_tickets.short_description = "取消激活所选券"
complete_order.short_description = "完成所选订单"

class TiecketResource(resources.ModelResource):
        
    class Meta:
        model = Ticket
        import_id_fields = ('sn',)
        skip_unchanged = False
        fields = ('batch', 'sn', 'pwd', 'date_expire', 'product', 'order_name', 'order_phone', 'order_address', 'order_comments', 'order_completed')
        export_order = ('batch', 'sn', 'pwd', 'product', 'date_expire' , 'order_completed' , 'order_name', 'order_phone', 'order_address', 'order_comments')
    
class TicketAdmin(ImportExportActionModelAdmin):
    resource_class = TiecketResource
    search_fields = ['batch','sn','order_name','order_phone']
    fields = (
        ('batch', 'sn', 'pwd'),
        ('actived', 'date_effective', 'date_expire'),
        ('date_use'),
        ('order_name', 'order_phone', 'product'),
        ('order_completed', 'order_comments'),
        'order_address'
        )
        
    list_filter = ['date_use', 'batch', 'actived', 'order_completed', 'date_creat']
    list_display = ['batch', 'sn', 'actived', 'date_use', 'order_name']
    list_display_links = ['sn', 'order_name']
    actions = [active_tickets, deactive_tickets, complete_order]
    date_hierarchy = 'date_creat'
    
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Ticket, TicketAdmin)
