# Generated by Django 5.0 on 2023-12-20 06:03

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Identity", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CertificateRelated",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("certificate", models.CharField(max_length=10000)),
                ("private_key", models.CharField(max_length=10000)),
                ("public_key", models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Environment",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "membership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.membership",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Network",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="membership",
            name="network",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Identity.network"
            ),
        ),
        migrations.CreateModel(
            name="FabricClient",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "certificate_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.certificaterelated",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.environment",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.network",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FabricAdmin",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "certificate_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.certificaterelated",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.environment",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.network",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="environment",
            name="network",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Identity.network"
            ),
        ),
        migrations.CreateModel(
            name="OrdererNode",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "certificate_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.certificaterelated",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.environment",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.network",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationNetwork",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.network",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PeerNode",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "certificate_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.certificaterelated",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.environment",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.network",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
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
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="identity_users", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="identity_users", to="auth.permission"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserOrganization",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Identity.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Identity.user"
                    ),
                ),
            ],
        ),
    ]
