from  channels.db import database_sync_to_async
from .exceptions import ClientError
from .models import Auction, AuctionItems
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile

@database_sync_to_async
def get_auction_or_error(pk, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room

@database_sync_to_async
def get_best_bids(pk, user):
    """
        Tries to get the best bid(s) (Depends on whether its reverse or foward auction).
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    
    try:
        auction = Auction.object.get(pk=pk)
    except Auction.DoesNotExist:
        raise ClientError("AUCTION_INVALID")
    return auction

def convertfiletobase64(file_obj):
    file_bytes = file_obj.read()
    file_bytes_base64 = base64.b64encode(file_bytes)
    file_bytes_base64_str = file_bytes_base64.decode('utf-8') # this is a str
    return file_bytes_base64_str

def convertbase64tofile(file_bytes_base64_str):
    file_bytes_base64 = file_bytes_base64_str.encode('utf-8')
    file_bytes = base64.b64decode(file_bytes_base64)
    return file_bytes

# Useful because javascript has no None its encoded to null as a string 
def NullStringToNone(request):
    request.data._mutable = True
    for j in request.data:
        if request.data[j] == 'null':
            request.data[j] = None
    request.data._mutable = False
    return None

def ValidateIfInMemoryUploadedFile(obj):
    if not isinstance(obj, InMemoryUploadedFile):
        return False
    else:
        return True