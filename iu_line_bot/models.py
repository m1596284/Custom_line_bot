from django.db import models

# Create your models here.


class user_info_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)


class chat_log_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_mod_date = models.DateTimeField(auto_now=True, blank=False)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    chat_room = models.CharField(max_length=50)
    chat_text = models.TextField()


class iu_love_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)


class iu_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)


class yuyan_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)


class ccc_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)


class man_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    package = models.IntegerField()
    url = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, null=True)


class mm_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    package = models.IntegerField()
    url = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, null=True)


class oo_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    package = models.IntegerField()
    url = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, null=True)


class pp_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    package = models.IntegerField()
    url = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, null=True)


class cc_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    package = models.IntegerField()
    url = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, null=True)


class ngag_funny_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    article_id = models.CharField(max_length=200, null=True)
    article_title = models.CharField(max_length=200, null=True)
    article_type = models.CharField(max_length=200, null=True)


class ngag_girl_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    article_id = models.CharField(max_length=200, null=True)
    article_title = models.CharField(max_length=200, null=True)
    article_type = models.CharField(max_length=200, null=True)


class ngag_nsfw_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    article_id = models.CharField(max_length=200, null=True)
    article_title = models.CharField(max_length=200, null=True)
    article_type = models.CharField(max_length=200, null=True)


class pray_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    pray_text = models.TextField()


class hometown_day_info_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_info = models.TextField()


class hometown_info_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)
    shift = models.CharField(max_length=200)
    id_num = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    working = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    info = models.CharField(max_length=200)


class hometown_history_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_num = models.CharField(max_length=20)
    history = models.TextField()


class password_book(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.TextField()
    account = models.TextField()
    password = models.TextField()
    link = models.TextField()


class line_buy_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    shopId = models.IntegerField()
    point = models.FloatField()
    url = models.TextField()
    image_url = models.TextField()
    transfer_url = models.TextField()
