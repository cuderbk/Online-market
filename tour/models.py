from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.models import NhanVien

# Signal to generate ma_tour before saving the Tour object
class Category(models.TextChoices):
    TRONGNGAY ='TN','Tour trong ngày'
    DAINGAY ='DN','Tour dài ngày'
# class Category(models.Model):
#     name = models.CharField(max_length=255)

#     class Meta:
#         ordering = ('name',)
#         verbose_name_plural = 'Categories'
    
#     def __str__(self):
#         return self.name

class Status(models.TextChoices):
    PENDING = 'PEN', 'Pending'
    AVAILABLE='AVAIL','Available'
    ON_HOLD = 'HLD', 'On Hold'

class ChiNhanh(models.Model):
    ma_cn = models.CharField(primary_key=True, max_length=8)
    ten_cn = models.CharField(unique=True, max_length=40)
    khu_vuc = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    fax = models.CharField(max_length=11, blank=True, null=True)
    ma_nvql = models.ForeignKey('core.NhanVien', on_delete=models.SET_NULL, null=True, db_column='ma_nvql')

    class Meta:
        managed = False
        db_table = 'chi_nhanh'

    def __str__(self):
        # self.ma_nvql = NhanVien.objects.filter(pk = self.ma_nvql)
        # ChiNhanh.ma_nvql.save()
        return self.ten_cn


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
    ma_tour = models.OneToOneField('Lichtrinhtour', models.DO_NOTHING, db_column='ma_tour', primary_key=True, related_name='diadiem_thamquan_ma_tour')
    stt_ngay = models.ForeignKey('Lichtrinhtour', models.DO_NOTHING, db_column='stt_ngay', related_name='diadiem_thamquan_stt_ngay')
    ma_diem = models.ForeignKey('DiemDulich', models.DO_NOTHING, db_column='ma_diem')
    thoigian_batdau = models.DateField(blank=True, null=True)
    thoigian_ketthuc = models.DateField(blank=True, null=True)
    mo_ta = models.TextField(blank=True, null=True)

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
    anh1 = models.TextField(blank=True, null=True)
    anh2 = models.TextField(blank=True, null=True)
    anh3 = models.TextField(blank=True, null=True)
    mo_ta = models.TextField(blank=True, null=True)
    ghi_chu = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diem_dulich'
    def __str__(self):
        return self.ten_diem

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
    anh1 = models.TextField(blank=True, null=True)
    anh2 = models.TextField(blank=True, null=True)
    anh3 = models.TextField(blank=True, null=True)
    anh4 = models.TextField(blank=True, null=True)
    anh5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donvi_cungcap'



class DvccDvchuyendi(models.Model):
    ma_tour = models.OneToOneField('LichtrinhChuyen', models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.ForeignKey('LichtrinhChuyen', models.DO_NOTHING, db_column='ngay_khoihanh', related_name='dvcc_dvchuyendi_ngay_khoihanh')
    stt_ngay = models.ForeignKey('LichtrinhChuyen', models.DO_NOTHING, db_column='stt_ngay', related_name='dvcc_dvchuyendi_stt_ngay')
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
    ma_tour = models.OneToOneField('Lichtrinhtour', models.DO_NOTHING, db_column='ma_tour', primary_key=True, related_name='hanhdong_lichtrinhtour_ma_tour')
    stt_ngay = models.ForeignKey('Lichtrinhtour', models.DO_NOTHING, db_column='stt_ngay', related_name='hanhdong_lichtrinhtour_stt_ngay')
    loai_hanhdong = models.IntegerField()
    thoigian_batdau = models.DateField(blank=True, null=True)
    thoigian_ketthuc = models.DateField(blank=True, null=True)
    mo_ta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hanhdong_lichtrinhtour'
        unique_together = (('ma_tour', 'stt_ngay', 'loai_hanhdong'),)


class HdvChuyendi(models.Model):
    ma_tour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='ma_tour', primary_key=True, related_name='hdvchuyendi_ma_tour')
    ngay_khoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ngay_khoihanh', related_name='hdvchuyendi_ngay_khoihanh')
    ma_hdv = models.ForeignKey('core.Nhanvien', models.DO_NOTHING, db_column='ma_hdv')

    class Meta:
        managed = False
        db_table = 'hdv_chuyendi'
        unique_together = (('ma_tour', 'ngay_khoihanh', 'ma_hdv'),)


class LichtrinhChuyen(models.Model):
    ma_tour = models.OneToOneField(Chuyendi, models.DO_NOTHING, db_column='ma_tour', primary_key=True)
    ngay_khoihanh = models.ForeignKey(Chuyendi, models.DO_NOTHING, db_column='ngay_khoihanh', related_name='lichtrinhchuyen_ngay_khoihanh')
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





class SoDienThoaiChiNhanh(models.Model):
    ma_cn = models.OneToOneField(ChiNhanh, models.DO_NOTHING, db_column='ma_cn', primary_key=True)
    sdt_cn = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'so_dien_thoai_chi_nhanh'
        unique_together = (('ma_cn', 'sdt_cn'),)


# Signal to generate ma_tour before saving the Tour object
# Signal to generate ma_tour before saving the Tour object
def increment_tour_pk():
    last_tour = Tour.objects.all().order_by('ma_tour').last()

    if not last_tour:
        return 'CN1' + '000001'

    # help_id = last_tour.help_num
    # help_int = help_id[13:17]
    # new_help_int = int(help_int) + 1
    new_help_id = 'CN1' + '000002'

    return new_help_id

class Tour(models.Model):
    ma_tour = models.CharField(primary_key=True, max_length=12)
    ten_tour = models.CharField(max_length=40, unique = True)
    anh = models.TextField(blank=True, null=True, max_length=200)
    ngay_batdau = models.DateField()
    sokhach_toida = models.IntegerField()
    giave_kl_nguoilon = models.IntegerField()
    giave_kl_treem = models.IntegerField()
    giave_kd_nguoilon = models.IntegerField()
    giave_kd_treem = models.IntegerField()
    sokhach_toithieu = models.IntegerField()
    sokhachdoan_toithieu = models.IntegerField(blank=True, null=True)
    so_dem = models.IntegerField()
    so_ngay = models.IntegerField()
    ma_cn = models.ForeignKey(ChiNhanh, models.DO_NOTHING, db_column='ma_cn')

    class Meta:
        managed = False
        db_table = 'tour'

    def __str__(self):
        return self.ten_tour

class City(models.TextChoices):
    AN_GIANG = 'AG', 'An Giang'
    BA_RIA_VUNG_TAU = 'BRVT', 'Ba Ria - Vung Tau'
    BAC_LIEU = 'BL', 'Bac Lieu'
    BAC_KAN = 'BK', 'Bac Kan'
    BAC_GIANG = 'BG', 'Bac Giang'
    BAC_NINH = 'BN', 'Bac Ninh'
    BEN_TRE = 'BT', 'Ben Tre'
    BINH_DUONG = 'BD', 'Binh Duong'
    BINH_DINH = 'BĐ', 'Binh Dinh'
    BINH_PHUOC = 'BP', 'Binh Phuoc'
    BINH_THUAN = 'BTH', 'Binh Thuan'
    CA_MAU = 'CM', 'Ca Mau'
    CAO_BANG = 'CB', 'Cao Bang'
    CAN_THO = 'CT', 'Can Tho'
    DA_NANG = 'DNG', 'Da Nang'
    DAK_LAK = 'DL', 'Dak Lak'
    DAK_NONG = 'DKN', 'Dak Nong'
    DIEN_BIEN = 'DB', 'Dien Bien'
    DONG_NAI = 'DN', 'Dong Nai'
    DONG_THAP = 'DT', 'Dong Thap'
    GIA_LAI = 'GL', 'Gia Lai'
    HA_GIANG = 'HAUG', 'Ha Giang'
    HA_NAM = 'HNAM', 'Ha Nam'
    HA_NOI = 'HNOI', "Ha Noi"
    HA_TINH = "HT", "Ha Tinh"
    HAI_DUONG = "HD", "Hai Duong"
    HAI_PHONG = "HP", "Hai Phong"
    HOA_BINH = "HB", "Hoa Binh"
    HAU_GIANG = "HG", "Hau Giang"
    HUNG_YEN = "HY", "Hung Yen"
    HO_CHI_MINH_CITY = "HCMC", "Ho Chi Minh City"
    KHANH_HOA = "KH", "Khanh Hoa"
    KIEN_GIANG = "KG", "Kien Giang"
    KON_TUM = "KT", "Kon Tum"
    LAI_CHAU = "LCH", "Lai Chau"
    LAM_DONG = "LD", "Lam Dong"
    LANG_SON = "LS", "Lang Son"
    LAO_CAI = "LCAI", "Lao Cai"
    LONG_AN = "LA", "Long An"
    NAM_DINH = "ND", "Nam Dinh"
    NGHE_AN = "NA", "Nghe An"
    NINH_BINH = "NB", "Ninh Binh"
    NINH_THUAN = "NT", "Ninh Thuan"
    PHU_THO = "PT", "Phu Tho"
    PHU_YEN  ="PY" , 	"Phu Yen" 
    QUANG_BINH  ="QB" , 	"Quang Binh" 
    QUANG_NAM  ="QNM" , 	"Quang Nam" 
    QUANG_NGAI  ="QNG" , 	"Quang Ngai" 
    QUANG_NINH  ="QNI" , 	"Quang Ninh" 
    QUANG_TRI  ="QT" , 	"Quang Tri" 
    SOC_TRANG  ="ST" , 	"Soc Trang" 
    SON_LA  ="SL" , 	"Son La" 
    TAY_NINH  ="TNI" , 	"Tay Ninh" 
    THAI_BINH  ="TB" , 	"Thai Binh" 
    THAI_NGUYEN  ="TN" , 	"Thai Nguyen" 
    THANH_HOA  ="TH" , 	"Thanh Hoa" 
    THUA_THIEN_HUE  ="TTH" , 	"Thua Thien Hue" 

class Info(models.Model):
    tour= models.OneToOneField( Tour, related_name='tours', on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    diemxp =models.CharField(
        max_length=10,  # Maximum length of the database value ('LT' or 'ST')
        choices=City.choices,  # Use the choices defined in the Category model
        default=City.HA_NOI,  # Set a default choice ('LONG' by default)
    )
    diemden=models.CharField(
        max_length=10,  # Maximum length of the database value ('LT' or 'ST')
        choices=City.choices,  # Use the choices defined in the Category model
        default=City.HO_CHI_MINH_CITY,  # Set a default choice ('LONG' by default)
    )
    category = models.CharField(
        max_length=9,  # Maximum length of the database value ('LT' or 'ST')
        choices=Category.choices,  # Use the choices defined in the Category model
        default=Category.TRONGNGAY,  # Set a default choice ('LONG' by default)
    )

    status = models.CharField(
        max_length=9,  # Maximum length of the database value ('LT' or 'ST')
        choices=Status.choices,  # Use the choices defined in the Category model
        default=Status.AVAILABLE,  # Set a default choice ('LONG' by default)
    )

    def __str__(self):
        return str(self.tour)
