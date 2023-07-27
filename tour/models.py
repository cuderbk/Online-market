from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

# class Item(models.Model):
#     category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price = models.FloatField()
#     image = models.ImageField(upload_to='item_images')
#     is_sold = models.BooleanField(default=False)
#     created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
from django.contrib.auth.models import User
from django.db import models

from django.db import models

class Tour(models.Model):
    
    MaTour = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    Anh = models.CharField(max_length=255)
    NgayBatDau = models.DateField(blank=True, null=True)
    SoKhachTourToiThieu = models.IntegerField()
    SoKhachTourToiDa = models.IntegerField()
    GiaVeLeNguoiLon = models.FloatField()
    GiaVeLeTreEm = models.FloatField()
    GiaVeDoanNguoiLon = models.FloatField()
    GiaVeDoanTreEm = models.FloatField()
    SoKhachDoanToiThieu = models.IntegerField(blank=True, null=True)
    SoDem = models.IntegerField(blank=True, null=True)
    SoNgay = models.IntegerField(blank=True, null=True)
    MaChiNhanh = models.IntegerField()

    # Additional Fields
    category = models.ForeignKey(Category, related_name='tours', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='tour_images')
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='tours', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tour'  # The name of the existing table in the database

    def __str__(self):
        return self.name


