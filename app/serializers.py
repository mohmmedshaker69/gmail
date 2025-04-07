from django.db.models import Max
from django.utils.timezone import timedelta
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.conf import settings  
from datetime import datetime, date
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from django.contrib.auth.models import User

from . models import EmailMessage, EmailGroup, EmailGroupAuditLog, EmailSettings, EmailSettingsAuditLog


class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = '__all__'

class EmailSettingsAuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    class Meta:
        model = EmailSettingsAuditLog
        fields = '__all__'



class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = ['groups', 'subject', 'text_message', 'attachment', 'photo']

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        email_message = EmailMessage.objects.create(**validated_data)
        email_message.groups.set(groups)
        return email_message

    def send_email(self):
        email_data = self.validated_data
        groups = email_data['groups']
        
        # Collect unique recipients from groups
        recipients = []
        for group in groups:
            group_recipients = [email.strip() for email in group.emails.split(',')]
            recipients.extend(group_recipients)
        recipients = list(set(recipients))  # Remove duplicates

        sender_email = settings.EMAIL_HOST_USER
        body_content = email_data.get('text_message', '')

        # Send individual emails to each recipient
        for recipient in recipients:
            email_message = DjangoEmailMessage(
                subject=email_data['subject'],
                body=body_content,
                from_email=sender_email,
                to=[recipient]  # Single recipient in 'to'
            )

            # Attach files if they exist
            if self.instance.attachment:
                email_message.attach_file(self.instance.attachment.path)
            if self.instance.photo:
                email_message.attach_file(self.instance.photo.path)

            # Send the email
            email_message.send(fail_silently=False)

class EmailGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailGroup
        fields = '__all__'

class EmailGroupAuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True) 
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = EmailGroupAuditLog
        fields = '__all__'