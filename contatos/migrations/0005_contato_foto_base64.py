# Generated by Django 5.0.6 on 2024-07-10 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0004_remove_usuario_last_login_usuario_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='foto_base64',
            field=models.TextField(blank=True, null=True),
        ),
    ]
