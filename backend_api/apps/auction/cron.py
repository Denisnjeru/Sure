import datetime
import pytz

from .models import Auction

def open_close_auction():
    """
    Add to cron job to open and close Auction automatically
    """
    
    time_utc = datetime.datetime.now(datetime.timezone.utc)

    open_auctions = Auction.objects.filter(closing_date__gte=time_utc)
    for auction in open_auctions:
        opening_date = auction.opening_date
        

        if opening_date < time_utc:
            auction.status_open = True
            auction.save()

    closing_auctions = Auction.objects.filter(closing_date__lte=time_utc, status_open=True)
    for auction in closing_auctions:
        closing_date = auction.closing_date
        if time_utc > closing_date:
            auction.status_open = False
            auction.save()

    return True
