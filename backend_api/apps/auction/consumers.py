from  channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin,
    action
)
from djangochannelsrestframework.observer import model_observer

from .models import Auction, AuctionItems, AuctionItemResponsesTracking
from .serializers import AuctionConsumerSerializer, AuctionItemConsumerSerializer, AuctionItemResponsesTrackingConsumerSerializer

# Consumer for Auction
class AuctionConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):

    """
    This chat consumer handles websocket connections for auction connections.
    For Bidding(updating best prices etc.)
    """

    queryset = Auction.objects.all()
    serializer_class = AuctionConsumerSerializer
    lookup_field = "pk"

    @model_observer(AuctionItems)
    async def auction_item_activity(
        self,
        message,
        observer=None,
        subscribing_request_ids = [],
        **kwargs
    ):
        """
        This is evaluated once for each subscribed consumer.
        The result of `@message_activity.serializer` is provided here as the message.
        """
        # since we provide the request_id when subscribing we can just loop over them here.
        for request_id in subscribing_request_ids:
            print(f'Request id {request_id}')
            message_body = dict(request_id=request_id)
            message_body.update(message)
            await self.send_json(message_body)

    @auction_item_activity.serializer
    def auction_item_activity(self, instance: AuctionItems, action, **kwargs):
        """
        This is evaluated before the update is sent
        out to all the subscribing consumers.
        """
        print(action.value)
        return dict(data=AuctionItemConsumerSerializer(instance).data, action=action.value)


    @auction_item_activity.groups_for_consumer
    def auction_item_activity(self, auction=None,**kwargs):
        print(f'Auction {auction}')
        if auction is not None:
            yield f'-auction__{auction}'

    @auction_item_activity.groups_for_signal
    def auction_item_activity(self, instance: AuctionItems, **kwargs):
        yield f'-auction__{instance.auction_id}'

    @action()
    async def subscribe_to_activity_in_auction(self, pk, request_id, **kwargs):
        print('Subscribed!')
        print(self.scope['user'].is_authenticated)
        if "user" in self.scope and self.scope["user"].is_authenticated:
            await self.auction_item_activity.subscribe(auction=pk, request_id=request_id)

    @action()
    async def unsubscribe_to_activity_in_auction(self, pk, request_id, **kwargs):
        print('UnSubscribed!')
        await self.auction_item_activity.unsubscribe(auction=pk, request_id=request_id)


class AuctionBiddingActivityConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):

    """
    Auction bidding activity consumer
    """

    queryset = AuctionItemResponsesTracking.objects.all()
    serializer_class = AuctionItemConsumerSerializer
    lookup_field = "pk"

    @model_observer(AuctionItemResponsesTracking)
    async def auction_item_responses_activity(
        self,
        message,
        observer=None,
        subscribing_request_ids = [],
        **kwargs
    ):
        """
        This is evaluated once for each subscribed consumer.
        The result of `@message_activity.serializer` is provided here as the message.
        """
        # since we provide the request_id when subscribing we can just loop over them here.
        for request_id in subscribing_request_ids:
            print(f'Request id {request_id}')
            message_body = dict(request_id=request_id)
            message_body.update(message)
            await self.send_json(message_body)

    @auction_item_responses_activity.serializer
    def auction_item_responses_activity(self, instance: AuctionItemResponsesTracking, action, **kwargs):
        """
        This is evaluated before the update is sent
        out to all the subscribing consumers.
        """
        print(action.value)
        return dict(data=AuctionItemResponsesTrackingConsumerSerializer(instance).data, action=action.value)


    @auction_item_responses_activity.groups_for_consumer
    def auction_item_responses_tracking_activity(self, auction=None, auctionItem=None,**kwargs):
        print(f'Auction {auction}')
        print(f'Auction Item {auctionItem}')
        if (auction is not None) and (auctionItem is not None):
            yield f'-auction__{auction}__item{auctionItem}'

    @auction_item_responses_activity.groups_for_signal
    def auction_item_responses_activity(self, instance: AuctionItemResponsesTracking, **kwargs):
        print(f'Testing signal function: {instance}')
        yield f'-auction__{instance.auction_item_response.auction_item.auction.id}__item{instance.auction_item_response.auction_item.id}'

    @action()
    async def subscribe_to_activity_in_auction_item_response_tracking(self, pk, item_id, request_id,**kwargs):
        print('Subscribed to activity - auction item response tracking!')
        print(self.scope['user'].is_authenticated)
        if "user" in self.scope and self.scope["user"].is_authenticated:
            await self.auction_item_responses_tracking_activity.subscribe(auction=pk,  auctionItem=item_id, request_id=request_id)

    @action()
    async def unsubscribe_to_activity_in_auction_item_response_tracking(self, pk, item_id, request_id, **kwargs):
        print('Unsubscribed to activity - auction item response tracking!')
        await self.auction_item_responses_tracking_activity.unsubscribe(auction=pk, auctionItem=item_id, request_id=request_id)


# class BuyercAuctionConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
# Will delete the code below later on now ist still useful for reference

    # async def disconnect(self, code):
    #     if hasattr(self, "room_subscribe"):
    #         await self.remove_supplier_from_auction(self.auction_subscribe)
    #         await self.notify_suppliers()
    #     return await super().disconnect(code)



    # @database_sync_to_async
    # def get_auction(self, pk: int) -> Auction:
    #     return Auction.objects.get(pk=pk)
    
    # @database_sync_to_async
    # def current_suppliers(self, auction: Auction):
    #     return [AuctionInviteeConsumerSerializer(auction_invitee).data for auction_invitee in auction.invitee_auction.all()]


    # @action()
    # async def join_auction(self, pk, **kwargs):
    #     if "user" in self.scope and self.scope["user"].is_authenticated:
    #         print(f'Authenticating user -- {self.scope["user"]} to auction.')
    #         print(f'pk is this: {pk}')
    #         self.auction_subscribe = pk
    #         await self.add_supplier_to_auction(pk)
    #         await self.notify_auction_invitees()
    
    # @action()
    # async def leave_auction(self, pk, **kwargs):
    #     await self.remove_supplier_from_auction(pk)

    # async def notify_suppliers(self):
    #     auction: Auction = await self.get_auction(self.auction_subscribe)
    #     for group in self.groups:
    #         await self.channel_layer.group_send(
    #             group,
    #             {
    #                 'type': 'update_suppliers',
    #                 'usuarios': await self.current_suppliers(auction)
    #             }
    #         )

    # async def update_suppliers(self, event: dict):
    #     await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    # @database_sync_to_async
    # def remove_supplier_from_auction(self, auction):
    #     supplier:Supplier = self.scope["Supplier"]
    #     supplier.invitee_auction_supplier.remove(auction)
    
    # @database_sync_to_async
    # def add_supplier_to_auction(self, pk):
    #     print(self.scope)
    #     supplier:Supplier = self.scope["Supplier"]
    #     if not supplier.invitee_auction_supplier.filter(pk=self.auction_subscribe).exists():
    #         supplier.invitee_auction_supplier.add(AuctionInvitee.objects.get(pk=pk))