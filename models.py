# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Chuyendi(models.Model):
    matour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    ngaykhoihanh = models.DateField(db_column='NgayKhoiHanh')  # Field name made lowercase.
    ngayketthuc = models.DateField(db_column='NgayKetThuc', blank=True, null=True)  # Field name made lowercase.
    tonggia = models.FloatField(db_column='TongGia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chuyendi'
        unique_together = (('matour', 'ngaykhoihanh'),)


class Donvicungcapdichvuchuyen(models.Model):
    matour = models.OneToOneField('Lichtrinhchuyen', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    ngaykhoihanh = models.ForeignKey('Lichtrinhchuyen', models.DO_NOTHING, db_column='NgayKhoiHanh')  # Field name made lowercase.
    sttngay = models.ForeignKey('Lichtrinhchuyen', models.DO_NOTHING, db_column='STTNgay')  # Field name made lowercase.
    loai = models.IntegerField(db_column='Loai')  # Field name made lowercase.
    madonvi = models.IntegerField(db_column='MaDonVi', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donvicungcapdichvuchuyen'
        unique_together = (('matour', 'ngaykhoihanh', 'sttngay', 'loai'),)


class Donvicungcapdichvulienquan(models.Model):
    matour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    madiem = models.IntegerField(db_column='MaDiem')  # Field name made lowercase.
    madonvi = models.IntegerField(db_column='MaDonVi')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donvicungcapdichvulienquan'
        unique_together = (('matour', 'madiem', 'madonvi'),)


class Hanhdonglichtrinhtour(models.Model):
    matour = models.OneToOneField('Lichtrinhtour', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    sttngay = models.ForeignKey('Lichtrinhtour', models.DO_NOTHING, db_column='STTNgay')  # Field name made lowercase.
    loaihanhdong = models.IntegerField(db_column='LoaiHanhDong')  # Field name made lowercase.
    giobatdau = models.TimeField(db_column='GioBatDau', blank=True, null=True)  # Field name made lowercase.
    gioketthuc = models.TimeField(db_column='GioKetThuc', blank=True, null=True)  # Field name made lowercase.
    mota = models.CharField(db_column='MoTa', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hanhdonglichtrinhtour'
        unique_together = (('matour', 'sttngay', 'loaihanhdong'),)


class Huongdanviendanchuyendi(models.Model):
    matour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    ngaykhoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='NgayKhoiHanh')  # Field name made lowercase.
    mahdv = models.IntegerField(db_column='MaHDV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'huongdanviendanchuyendi'
        unique_together = (('matour', 'ngaykhoihanh'),)


class Lichtrinhchuyen(models.Model):
    matour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    ngaykhoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='NgayKhoiHanh')  # Field name made lowercase.
    sttngay = models.IntegerField(db_column='STTNgay')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lichtrinhchuyen'
        unique_together = (('matour', 'ngaykhoihanh', 'sttngay'),)


class Lichtrinhtour(models.Model):
    matour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    sttngay = models.IntegerField(db_column='STTNgay')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lichtrinhtour'
        unique_together = (('matour', 'sttngay'),)


class Ngaykhoihanhtourdaingay(models.Model):
    matour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    ngay = models.IntegerField(db_column='Ngay')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ngaykhoihanhtourdaingay'
        unique_together = (('matour', 'ngay'),)


class Tour(models.Model):
    matour = models.CharField(db_column='MaTour', primary_key=True, max_length=20)  # Field name made lowercase.
    tentour = models.CharField(db_column='TenTour', max_length=255)  # Field name made lowercase.
    anh = models.CharField(db_column='Anh', max_length=255)  # Field name made lowercase.
    ngaybatdau = models.DateField(db_column='NgayBatDau', blank=True, null=True)  # Field name made lowercase.
    sokhachtourtoithieu = models.IntegerField(db_column='SoKhachTourToiThieu')  # Field name made lowercase.
    sokhachtourtoida = models.IntegerField(db_column='SoKhachTourToiDa')  # Field name made lowercase.
    giavelenguoilon = models.FloatField(db_column='GiaVeLeNguoiLon')  # Field name made lowercase.
    giaveletreem = models.FloatField(db_column='GiaVeLeTreEm')  # Field name made lowercase.
    giavedoannguoilon = models.FloatField(db_column='GiaVeDoanNguoiLon')  # Field name made lowercase.
    giavedoantreem = models.FloatField(db_column='GiaVeDoanTreEm')  # Field name made lowercase.
    sokhachdoantoithieu = models.IntegerField(db_column='SoKhachDoanToiThieu', blank=True, null=True)  # Field name made lowercase.
    sodem = models.IntegerField(db_column='SoDem', blank=True, null=True)  # Field name made lowercase.
    songay = models.IntegerField(db_column='SoNgay', blank=True, null=True)  # Field name made lowercase.
    machinhanh = models.IntegerField(db_column='MaChiNhanh')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tour'


class Tourgomdiadiemthamquan(models.Model):
    matour = models.OneToOneField(Lichtrinhtour, models.DO_NOTHING, db_column='MaTour', primary_key=True)  # Field name made lowercase.
    sttngay = models.ForeignKey(Lichtrinhtour, models.DO_NOTHING, db_column='STTNgay')  # Field name made lowercase.
    madiemdulich = models.IntegerField(db_column='MaDiemDuLich')  # Field name made lowercase.
    thoigianbatdau = models.TimeField(db_column='ThoiGianBatDau', blank=True, null=True)  # Field name made lowercase.
    thoigianketthuc = models.TimeField(db_column='ThoiGianKetThuc', blank=True, null=True)  # Field name made lowercase.
    mota = models.CharField(db_column='MoTa', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tourgomdiadiemthamquan'
        unique_together = (('matour', 'sttngay', 'madiemdulich'),)
