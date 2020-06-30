# Generated by Django 3.0.6 on 2020-06-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_approval', '0002_auto_20200629_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('Gender', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Married', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Dependents', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Education', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Self_Employed', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('ApplicantIncome', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('CoapplicantIncome', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('LoanAmount', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Loan_Amount_Term', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Credit_History', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Property_Area', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Loan_Status', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Level', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'verbose_name': '信用等级数据',
                'verbose_name_plural': '信用等级数据',
            },
        ),
        migrations.CreateModel(
            name='CreditLevelPredict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('ApplicantIncome', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('CoapplicantIncome', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('LoanAmount', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Loan_Amount_Term', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Credit_History', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Gender_Male', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Married_Yes', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Dependents_1', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Dependents_2', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Dependents_3', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Education_Not_Graduate', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Self_Employed_Yes', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Property_Area_Semiurban', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Property_Area_Urban', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'verbose_name': '信用等级预测',
                'verbose_name_plural': '信用等级预测',
            },
        ),
    ]
