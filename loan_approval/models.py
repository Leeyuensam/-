from django.db import models


class Anti_Fraud_Yes(models.Model):
    sid = models.CharField(max_length=224, verbose_name='样本ID')
    label = models.CharField(verbose_name='是否作弊', max_length=500, blank=True, null=True, default=None)
    pkgname = models.CharField(max_length=500, verbose_name='包名(MD5加密)', blank=True, null=True, default=None)
    ver = models.CharField(max_length=500, verbose_name='APP版本', blank=True, null=True, default=None)
    adunitshowid = models.CharField(max_length=500, verbose_name='对外广告位ID（MD5加密）', blank=True, null=True, default=None)
    mediashowid = models.CharField(max_length=500, verbose_name='对外媒体ID（MD5加密）', blank=True, null=True, default=None)
    apptype = models.CharField(verbose_name='app所属分类', max_length=500, blank=True, null=True, default=None)
    nginxtime = models.CharField(verbose_name='请求到达服务时间', max_length=500, blank=True, null=True, default=None)
    ip = models.CharField(verbose_name='客户端IP地址', max_length=500, blank=True, null=True, default=None)
    city = models.CharField(verbose_name='城市', max_length=500, blank=True, null=True, default=None)
    province = models.CharField(verbose_name='省份', max_length=500, blank=True, null=True, default=None)
    reqrealip = models.CharField(verbose_name='请求的http协议头携带IP', max_length=500, blank=True, null=True, default=None)
    adidmd5 = models.CharField(verbose_name='Adroid ID的MD5值', max_length=500, blank=True, null=True, default=None)
    imeimd5 = models.CharField(verbose_name='imei的MD5值', max_length=500, blank=True, null=True, default=None)
    idfamd5 = models.CharField(verbose_name='idfa的MD5值', max_length=500, blank=True, null=True, default=None)
    openudidmd5 = models.CharField(verbose_name='openudid的MD5值', max_length=500, blank=True, null=True, default=None)
    macmd5 = models.CharField(verbose_name='mac的MD5值', max_length=500, blank=True, null=True, default=None)
    dvctype = models.CharField(verbose_name='设备类型', max_length=500, blank=True, null=True, default=None)
    model = models.CharField(verbose_name='机型', max_length=500, blank=True, null=True, default=None)
    make = models.CharField(verbose_name='厂商', max_length=500, blank=True, null=True, default=None)
    ntt = models.CharField(verbose_name='网络类型', max_length=500, blank=True, null=True, default=None)
    carrier = models.CharField(verbose_name='运营商', max_length=500, blank=True, null=True, default=None)
    os = models.CharField(verbose_name='操作系统', max_length=500, blank=True, null=True, default=None)
    osv = models.CharField(verbose_name='操作系统版本', max_length=500, blank=True, null=True, default=None)
    orientation = models.CharField(verbose_name='横竖屏', max_length=500, blank=True, null=True, default=None)
    lan = models.CharField(verbose_name='语言', max_length=500, blank=True, null=True, default=None)
    h = models.CharField(verbose_name='设备高', max_length=500, blank=True, null=True, default=None)
    w = models.CharField(verbose_name='设备宽', max_length=500, blank=True, null=True, default=None)
    ppi = models.CharField(verbose_name='屏幕密度', max_length=500, blank=True, null=True, default=None)

    class Meta:
        verbose_name = '欺诈申请队列'
        verbose_name_plural = '欺诈申请队列'

    def __str__(self):
        return self.sid


class CreditScore(models.Model):
    loan_ID = models.CharField(max_length=100, verbose_name='贷款ID')
    gender = models.CharField(verbose_name="性别", max_length=100, blank=True, null=True, default=None)
    age = models.CharField(verbose_name="年龄", max_length=100, blank=True, null=True, default=None)
    income = models.CharField(verbose_name="年收入", max_length=100, blank=True, null=True, default=None)
    income_source = models.CharField(verbose_name='收入来源', max_length=100, blank=True, null=True, default=None)
    job = models.CharField(verbose_name='工作类别', max_length=100, blank=True, null=True, default=None)
    job_history = models.CharField(verbose_name="工作年限", max_length=100, blank=True, null=True, default=None)
    edu = models.CharField(verbose_name='教育水平', max_length=100, blank=True, null=True, default=None)
    marry = models.CharField(verbose_name='婚姻状况', max_length=100, blank=True, null=True, default=None)
    is_Email = models.CharField(verbose_name='是否有电子邮箱', max_length=100, blank=True, null=True, default=None)
    is_WorkTel = models.CharField(verbose_name='是否有工作电话', max_length=100, blank=True, null=True, default=None)
    is_Tel = models.CharField(verbose_name='是否有手机', max_length=100, blank=True, null=True, default=None)
    is_Car = models.CharField(verbose_name='是否有车', max_length=100, blank=True, null=True, default=None)
    Child_Num = models.CharField(verbose_name='孩子数量', max_length=100, blank=True, null=True, default=None)
    live_addr = models.CharField(verbose_name='居住方式', max_length=100, blank=True, null=True, default=None)
    Fam_Num = models.CharField(verbose_name='家庭成员数量', max_length=100, blank=True, null=True, default=None)
    is_Asset = models.CharField(verbose_name="是否有固定资产", max_length=100, blank=True, null=True, default=None)
    is_Break = models.CharField(verbose_name="是否违约", max_length=100, blank=True, null=True, default=None)
    credit_score = models.CharField(verbose_name='信用分', max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = '贷款额度审核'
        verbose_name_plural = '贷款额度审核'

    def __str__(self):
        return self.loan_ID


class CreditLevelPredict(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    ApplicantIncome = models.CharField(max_length=100, blank=True, null=True, default=None)
    CoapplicantIncome = models.CharField(max_length=100, blank=True, null=True, default=None)
    LoanAmount = models.CharField(max_length=100, blank=True, null=True, default=None)
    Loan_Amount_Term = models.CharField(max_length=100, blank=True, null=True, default=None)
    Credit_History = models.CharField(max_length=100, blank=True, null=True, default=None)
    Gender_Male = models.CharField(max_length=100, blank=True, null=True, default=None)
    Married_Yes = models.CharField(max_length=100, blank=True, null=True, default=None)
    Dependents_1 = models.CharField(max_length=100, blank=True, null=True, default=None)
    Dependents_2 = models.CharField(max_length=100, blank=True, null=True, default=None)
    Dependents_3 = models.CharField(max_length=100, blank=True, null=True, default=None)
    Education_Not_Graduate = models.CharField(max_length=100, blank=True, null=True, default=None)
    Self_Employed_Yes = models.CharField(max_length=100, blank=True, null=True, default=None)
    Property_Area_Semiurban = models.CharField(max_length=100, blank=True, null=True, default=None)
    Property_Area_Urban = models.CharField(max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = '信用等级预测'
        verbose_name_plural = '信用等级预测'


class CreditLevel(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    Gender = models.CharField(max_length=100, blank=True, null=True, default=None)
    Married = models.CharField(max_length=100, blank=True, null=True, default=None)
    Dependents = models.CharField(max_length=100, blank=True, null=True, default=None)
    Education = models.CharField(max_length=100, blank=True, null=True, default=None)
    Self_Employed = models.CharField(max_length=100, blank=True, null=True, default=None)
    ApplicantIncome = models.CharField(max_length=100, blank=True, null=True, default=None)
    CoapplicantIncome = models.CharField(max_length=100, blank=True, null=True, default=None)
    LoanAmount = models.CharField(max_length=100, blank=True, null=True, default=None)
    Loan_Amount_Term = models.CharField(max_length=100, blank=True, null=True, default=None)
    Credit_History = models.CharField(max_length=100, blank=True, null=True, default=None)
    Property_Area = models.CharField(max_length=100, blank=True, null=True, default=None)
    Loan_Status = models.CharField(max_length=100, blank=True, null=True, default=None)
    Level = models.CharField(max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = '信用等级数据'
        verbose_name_plural = '信用等级数据'

# Create your models here.
