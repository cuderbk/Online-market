# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ChiNhanh(models.Model):
    ma_cn = models.CharField(primary_key=True, max_length=8)
    ten_cn = models.CharField(unique=True, max_length=40)
    khu_vuc = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    fax = models.CharField(max_length=11, blank=True, null=True)
    ma_nvql = models.ForeignKey('NhanVien', models.DO_NOTHING, db_column='ma_nvql', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chi_nhanh'


class Chuyendi(models.Model):
    ma_tour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.DateField()
    ngay_ketthuc = models.DateField(blank=True, null=True)
    tonggia = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chuyendi'
        unique_together = (('ma_tour', 'ngay_khoihanh'),)


class DiadiemThamquan(models.Model):
    ma_tour = models.OneToOneField('Lichtrinhtour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    stt_ngay = models.ForeignKey('Lichtrinhtour', models.DO_NOTHING, db_column='stt_ngay')
    ma_diem = models.ForeignKey('DiemDulich', models.DO_NOTHING, db_column='ma_diem')
    thoigian_batdau = models.DateField(blank=True, null=True)
    thoigian_ketthuc = models.DateField(blank=True, null=True)
    mo_ta = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diadiem_thamquan'
        unique_together = (('ma_tour', 'stt_ngay', 'ma_diem'),)


class DiemDulich(models.Model):
    ma_diem = models.AutoField(primary_key=True)
    ten_diem = models.CharField(max_length=30)
    dia_chi = models.CharField(max_length=100)
    phuong_xa = models.CharField(max_length=20)
    quan_huyen = models.CharField(max_length=20)
    tinh = models.CharField(max_length=20)
    anh1 = models.CharField(max_length=200, blank=True, null=True)
    anh2 = models.CharField(max_length=200, blank=True, null=True)
    anh3 = models.CharField(max_length=200, blank=True, null=True)
    mo_ta = models.CharField(max_length=500, blank=True, null=True)
    ghi_chu = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diem_dulich'


class DonviCungcap(models.Model):
    ma_donvi = models.CharField(primary_key=True, max_length=6)
    ten_donvi = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    sdt_dvcc = models.CharField(max_length=10, blank=True, null=True)
    ten_nguoidaidien = models.CharField(max_length=60, blank=True, null=True)
    sdt_nguoidaidien = models.CharField(max_length=10, blank=True, null=True)
    dia_chi = models.CharField(max_length=100)
    phuong_xa = models.CharField(max_length=20)
    quan_huyen = models.CharField(max_length=20)
    tinh = models.CharField(max_length=20)
    anh1 = models.CharField(max_length=200, blank=True, null=True)
    anh2 = models.CharField(max_length=200, blank=True, null=True)
    anh3 = models.CharField(max_length=200, blank=True, null=True)
    anh4 = models.CharField(max_length=200, blank=True, null=True)
    anh5 = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donvi_cungcap'


class DvccDvchuyendi(models.Model):
    ma_tour = models.OneToOneField('LichtrinhChuyen', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.ForeignKey('LichtrinhChuyen', models.DO_NOTHING, db_column='ngay_khoihanh')
    stt_ngay = models.ForeignKey('LichtrinhChuyen', models.DO_NOTHING, db_column='stt_ngay')
    loai = models.IntegerField()
    ma_donvi = models.ForeignKey(DonviCungcap, models.DO_NOTHING, db_column='ma_donvi')

    class Meta:
        managed = False
        db_table = 'dvcc_dvchuyendi'
        unique_together = (('ma_tour', 'ngay_khoihanh', 'stt_ngay', 'loai', 'ma_donvi'),)


class DvccDvlq(models.Model):
    ma_tour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ma_diem = models.ForeignKey(DiemDulich, models.DO_NOTHING, db_column='ma_diem')
    ma_donvi = models.ForeignKey(DonviCungcap, models.DO_NOTHING, db_column='ma_donvi')

    class Meta:
        managed = False
        db_table = 'dvcc_dvlq'
        unique_together = (('ma_tour', 'ma_diem', 'ma_donvi'),)


class HanhdongLichtrinhtour(models.Model):
    ma_tour = models.OneToOneField('Lichtrinhtour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    stt_ngay = models.ForeignKey('Lichtrinhtour', models.DO_NOTHING, db_column='stt_ngay')
    loai_hanhdong = models.IntegerField()
    thoigian_batdau = models.DateField(blank=True, null=True)
    thoigian_ketthuc = models.DateField(blank=True, null=True)
    mo_ta = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hanhdong_lichtrinhtour'
        unique_together = (('ma_tour', 'stt_ngay', 'loai_hanhdong'),)


class HdvChuyendi(models.Model):
    ma_tour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ngay_khoihanh')
    ma_hdv = models.ForeignKey('NhanVien', models.DO_NOTHING, db_column='ma_hdv')

    class Meta:
        managed = False
        db_table = 'hdv_chuyendi'
        unique_together = (('ma_tour', 'ngay_khoihanh', 'ma_hdv'),)


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


class KyNang(models.Model):
    ma_nv = models.OneToOneField('NhanVien', models.DO_NOTHING, db_column='ma_nv', primary_key=True)
    ky_nang = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ky_nang'
        unique_together = (('ma_nv', 'ky_nang'),)


class LichtrinhChuyen(models.Model):
    ma_tour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ngay_khoihanh')
    stt_ngay = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lichtrinh_chuyen'
        unique_together = (('ma_tour', 'ngay_khoihanh', 'stt_ngay'),)


class Lichtrinhtour(models.Model):
    ma_tour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    stt_ngay = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lichtrinhtour'
        unique_together = (('ma_tour', 'stt_ngay'),)


class NgaykhoihanhTourdai(models.Model):
    ma_tour = models.OneToOneField('Tour', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ngaykhoihanh_tourdai'
        unique_together = (('ma_tour', 'ngay'),)


class NgoaiNgu(models.Model):
    ma_nv = models.OneToOneField('NhanVien', models.DO_NOTHING, db_column='ma_nv', primary_key=True)
    ngoai_ngu = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ngoai_ngu'
        unique_together = (('ma_nv', 'ngoai_ngu'),)


class NhanVien(models.Model):
    ma_nv = models.CharField(primary_key=True, max_length=6)
    cmnd = models.CharField(unique=True, max_length=12)
    ho_ten = models.CharField(max_length=60)
    dia_chi = models.CharField(max_length=100, blank=True, null=True)
    gioi_tinh = models.CharField(max_length=1, blank=True, null=True)
    ngay_sinh = models.DateField(blank=True, null=True)
    cong_viec = models.CharField(max_length=2)
    vi_tri = models.CharField(max_length=30, blank=True, null=True)
    ma_cn = models.ForeignKey(ChiNhanh, models.DO_NOTHING, db_column='ma_cn', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nhan_vien'


class Phieudk(models.Model):
    ma_phieu = models.CharField(primary_key=True, max_length=8)
    ngay_dangky = models.DateField()
    ghichu = models.CharField(max_length=200, blank=True, null=True)
    ma_nv = models.ForeignKey(NhanVien, models.DO_NOTHING, db_column='ma_nv')
    ma_doan = models.ForeignKey(KhachDoan, models.DO_NOTHING, db_column='ma_doan', blank=True, null=True)
    ma_kh = models.ForeignKey(KhachHang, models.DO_NOTHING, db_column='ma_kh', blank=True, null=True)
    ma_tour = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ma_tour')
    ngay_khoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ngay_khoihanh')

    class Meta:
        managed = False
        db_table = 'phieudk'


class SoDienThoaiChiNhanh(models.Model):
    ma_cn = models.OneToOneField(ChiNhanh, models.DO_NOTHING, db_column='ma_cn', primary_key=True)
    sdt_cn = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'so_dien_thoai_chi_nhanh'
        unique_together = (('ma_cn', 'sdt_cn'),)


class Tour(models.Model):
    ma_tour = models.CharField(primary_key=True, max_length=10)
    ten_tour = models.CharField(unique=True, max_length=40)
    anh = models.CharField(max_length=200, blank=True, null=True)
    ngay_batdau = models.DateField()
    sokhach_toida = models.IntegerField()
    giave_kl_nguoilon = models.IntegerField()
    giave_kl_treem = models.IntegerField()
    giave_kd_nguoilon = models.IntegerField()
    giave_kd_treem = models.IntegerField()
    sokhach_toithieu = models.IntegerField()
    so_dem = models.IntegerField()
    so_ngay = models.IntegerField()
    ma_cn = models.ForeignKey(ChiNhanh, models.DO_NOTHING, db_column='ma_cn')

    class Meta:
        managed = False
        db_table = 'tour'
