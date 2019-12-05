# Generated by Django 2.2.8 on 2019-12-04 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('img', models.ImageField(upload_to='books_images')),
                ('author', models.CharField(max_length=255)),
                ('pages', models.IntegerField()),
                ('published', models.DateField()),
                ('isbn', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('img_source', models.URLField(max_length=255, null=True)),
                ('book_source', models.URLField(blank=True, max_length=255, null=True)),
                ('parsing_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('website', models.URLField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('moderated', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='cat',
            field=models.ManyToManyField(to='catalog.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='char',
            field=models.ManyToManyField(to='catalog.Character'),
        ),
    ]