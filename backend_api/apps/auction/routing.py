from django.urls import re_path, path
from channels.routing import URLRouter
from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/auction/$', consumers.AuctionConsumer.as_asgi()),
# ]
auction_websocket_urlpatterns = [
    re_path(r'auction/$', consumers.AuctionConsumer.as_asgi()),
    re_path(r'auction/dashboard/$', consumers.AuctionBiddingActivityConsumer.as_asgi())
]