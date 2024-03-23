from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_save
from .models import AuctionItems, AuctionItemResponses, AuctionItemResponsesTracking, AuctionItemImage

@receiver(pre_save, sender=AuctionItemResponses)
def cache_previous_bid(sender, instance, *args, **kwargs):
    original_price = None
    print(instance)
    if instance.bid_price:
        try:
            original_price = AuctionItemResponses.objects.get(pk=instance.id).bid_price
        except ObjectDoesNotExist:
            original_price = 0

    instance.__original_price = original_price


@receiver(post_save, sender=AuctionItemResponses)
def update_responses_tracking(sender, instance, created, **kwargs):
    if instance.bid_price != instance.__original_price:
        obj, created = AuctionItemResponsesTracking.objects.update_or_create(
            auction_item_response = instance,
            bid=instance.bid_price,
            defaults={
                'auction_item_response':instance,
                'bid':instance.bid_price
            }
        )

@receiver(post_save, sender=AuctionItemResponses)
def update_item_best_bid_price(sender, instance, created, **kwargs):
    best_bid = 0
    try:
        obj = AuctionItems.objects.get(pk=instance.auction_item.id)
        best_bid = obj.fetch_best_bid_price["bid_price__min"]
        obj.best_bid_price = best_bid
        obj.save()
    except Exception as e:
        print(f'Error saving Auction Item Best Bid ! ->: {e}')

@receiver(post_save, sender=AuctionItemImage)
def create_image_thumbnail(sender, instance, created, **kwargs):
    
    # To prevent post_save recursion without overriding model save()
    # this is introduced because post_save handler needs to save
    # the sender instance it will trigger post_save again
    # thats why we use a custom attribute like _dirty 

    if not instance:
        return

    if hasattr(instance, '_dirty'):
        return

    if not instance.image:
        return

    import os
    from PIL import Image
    from io import StringIO, BytesIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.core.files.base import ContentFile
    
    # Set our max thumbnail size in a tuple (max width, max height)
    THUMBNAIL_SIZE = (233, 175)

    print(instance.image)
    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(instance.image.path)

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that contrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, image.format)
    temp_handle = temp_handle.getvalue()

    # Save image to a ContentFile which can be saved into
    # ImageField
    img_file = ContentFile(temp_handle)
    print('trying to save thumbnail')
    try:
        instance._dirty = True
        instance.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(instance.image.name)[0], os.path.splitext(instance.image.name)[1]),
            img_file,
            save=True
        )
    except Exception as e:
        print(f'Error creating thumbnail ! -> : {e}')
    finally:
        del instance._dirty