import traceback

from termcolor import cprint



class Network():
    MAINNET: str = "wss://stream.openseabeta.com/socket/websocket"
    TESTNET: str = "wss://testnets-stream.openseabeta.com/socket/websocket"


class EventTypes():
    ITEM_METADATA_UPDATED: str = 'item_metadata_updated'
    ITEM_LISTED: str = 'item_listed'
    ITEM_SOLD: str = 'item_sold'
    ITEM_TRANSFERRED: str = 'item_transferred'
    ITEM_RECEIVED_OFFER: str = 'item_received_offer'
    ITEM_RECEIVED_BID: str = 'item_received_bid'
    ITEM_CANCELLED: str = 'item_cancelled'
    COLLECTION_OFFER: str = 'collection_offer'
    TRAIT_OFFER: str = 'trait_offer'
    ORDER_INVALIDATE: str = 'order_invalidate'
    ORDER_REVALIDATE: str = 'order_revalidate'



class Logger():
    def __init__(self, message: str) -> None:
        self.message = message

    def debug(self):
        cprint(f'[DEBUG]: {self.message}', 'cyan')

    def info(self):
        cprint(f'[INFO]: {self.message}', 'green')

    def warn(self):
        cprint(f'[WARN]: {self.message}', 'yellow')

    def error(self):
        traceback.print_exc()
        cprint(f'[ERROR]: {self.message}', 'red')

