# Generated by Django 5.2 on 2025-04-28 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bidding_bid_bidding_bidder_bidding_item_bidding_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidding',
            old_name='bidder',
            new_name='user',
        ),
    ]
