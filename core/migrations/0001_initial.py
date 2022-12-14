# Generated by Django 4.1.1 on 2022-09-09 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=10
                    ),
                ),
                (
                    "user_roles",
                    models.CharField(
                        choices=[
                            ("OfficeAdmin", "OfficeAdmin"),
                            ("Supervisor", "Supervisor"),
                            ("LoanOfficer", "LoanOfficer"),
                            ("Cashier", "Cashier"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_of_birth", models.DateField(default="2000-01-01", null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("country", models.CharField(max_length=50, null=True)),
                ("county", models.CharField(max_length=50, null=True)),
                ("subcounty", models.CharField(max_length=50, null=True)),
                ("city", models.CharField(max_length=50, null=True)),
                ("area", models.CharField(max_length=150, null=True)),
                ("mobile", models.CharField(default="0", max_length=10, null=True)),
                ("pincode", models.CharField(default="", max_length=10, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="user_permissions",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "permissions": (("OfficeAdmin", "Can manage all users accounts."),),
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                ("national_id", models.PositiveIntegerField(default=0)),
                ("email", models.EmailField(max_length=255, null=True)),
                ("account_number", models.CharField(max_length=50, unique=True)),
                ("date_of_birth", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=10
                    ),
                ),
                ("occupation", models.CharField(max_length=200)),
                ("annual_income", models.BigIntegerField()),
                ("country", models.CharField(max_length=50)),
                ("county", models.CharField(max_length=50)),
                ("subcounty", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("area", models.CharField(max_length=150)),
                ("mobile", models.CharField(default=True, max_length=20, null=True)),
                ("pincode", models.CharField(default=True, max_length=20, null=True)),
                ("photo", models.ImageField(null=True, upload_to="static/img/users")),
                (
                    "signature",
                    models.ImageField(null=True, upload_to="static/img/signatures"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_client", models.BooleanField(default=True)),
                (
                    "status",
                    models.CharField(default="UnAssigned", max_length=50, null=True),
                ),
                (
                    "sharecapital_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "entrancefee_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "membershipfee_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "bookfee_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "insurance_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LoanAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_no", models.CharField(max_length=50, unique=True)),
                (
                    "interest_type",
                    models.CharField(
                        choices=[("Flat", "Flat"), ("Declining", "Declining")],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Applied", "Applied"),
                            ("Withdrawn", "Withdrawn"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                            ("Closed", "Closed"),
                        ],
                        max_length=20,
                    ),
                ),
                ("opening_date", models.DateField(auto_now_add=True)),
                ("approved_date", models.DateField(blank=True, null=True)),
                ("loan_issued_date", models.DateField(blank=True, null=True)),
                ("closed_date", models.DateField(blank=True, null=True)),
                ("loan_amount", models.DecimalField(decimal_places=6, max_digits=19)),
                ("loan_repayment_period", models.IntegerField()),
                ("loan_repayment_every", models.IntegerField()),
                (
                    "loan_repayment_amount",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=19, null=True
                    ),
                ),
                (
                    "total_loan_amount_repaid",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                ("loanpurpose_description", models.TextField()),
                (
                    "interest_charged",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "total_interest_repaid",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "total_loan_paid",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "total_loan_balance",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                (
                    "loanprocessingfee_amount",
                    models.DecimalField(decimal_places=6, default=0, max_digits=19),
                ),
                ("no_of_repayments_completed", models.IntegerField(default=0)),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.client",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "loan_issued_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="loan_issued_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LoanRepaymentEvery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Receipts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("receipt_number", models.CharField(max_length=50, unique=True)),
                (
                    "sharecapital_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "entrancefee_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "membershipfee_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "bookfee_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "loanprocessingfee_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "savingsdeposit_thrift_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "fixeddeposit_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "recurringdeposit_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "loanprinciple_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "loaninterest_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "insurance_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "savings_balance_atinstant",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=19, null=True
                    ),
                ),
                (
                    "demand_loanprinciple_amount_atinstant",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "demand_loaninterest_amount_atinstant",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "principle_loan_balance_atinstant",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.client",
                    ),
                ),
                (
                    "group_loan_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="group_loan_account",
                        to="core.loanaccount",
                    ),
                ),
                (
                    "member_loan_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.loanaccount",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("Loans", "Loans"),
                            ("LoanProcessingFee", "LoanProcessingFee"),
                            ("Penalty", "Penalty"),
                        ],
                        max_length=25,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=6, max_digits=19)),
                (
                    "interest",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                ("total_amount", models.DecimalField(decimal_places=6, max_digits=19)),
                ("totalamount_in_words", models.CharField(max_length=200)),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.client",
                    ),
                ),
                (
                    "loan_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_loanaccount",
                        to="core.loanaccount",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
