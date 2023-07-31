from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Status(models.TextChoices):
    PENDING = 'PEN', 'Pending'
    AVAILABLE='AVAIL','Available'
    ON_HOLD = 'HLD', 'On Hold'

class Tour(models.Model):
    matour = models.AutoField(db_column='MaTour', primary_key=True)  # Field name made lowercase.
    tentour = models.CharField(db_column='TenTour', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anh = models.CharField(db_column='Anh', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ngaybatdau = models.DateField(db_column='NgayBatDau', blank=True, null=True)  # Field name made lowercase.
    sokhachtourtoithieu = models.IntegerField(db_column='SoKhachTourToiThieu', blank=True, null=True)  # Field name made lowercase.
    sokhachtourtoida = models.IntegerField(db_column='SoKhachTourToiDa', blank=True, null=True)  # Field name made lowercase.
    giavelenguoilon = models.FloatField(db_column='GiaVeLeNguoiLon', blank=True, null=True)  # Field name made lowercase.
    giaveletreem = models.FloatField(db_column='GiaVeLeTreEm', blank=True, null=True)  # Field name made lowercase.
    giavedoannguoilon = models.FloatField(db_column='GiaVeDoanNguoiLon', blank=True, null=True)  # Field name made lowercase.
    giavedoantreem = models.FloatField(db_column='GiaVeDoanTreEm', blank=True, null=True)  # Field name made lowercase.
    sokhachdoantoithieu = models.IntegerField(db_column='SoKhachDoanToiThieu', blank=True, null=True)  # Field name made lowercase.
    sodem = models.IntegerField(db_column='SoDem')  # Field name made lowercase.
    songay = models.IntegerField(db_column='SoNgay')  # Field name made lowercase.
    machinhanh = models.IntegerField(db_column='MaChiNhanh', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tour'

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
    tour= models.OneToOneField( Tour, related_name='tours', on_delete=models.CASCADE, primary_key= True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='tour_images')
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    city =models.CharField(
        max_length=10,  # Maximum length of the database value ('LT' or 'ST')
        choices=City.choices,  # Use the choices defined in the Category model
        default=City.HA_NOI,  # Set a default choice ('LONG' by default)
    )
    category = models.ForeignKey(Category, related_name='tours', on_delete=models.CASCADE)

    status = models.CharField(
        max_length=9,  # Maximum length of the database value ('LT' or 'ST')
        choices=Status.choices,  # Use the choices defined in the Category model
        default=Status.PENDING,  # Set a default choice ('LONG' by default)
    )

    def __str__(self):
        return str(self.tour)
