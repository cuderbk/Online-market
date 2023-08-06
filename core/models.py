from django.db import models
from django.db.models import ForeignKey

# Create your models here.
class KhachDoan(models.Model):
    ma_doan = models.CharField(primary_key=True, max_length=6)
    ten_coquan = models.CharField(max_length=40)
    email = models.CharField(max_length=60, blank=True, null=True)
    sdt = models.CharField(max_length=10, blank=True, null=True)
    dia_chi = models.CharField(max_length=100)
    ma_daidien = models.ForeignKey('KhachHang', models.DO_NOTHING, db_column='ma_daidien')

    class Meta:
        managed = False
        db_table = 'khach_doan'


class KhachHang(models.Model):
    ma_kh = models.CharField(primary_key=True, max_length=6)
    cmnd = models.CharField(max_length=12, blank=True, null=True)
    ho_ten = models.CharField(max_length=60)
    email = models.CharField(max_length=60, blank=True, null=True)
    sdt = models.CharField(max_length=10, blank=True, null=True)
    ngay_sinh = models.DateField(blank=True, null=True)
    dia_chi = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'khach_hang'


class KhackDoanLe(models.Model):
    ma_doan = models.OneToOneField(KhachDoan, models.DO_NOTHING, db_column='ma_doan', primary_key=True)
    ma_kh = models.ForeignKey(KhachHang, models.DO_NOTHING, db_column='ma_kh')

    class Meta:
        managed = False
        db_table = 'khack_doan_le'
        unique_together = (('ma_doan', 'ma_kh'),)

class NgoaiNgu(models.Model):
    ma_nv = models.OneToOneField('NhanVien', models.DO_NOTHING, db_column='ma_nv', primary_key=True)
    ngoai_ngu = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ngoai_ngu'
        unique_together = (('ma_nv', 'ngoai_ngu'),)

class KyNang(models.Model):
    ma_nv = models.OneToOneField('NhanVien', models.DO_NOTHING, db_column='ma_nv', primary_key=True)
    ky_nang = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ky_nang'
        unique_together = (('ma_nv', 'ky_nang'),)

class NhanVien(models.Model):
    ma_nv = models.CharField(primary_key=True, max_length=6)
    cmnd = models.CharField(unique=True, max_length=12)
    ho_ten = models.CharField(max_length=60)
    dia_chi = models.CharField(max_length=100, blank=True, null=True)
    gioi_tinh = models.CharField(max_length=1, blank=True, null=True)
    ngay_sinh = models.DateField(blank=True, null=True)
    cong_viec = models.CharField(max_length=2, blank=True, null=True)
    vi_tri = models.CharField(max_length=30, blank=True, null=True)
    ma_cn = models.ForeignKey('tour.ChiNhanh', models.DO_NOTHING, db_column='ma_cn', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nhan_vien'
        
class Phieudk(models.Model):
    ma_phieu = models.CharField(primary_key=True, max_length=8)
    ngay_dangky = models.DateField()
    ghichu = models.TextField(blank=True, null=True)
    ma_nv = models.ForeignKey(NhanVien, models.DO_NOTHING, db_column='ma_nv')
    ma_doan = models.ForeignKey(KhachDoan, models.DO_NOTHING, db_column='ma_doan', blank=True, null=True)
    ma_kh = models.ForeignKey(KhachHang, models.DO_NOTHING, db_column='ma_kh', blank=True, null=True)
    ma_tour = models.ForeignKey('tour.Chuyendi', models.DO_NOTHING, db_column='ma_tour', related_name='phieudk_ma_tour')
    ngay_khoihanh = models.ForeignKey('tour.Chuyendi', models.DO_NOTHING, db_column='ngay_khoihanh', related_name= 'phieudk_ngay_khoihanh')

    class Meta:
        managed = False
        db_table = 'phieudk'
