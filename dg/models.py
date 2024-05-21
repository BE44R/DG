"""This module describes models"""
from django.db import models
import os
from PIL import Image




class Chat(models.Model):
    """This is Chat model"""
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()


class GlobalChat(models.Model):
    """This is GlobalChat model"""
    sender_username = models.CharField(max_length=1000)
    text = models.CharField(max_length=2500)
    time = models.TimeField()


class MessageFile(models.Model):
    """This is files attached to global chat model"""
    file = models.FileField(upload_to="global_chat", blank=True, null=True, default=None)
    name = models.CharField(max_length=50, null=True, blank=True, default=None)
    size = models.IntegerField(null=True, blank=True, default=None)
    message = models.ForeignKey(GlobalChat, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                related_name='files')

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def is_image(self):
        extension = self.extension()
        if extension in ['.jpg', '.jpeg', '.png']:
            return True
        return False


class Message(models.Model):
    """This is Message model"""
    text = models.CharField(max_length=500)
    chat_id = models.IntegerField()
    sender_id = models.IntegerField()
    time = models.DateTimeField()


class MessageFileDirect(models.Model):
    """This is files attached to direct chat model"""
    file = models.FileField(upload_to="direct_chat", blank=True, null=True, default=None)
    name = models.CharField(max_length=50, null=True, blank=True, default=None)
    size = models.IntegerField(null=True, blank=True, default=None)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                related_name='files')

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def is_image(self):
        extension = self.extension()
        if extension in ['.jpg', '.jpeg', '.png']:
            return True
        return False


class UserBalance(models.Model):
    """This is Balance model"""
    user_id = models.IntegerField()
    money = models.IntegerField()


class ShopKeys(models.Model):
    """This is keys model"""
    key = models.CharField(max_length=100)
    money = models.IntegerField()
    status = models.IntegerField()
