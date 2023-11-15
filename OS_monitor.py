import asyncio
import multiprocessing
import threading
import time

from opensea_sdk import *

api_key = '' # Your opensea api key

def callback(payload: dict):
    print(payload)
    return


def thread():

    slugs = []
    with open('SLUGs.txt', 'r') as file:
        for i in file:
            slugs.append(i.rstrip())

    asyncio.set_event_loop(asyncio.new_event_loop())

    Client = OpenseaStreamClient(api_key, Network.MAINNET)

    for slug in slugs:
        # Client.onItemListed(slug, callback)
        # Client.onItemReceivedOffer(slug, callback)
        Client.onItemReceivedBid(slug, callback)

    Client.startListening()


if __name__ == '__main__':
    # thread()
    while True:


        thread_ = multiprocessing.Process(target=thread, args=())
        thread_.start()

        time.sleep(3600)

        thread_.terminate()
