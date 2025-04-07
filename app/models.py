from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class EmailSettings(models.Model):
    email_host = models.CharField(max_length=255, default='smtp.gmail.com')
    email_port = models.IntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.EmailField(default='mohmmedshaker69@gmail.com')
    email_host_password = models.CharField(default='qwjs resc ecdg bcxu', max_length=255)
    default_from_email = models.EmailField(default='mohmmedshaker69@gmail.com')

    class Meta:
        db_table = "shared_mail_setting"

    def save(self, *args, **kwargs):

        if self.pk is None and EmailSettings.objects.exists():
            raise ValidationError("Only one instance of EmailSettings can exist.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email_host_user
    

class EmailSettingsAuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    email_settings_id = models.IntegerField()  
    field_name = models.CharField(max_length=255) 
    old_value = models.TextField(null=True, blank=True)  
    new_value = models.TextField(null=True, blank=True)
    change_time = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-change_time']
        db_table = "shared_audit_mail_setting"


    def __str__(self):
        return f"Change in EmailSettings ID: {self.email_settings_id} by {self.user}"
    

class EmailGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    arabic_name = models.CharField(max_length=255, null=True, blank=True)
    emails = models.TextField(help_text="Comma-separated email addresses")
    notify = models.BooleanField(default=False)

    class Meta:
        db_table = "shared_mail_group"

    def __str__(self):
        return self.name
    
class EmailGroupAuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    object_id = models.IntegerField()  
    field_name = models.CharField(max_length=255)  
    old_value = models.TextField(null=True, blank=True)  
    new_value = models.TextField(null=True, blank=True)  
    change_time = models.DateTimeField(auto_now_add=True) 
    name = models.CharField(max_length=255, null=True, blank=True) 
    arabic_name = models.CharField(max_length=255, null=True, blank=True) 

    class Meta:
        ordering = ['-change_time']
        db_table = "shared_audit_mail_group"

    def __str__(self):
        return f"Change in EmailGroup (ID: {self.object_id}) by {self.user}"

class EmailMessage(models.Model):
    groups = models.ManyToManyField(EmailGroup, related_name='email_messages')  
    subject = models.CharField(max_length=255)
    text_message = models.TextField(blank=True, null=True)  
    attachment = models.FileField(upload_to='email_attachments/', blank=True, null=True)  
    photo = models.ImageField(upload_to='email_photos/', blank=True, null=True)  

    def __str__(self):
        return self.subject