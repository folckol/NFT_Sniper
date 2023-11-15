import asyncio
import multiprocessing
import threading
import time
import uuid
from pprint import pprint

import dateutil.parser
import requests

from opensea_sdk import *
from DB import *

api_key = '' # Your opensea api key

def callback(payload: dict):
    print(payload)

    if payload['event_type'] == 'trait_offer':
        ...
    elif payload['event_type'] == 'item_received_bid':

        collection = payload['payload']['collection']['slug']
        collection_ = session.query(Collection).filter(Collection.collection_slug == collection).first()
        if collection_ is None:
            collection_ = Collection(collection_slug=collection)
            session.add(collection_)

        id = payload['payload']['item']['nft_id']

        item = session.query(Item).filter(Item.id == id).first()
        if item is None:
            item = Item(id=id,
                        chain=payload['payload']['item']['chain']['name'],
                        permalink=payload['payload']['item']['permalink'],
                        token_id=payload['payload']['item']['chain']['name'],

                        collection = collection_
                        )

            session.add(item)

            MD = Metadata(id=str(uuid.uuid4()),
                          animation_url=payload['payload']['item']['metadata']['animation_url'],
                          image_url=payload['payload']['item']['metadata']['image_url'],
                          metadata_url=payload['payload']['item']['metadata']['metadata_url'],
                          name=payload['payload']['item']['metadata']['name'],

                          item=item)

            session.add(MD)


            try:
                data = GetNFTData(id.split('/')[1], id.split('/')[2])

                item.num_sales = data['num_sales']
                item.background_color = data['background_color']
                item.image_url = data['image_url']
                item.image_preview_url = data['image_preview_url']
                item.image_thumbnail_url = data['image_thumbnail_url']
                item.image_original_url = data['image_original_url']
                item.animation_url = data['animation_url']
                item.animation_original_url = data['animation_original_url']
                item.name = data['name']
                item.description = data['description']
                item.external_link = data['external_link']


                for trait in data['traits']:
                    trait_ = Trait(id=str(uuid.uuid4()),
                                  trait_type = trait['trait_type'],
                                  display_type = trait['display_type'],
                                  max_value = trait['max_value'],
                                  trait_count = trait['trait_count'],
                                  order = trait['order'],
                                  value = trait['value'],

                                   item = item
                                )

                    session.add(trait_)

                collection_.asset_contract_criteria = data['asset_contract']['address']
                collection_.asset_contract_type = data['asset_contract']['asset_contract_type']
                collection_.chain_identifier = data['asset_contract']['chain_identifier']
                collection_.created_date = data['collection']['created_date']
                collection_.name = data['collection']['name']
                collection_.nft_version = data['asset_contract']['nft_version']
                collection_.opensea_version = data['asset_contract']['opensea_version']
                collection_.owner = data['asset_contract']['owner']
                collection_.schema_name = data['asset_contract']['schema_name']
                collection_.symbol = data['asset_contract']['symbol']
                collection_.total_supply = data['asset_contract']['total_supply']
                collection_.description = data['collection']['description']
                collection_.external_link = data['asset_contract']['external_link']
                collection_.image_url = data['asset_contract']['image_url']
                collection_.default_to_fiat = data['asset_contract']['default_to_fiat']
                collection_.dev_buyer_fee_basis_points = data['collection']['dev_buyer_fee_basis_points']
                collection_.dev_seller_fee_basis_points = data['collection']['dev_seller_fee_basis_points']
                collection_.only_proxied_transfers = data['collection']['only_proxied_transfers']
                collection_.opensea_buyer_fee_basis_points = data['collection']['opensea_buyer_fee_basis_points']
                collection_.opensea_seller_fee_basis_points = data['collection']['opensea_seller_fee_basis_points']
                collection_.buyer_fee_basis_points = data['asset_contract']['buyer_fee_basis_points']
                collection_.seller_fee_basis_points = data['asset_contract']['seller_fee_basis_points']
                collection_.payout_address = data['asset_contract']['payout_address']

                stats = Stat(id=str(uuid.uuid4()),
                             one_minute_volume=data['collection']['stats']['one_minute_volume'],
                             one_minute_change=data['collection']['stats']['one_minute_change'],
                             one_minute_sales=data['collection']['stats']['one_minute_sales'],
                             one_minute_sales_change=data['collection']['stats']['one_minute_sales_change'],
                             one_minute_average_price=data['collection']['stats']['one_minute_average_price'],
                             one_minute_difference=data['collection']['stats']['one_minute_difference'],
                             five_minute_volume=data['collection']['stats']['five_minute_volume'],
                             five_minute_change=data['collection']['stats']['five_minute_change'],
                             five_minute_sales=data['collection']['stats']['five_minute_sales'],
                             five_minute_sales_change=data['collection']['stats']['five_minute_sales_change'],
                             five_minute_average_price=data['collection']['stats']['five_minute_average_price'],
                             five_minute_difference=data['collection']['stats']['five_minute_difference'],
                             fifteen_minute_volume=data['collection']['stats']['fifteen_minute_volume'],
                             fifteen_minute_change=data['collection']['stats']['fifteen_minute_change'],
                             fifteen_minute_sales=data['collection']['stats']['fifteen_minute_sales'],
                             fifteen_minute_sales_change=data['collection']['stats']['fifteen_minute_sales_change'],
                             fifteen_minute_average_price=data['collection']['stats']['fifteen_minute_average_price'],
                             fifteen_minute_difference=data['collection']['stats']['fifteen_minute_difference'],
                             thirty_minute_volume=data['collection']['stats']['thirty_minute_volume'],
                             thirty_minute_change=data['collection']['stats']['thirty_minute_change'],
                             thirty_minute_sales=data['collection']['stats']['thirty_minute_sales'],
                             thirty_minute_sales_change=data['collection']['stats']['thirty_minute_sales_change'],
                             thirty_minute_average_price=data['collection']['stats']['thirty_minute_average_price'],
                             thirty_minute_difference=data['collection']['stats']['thirty_minute_difference'],
                             one_hour_volume=data['collection']['stats']['one_hour_volume'],
                             one_hour_change=data['collection']['stats']['one_hour_change'],
                             one_hour_sales=data['collection']['stats']['one_hour_sales'],
                             one_hour_sales_change=data['collection']['stats']['one_hour_sales_change'],
                             one_hour_average_price=data['collection']['stats']['one_hour_average_price'],
                             one_hour_difference=data['collection']['stats']['one_hour_difference'],
                             six_hour_volume=data['collection']['stats']['six_hour_volume'],
                             six_hour_change=data['collection']['stats']['six_hour_change'],
                             six_hour_sales=data['collection']['stats']['six_hour_sales'],
                             six_hour_sales_change=data['collection']['stats']['six_hour_sales_change'],
                             six_hour_average_price=data['collection']['stats']['six_hour_average_price'],
                             six_hour_difference=data['collection']['stats']['six_hour_difference'],
                             one_day_volume=data['collection']['stats']['one_day_volume'],
                             one_day_change=data['collection']['stats']['one_day_change'],
                             one_day_sales=data['collection']['stats']['one_day_sales'],
                             one_day_sales_change=data['collection']['stats']['one_day_sales_change'],
                             one_day_average_price=data['collection']['stats']['one_day_average_price'],
                             one_day_difference=data['collection']['stats']['one_day_difference'],
                             seven_day_volume=data['collection']['stats']['seven_day_volume'],
                             seven_day_change=data['collection']['stats']['seven_day_change'],
                             seven_day_sales=data['collection']['stats']['seven_day_sales'],
                             seven_day_average_price=data['collection']['stats']['seven_day_average_price'],
                             seven_day_difference=data['collection']['stats']['seven_day_difference'],
                             thirty_day_volume=data['collection']['stats']['thirty_day_volume'],
                             thirty_day_change=data['collection']['stats']['thirty_day_change'],
                             thirty_day_sales=data['collection']['stats']['thirty_day_sales'],
                             thirty_day_average_price=data['collection']['stats']['thirty_day_average_price'],
                             thirty_day_difference=data['collection']['stats']['thirty_day_difference'],
                             total_volume=data['collection']['stats']['total_volume'],
                             total_sales=data['collection']['stats']['total_sales'],
                             total_supply=data['collection']['stats']['total_supply'],
                             count=data['collection']['stats']['count'],
                             num_owners=data['collection']['stats']['num_owners'],
                             average_price=data['collection']['stats']['average_price'],
                             num_reports=data['collection']['stats']['num_reports'],
                             market_cap=data['collection']['stats']['market_cap'],
                             floor_price=data['collection']['stats']['floor_price'],
                             )

                collection_.stats = [stats]

                ready_fees = []
                for i in data['collection']['fees']:
                    name = next(iter(i))  # Получение ключа первого уровня ('opensea_fees')
                    address, fee_percentage = next(
                        iter(i[name].items()))  # Получение пары ключ-значение из вложенного словаря

                    fee = Fee(id=str(uuid.uuid4()),
                              name=name,
                              address=address,
                              fee_perccentage=fee_percentage
                              )

                    ready_fees.append(fee)

                collection_.fees = ready_fees

            except:
                pass

        paymentToken = session.query(PaymentToken).filter(
            PaymentToken.name == payload['payload']['payment_token']['name']).first()
        if paymentToken is None:
            paymentToken = PaymentToken(id=str(uuid.uuid4()),
                                        address=payload['payload']['payment_token']['address'],
                                        decimals=payload['payload']['payment_token']['decimals'],
                                        eth_price=payload['payload']['payment_token']['eth_price'],
                                        name=payload['payload']['payment_token']['name'],
                                        symbol=payload['payload']['payment_token']['symbol'],
                                        usd_price=payload['payload']['payment_token']['usd_price']
                                        )
            session.add(paymentToken)

        cons_ready = []
        for consideration_data in payload['payload']['protocol_data']['parameters']['consideration']:
            consideration = Consideration(id=str(uuid.uuid4()),
                                          endAmount=consideration_data['endAmount'],
                                          identifierOrCriteria=consideration_data['identifierOrCriteria'],
                                          itemType=consideration_data['itemType'],
                                          recipient=consideration_data['recipient'],
                                          startAmount=consideration_data['startAmount'],
                                          token=consideration_data['token'],
                                          )
            cons_ready.append(consideration)

        protocol_data_offers_ready = []
        for protocol_data_offer in payload['payload']['protocol_data']['parameters']['offer']:
            PD_offer = ProtocolDataOffer(id=str(uuid.uuid4()),
                                         endAmount=protocol_data_offer['endAmount'],
                                         identifierOrCriteria=protocol_data_offer['identifierOrCriteria'],
                                         itemType=protocol_data_offer['itemType'],
                                         startAmount=protocol_data_offer['startAmount'],
                                         token=protocol_data_offer['token'],
                                         )
            protocol_data_offers_ready.append(PD_offer)

        protocol_data = ProtocolData(id = str(uuid.uuid4()),
                                     conduitKey=payload['payload']['protocol_data']['parameters']['conduitKey'],
                                     counter=payload['payload']['protocol_data']['parameters']['counter'],
                                     endTime=payload['payload']['protocol_data']['parameters']['endTime'],
                                     offerer=payload['payload']['protocol_data']['parameters']['offerer'],
                                     orderType=payload['payload']['protocol_data']['parameters']['orderType'],
                                     salt=payload['payload']['protocol_data']['parameters']['salt'],
                                     startTime=payload['payload']['protocol_data']['parameters']['startTime'],
                                     totalOriginalConsiderationItems=payload['payload']['protocol_data']['parameters'][
                                         'totalOriginalConsiderationItems'],
                                     zone=payload['payload']['protocol_data']['parameters']['zone'],
                                     zoneHash=payload['payload']['protocol_data']['parameters']['zoneHash'],
                                     signature=payload['payload']['protocol_data']['signature'],

                                     protocol_data_offers_=protocol_data_offers_ready,
                                     considerations_=cons_ready
                                     )
        session.add(protocol_data)

        offer = Offer(order_hash=payload['payload']['order_hash'],
                      maker=payload['payload']['maker']['address'],
                      protocol_address=payload['payload']['protocol_address'],
                      quantity=payload['payload']['quantity'],
                      taker=payload['payload']['taker'],

                      protocol_data=[protocol_data],
                      payment_token=[paymentToken])

        session.add(offer)

        if item.item_offers == None or len(item.item_offers) == 0:
            item.item_offers = [offer]
        else:
            item.item_offers.append(offer)

        session.commit()



    elif payload['event_type'] == 'collection_offer':

        # pprint(payload)

        collection = payload['payload']['collection']['slug']
        collection_ = session.query(Collection).filter(Collection.collection_slug == collection).first()
        if collection_ is None:
            collection_ = Collection(collection_slug=collection)
            session.add(collection_)

        paymentToken = session.query(PaymentToken).filter(
            PaymentToken.name == payload['payload']['payment_token']['name']).first()
        if paymentToken is None:
            paymentToken = PaymentToken(id=str(uuid.uuid4()),
                                        address=payload['payload']['payment_token']['address'],
                                        decimals=payload['payload']['payment_token']['decimals'],
                                        eth_price=payload['payload']['payment_token']['eth_price'],
                                        name=payload['payload']['payment_token']['name'],
                                        symbol=payload['payload']['payment_token']['symbol'],
                                        usd_price=payload['payload']['payment_token']['usd_price']
                                        )
            session.add(paymentToken)

        cons_ready = []
        for consideration_data in payload['payload']['protocol_data']['parameters']['consideration']:
            consideration = Consideration(id=str(uuid.uuid4()),
                                          endAmount=consideration_data['endAmount'],
                                          identifierOrCriteria=consideration_data['identifierOrCriteria'],
                                          itemType=consideration_data['itemType'],
                                          recipient=consideration_data['recipient'],
                                          startAmount=consideration_data['startAmount'],
                                          token=consideration_data['token'],
                                          )
            cons_ready.append(consideration)

        protocol_data_offers_ready = []
        for protocol_data_offer in payload['payload']['protocol_data']['parameters']['offer']:
            PD_offer = ProtocolDataOffer(id=str(uuid.uuid4()),
                                         endAmount=protocol_data_offer['endAmount'],
                                         identifierOrCriteria=protocol_data_offer['identifierOrCriteria'],
                                         itemType=protocol_data_offer['itemType'],
                                         startAmount=protocol_data_offer['startAmount'],
                                         token=protocol_data_offer['token'],
                                         )
            protocol_data_offers_ready.append(PD_offer)

        protocol_data = ProtocolData(id = str(uuid.uuid4()),
                                     conduitKey=payload['payload']['protocol_data']['parameters']['conduitKey'],
                                     counter=payload['payload']['protocol_data']['parameters']['counter'],
                                     endTime=payload['payload']['protocol_data']['parameters']['endTime'],
                                     offerer=payload['payload']['protocol_data']['parameters']['offerer'],
                                     orderType=payload['payload']['protocol_data']['parameters']['orderType'],
                                     salt=payload['payload']['protocol_data']['parameters']['salt'],
                                     startTime=payload['payload']['protocol_data']['parameters']['startTime'],
                                     totalOriginalConsiderationItems=payload['payload']['protocol_data']['parameters'][
                                         'totalOriginalConsiderationItems'],
                                     zone=payload['payload']['protocol_data']['parameters']['zone'],
                                     zoneHash=payload['payload']['protocol_data']['parameters']['zoneHash'],
                                     signature=payload['payload']['protocol_data']['signature'],

                                     protocol_data_offers_=protocol_data_offers_ready,
                                     considerations_=cons_ready
                                     )
        session.add(protocol_data)

        offer = Offer(order_hash=payload['payload']['order_hash'],
                      maker=payload['payload']['maker']['address'],
                      protocol_address=payload['payload']['protocol_address'],
                      quantity=payload['payload']['quantity'],
                      taker=payload['payload']['taker'],

                      protocol_data=[protocol_data],
                      payment_token=[paymentToken])

        session.add(offer)

        if collection_.offers == None or len(collection_.offers) == 0:
            collection_.offers = [offer]
        else:
            collection_.offers.append(offer)

        session.commit()

    elif payload['event_type'] == 'item_listed':

        # pprint(payload)

        collection = payload['payload']['collection']['slug']
        collection_ = session.query(Collection).filter(Collection.collection_slug == collection).first()
        if collection_ is None:
            collection_ = Collection(collection_slug=collection)
            session.add(collection_)

        id = payload['payload']['item']['nft_id']

        item = session.query(Item).filter(Item.id == id).first()
        if item is None:
            item = Item(id=id,
                        chain=payload['payload']['item']['chain']['name'],
                        permalink=payload['payload']['item']['permalink'],
                        token_id=payload['payload']['item']['chain']['name'],

                        collection = collection_
                        )

            session.add(item)

            MD = Metadata(id=str(uuid.uuid4()),
                          animation_url=payload['payload']['item']['metadata']['animation_url'],
                          image_url=payload['payload']['item']['metadata']['image_url'],
                          metadata_url=payload['payload']['item']['metadata']['metadata_url'],
                          name=payload['payload']['item']['metadata']['name'],

                          item=item)

            session.add(MD)


            try:
                data = GetNFTData(id.split('/')[1], id.split('/')[2])

                item.num_sales = data['num_sales']
                item.background_color = data['background_color']
                item.image_url = data['image_url']
                item.image_preview_url = data['image_preview_url']
                item.image_thumbnail_url = data['image_thumbnail_url']
                item.image_original_url = data['image_original_url']
                item.animation_url = data['animation_url']
                item.animation_original_url = data['animation_original_url']
                item.name = data['name']
                item.description = data['description']
                item.external_link = data['external_link']


                for trait in data['traits']:
                    trait_ = Trait(id=str(uuid.uuid4()),
                                  trait_type = trait['trait_type'],
                                  display_type = trait['display_type'],
                                  max_value = trait['max_value'],
                                  trait_count = trait['trait_count'],
                                  order = trait['order'],
                                  value = trait['value'],

                                   item = item
                                )

                    session.add(trait_)


                collection_.asset_contract_criteria = data['asset_contract']['address']
                collection_.asset_contract_type = data['asset_contract']['asset_contract_type']
                collection_.chain_identifier = data['asset_contract']['chain_identifier']
                collection_.created_date = data['collection']['created_date']
                collection_.name = data['collection']['name']
                collection_.nft_version = data['asset_contract']['nft_version']
                collection_.opensea_version = data['asset_contract']['opensea_version']
                collection_.owner = data['asset_contract']['owner']
                collection_.schema_name = data['asset_contract']['schema_name']
                collection_.symbol = data['asset_contract']['symbol']
                collection_.total_supply = data['asset_contract']['total_supply']
                collection_.description = data['collection']['description']
                collection_.external_link = data['asset_contract']['external_link']
                collection_.image_url = data['asset_contract']['image_url']
                collection_.default_to_fiat = data['asset_contract']['default_to_fiat']
                collection_.dev_buyer_fee_basis_points = data['collection']['dev_buyer_fee_basis_points']
                collection_.dev_seller_fee_basis_points = data['collection']['dev_seller_fee_basis_points']
                collection_.only_proxied_transfers = data['collection']['only_proxied_transfers']
                collection_.opensea_buyer_fee_basis_points = data['collection']['opensea_buyer_fee_basis_points']
                collection_.opensea_seller_fee_basis_points = data['collection']['opensea_seller_fee_basis_points']
                collection_.buyer_fee_basis_points = data['asset_contract']['buyer_fee_basis_points']
                collection_.seller_fee_basis_points = data['asset_contract']['seller_fee_basis_points']
                collection_.payout_address = data['asset_contract']['payout_address']

                stats = Stat(id=str(uuid.uuid4()),
                             one_minute_volume=data['collection']['stats']['one_minute_volume'],
                            one_minute_change = data['collection']['stats']['one_minute_change'],
                            one_minute_sales = data['collection']['stats']['one_minute_sales'],
                            one_minute_sales_change = data['collection']['stats']['one_minute_sales_change'],
                            one_minute_average_price = data['collection']['stats']['one_minute_average_price'],
                            one_minute_difference = data['collection']['stats']['one_minute_difference'],
                            five_minute_volume = data['collection']['stats']['five_minute_volume'],
                            five_minute_change = data['collection']['stats']['five_minute_change'],
                            five_minute_sales = data['collection']['stats']['five_minute_sales'],
                            five_minute_sales_change = data['collection']['stats']['five_minute_sales_change'],
                            five_minute_average_price = data['collection']['stats']['five_minute_average_price'],
                            five_minute_difference = data['collection']['stats']['five_minute_difference'],
                            fifteen_minute_volume = data['collection']['stats']['fifteen_minute_volume'],
                            fifteen_minute_change = data['collection']['stats']['fifteen_minute_change'],
                            fifteen_minute_sales = data['collection']['stats']['fifteen_minute_sales'],
                            fifteen_minute_sales_change = data['collection']['stats']['fifteen_minute_sales_change'],
                            fifteen_minute_average_price = data['collection']['stats']['fifteen_minute_average_price'],
                            fifteen_minute_difference = data['collection']['stats']['fifteen_minute_difference'],
                            thirty_minute_volume = data['collection']['stats']['thirty_minute_volume'],
                            thirty_minute_change = data['collection']['stats']['thirty_minute_change'],
                            thirty_minute_sales = data['collection']['stats']['thirty_minute_sales'],
                            thirty_minute_sales_change = data['collection']['stats']['thirty_minute_sales_change'],
                            thirty_minute_average_price = data['collection']['stats']['thirty_minute_average_price'],
                            thirty_minute_difference = data['collection']['stats']['thirty_minute_difference'],
                            one_hour_volume = data['collection']['stats']['one_hour_volume'],
                            one_hour_change = data['collection']['stats']['one_hour_change'],
                            one_hour_sales = data['collection']['stats']['one_hour_sales'],
                            one_hour_sales_change = data['collection']['stats']['one_hour_sales_change'],
                            one_hour_average_price = data['collection']['stats']['one_hour_average_price'],
                            one_hour_difference = data['collection']['stats']['one_hour_difference'],
                            six_hour_volume = data['collection']['stats']['six_hour_volume'],
                            six_hour_change = data['collection']['stats']['six_hour_change'],
                            six_hour_sales = data['collection']['stats']['six_hour_sales'],
                            six_hour_sales_change = data['collection']['stats']['six_hour_sales_change'],
                            six_hour_average_price = data['collection']['stats']['six_hour_average_price'],
                            six_hour_difference = data['collection']['stats']['six_hour_difference'],
                            one_day_volume = data['collection']['stats']['one_day_volume'],
                            one_day_change = data['collection']['stats']['one_day_change'],
                            one_day_sales = data['collection']['stats']['one_day_sales'],
                            one_day_sales_change = data['collection']['stats']['one_day_sales_change'],
                            one_day_average_price = data['collection']['stats']['one_day_average_price'],
                            one_day_difference = data['collection']['stats']['one_day_difference'],
                            seven_day_volume = data['collection']['stats']['seven_day_volume'],
                            seven_day_change = data['collection']['stats']['seven_day_change'],
                            seven_day_sales = data['collection']['stats']['seven_day_sales'],
                            seven_day_average_price = data['collection']['stats']['seven_day_average_price'],
                            seven_day_difference = data['collection']['stats']['seven_day_difference'],
                            thirty_day_volume = data['collection']['stats']['thirty_day_volume'],
                            thirty_day_change = data['collection']['stats']['thirty_day_change'],
                            thirty_day_sales = data['collection']['stats']['thirty_day_sales'],
                            thirty_day_average_price = data['collection']['stats']['thirty_day_average_price'],
                            thirty_day_difference = data['collection']['stats']['thirty_day_difference'],
                            total_volume = data['collection']['stats']['total_volume'],
                            total_sales = data['collection']['stats']['total_sales'],
                            total_supply = data['collection']['stats']['total_supply'],
                            count = data['collection']['stats']['count'],
                            num_owners = data['collection']['stats']['num_owners'],
                            average_price = data['collection']['stats']['average_price'],
                            num_reports = data['collection']['stats']['num_reports'],
                            market_cap = data['collection']['stats']['market_cap'],
                            floor_price = data['collection']['stats']['floor_price'],
                )

                collection_.stats = [stats]

                ready_fees = []
                for i in data['collection']['fees']:
                    name = next(iter(i))  # Получение ключа первого уровня ('opensea_fees')
                    address, fee_percentage = next(
                        iter(i[name].items()))  # Получение пары ключ-значение из вложенного словаря

                    fee = Fee(id=str(uuid.uuid4()),
                              name = name,
                              address = address,
                              fee_perccentage = fee_percentage
                    )

                    ready_fees.append(fee)

                collection_.fees = ready_fees
            except:
                pass

        paymentToken = session.query(PaymentToken).filter(PaymentToken.name == payload['payload']['payment_token']['name']).first()
        if paymentToken is None:
            paymentToken = PaymentToken(id=str(uuid.uuid4()),
                                        address=payload['payload']['payment_token']['address'],
                                        decimals=payload['payload']['payment_token']['decimals'],
                                        eth_price=payload['payload']['payment_token']['eth_price'],
                                        name=payload['payload']['payment_token']['name'],
                                        symbol=payload['payload']['payment_token']['symbol'],
                                        usd_price=payload['payload']['payment_token']['usd_price']
                                        )
            session.add(paymentToken)

        cons_ready = []
        for consideration_data in payload['payload']['protocol_data']['parameters']['consideration']:
            consideration = Consideration(id=str(uuid.uuid4()),
                                           endAmount = consideration_data['endAmount'],
                                           identifierOrCriteria = consideration_data['identifierOrCriteria'],
                                           itemType = consideration_data['itemType'],
                                           recipient = consideration_data['recipient'],
                                           startAmount = consideration_data['startAmount'],
                                           token = consideration_data['token'],
            )
            cons_ready.append(consideration)

        protocol_data_offers_ready = []
        for protocol_data_offer in payload['payload']['protocol_data']['parameters']['offer']:
            PD_offer = ProtocolDataOffer(id=str(uuid.uuid4()),
                                     endAmount = protocol_data_offer['endAmount'],
                                     identifierOrCriteria = protocol_data_offer['identifierOrCriteria'],
                                     itemType = protocol_data_offer['itemType'],
                                     startAmount = protocol_data_offer['startAmount'],
                                     token = protocol_data_offer['token'],
                                      )
            protocol_data_offers_ready.append(PD_offer)

        protocol_data = ProtocolData(id = str(uuid.uuid4()),
                                     conduitKey = payload['payload']['protocol_data']['parameters']['conduitKey'],
                                     counter = payload['payload']['protocol_data']['parameters']['counter'],
                                     endTime = payload['payload']['protocol_data']['parameters']['endTime'],
                                     offerer = payload['payload']['protocol_data']['parameters']['offerer'],
                                     orderType = payload['payload']['protocol_data']['parameters']['orderType'],
                                     salt = payload['payload']['protocol_data']['parameters']['salt'],
                                     startTime = payload['payload']['protocol_data']['parameters']['startTime'],
                                     totalOriginalConsiderationItems = payload['payload']['protocol_data']['parameters']['totalOriginalConsiderationItems'],
                                     zone = payload['payload']['protocol_data']['parameters']['zone'],
                                     zoneHash = payload['payload']['protocol_data']['parameters']['zoneHash'],
                                     signature = payload['payload']['protocol_data']['signature'],

                                     protocol_data_offers_ = protocol_data_offers_ready,
                                     considerations_ = cons_ready
                                     )
        session.add(protocol_data)

        listing = Listing(order_hash = payload['payload']['order_hash'],
                          listed_status = True,
                          listing_price = payload['payload']['base_price'],
                          maker = payload['payload']['maker']['address'],
                          listing_expires = dateutil.parser.parse(payload['payload']['expiration_date']),
                          event_timestamp = dateutil.parser.parse(payload['payload']['listing_date']),

                          protocol_data = [protocol_data],
                          payment_token = [paymentToken])

        session.add(listing)

        item.listed_data = [listing]
        session.commit()



    elif payload['event_type'] == 'item_transferred':
        ...

    elif payload['event_type'] == 'order_invalidate':
        ...

    elif payload['event_type'] == 'item_cancelled':

        collection = payload['payload']['collection']['slug']
        collection_ = session.query(Collection).filter(Collection.collection_slug == collection).first()
        if collection_ is None:
            collection_ = Collection(collection_slug=collection)
            session.add(collection_)

        id = payload['payload']['item']['nft_id']

        item = session.query(Item).filter(Item.id == id).first()
        if item is None:
            item = Item(id=id,
                        chain=payload['payload']['item']['chain']['name'],
                        permalink=payload['payload']['item']['permalink'],
                        token_id=payload['payload']['item']['chain']['name'],

                        collection=collection_
                        )

            session.add(item)

            MD = Metadata(id=str(uuid.uuid4()),
                          animation_url=payload['payload']['item']['metadata']['animation_url'],
                          image_url=payload['payload']['item']['metadata']['image_url'],
                          metadata_url=payload['payload']['item']['metadata']['metadata_url'],
                          name=payload['payload']['item']['metadata']['name'],

                          item=item)

            session.add(MD)

            try:
                data = GetNFTData(id.split('/')[1], id.split('/')[2])

                item.num_sales = data['num_sales']
                item.background_color = data['background_color']
                item.image_url = data['image_url']
                item.image_preview_url = data['image_preview_url']
                item.image_thumbnail_url = data['image_thumbnail_url']
                item.image_original_url = data['image_original_url']
                item.animation_url = data['animation_url']
                item.animation_original_url = data['animation_original_url']
                item.name = data['name']
                item.description = data['description']
                item.external_link = data['external_link']

                for trait in data['traits']:
                    trait_ = Trait(id=str(uuid.uuid4()),
                                   trait_type=trait['trait_type'],
                                   display_type=trait['display_type'],
                                   max_value=trait['max_value'],
                                   trait_count=trait['trait_count'],
                                   order=trait['order'],
                                   value=trait['value'],

                                   item=item
                                   )

                    session.add(trait_)

                collection_.asset_contract_criteria = data['asset_contract']['address']
                collection_.asset_contract_type = data['asset_contract']['asset_contract_type']
                collection_.chain_identifier = data['asset_contract']['chain_identifier']
                collection_.created_date = data['collection']['created_date']
                collection_.name = data['collection']['name']
                collection_.nft_version = data['asset_contract']['nft_version']
                collection_.opensea_version = data['asset_contract']['opensea_version']
                collection_.owner = data['asset_contract']['owner']
                collection_.schema_name = data['asset_contract']['schema_name']
                collection_.symbol = data['asset_contract']['symbol']
                collection_.total_supply = data['asset_contract']['total_supply']
                collection_.description = data['collection']['description']
                collection_.external_link = data['asset_contract']['external_link']
                collection_.image_url = data['asset_contract']['image_url']
                collection_.default_to_fiat = data['asset_contract']['default_to_fiat']
                collection_.dev_buyer_fee_basis_points = data['collection']['dev_buyer_fee_basis_points']
                collection_.dev_seller_fee_basis_points = data['collection']['dev_seller_fee_basis_points']
                collection_.only_proxied_transfers = data['collection']['only_proxied_transfers']
                collection_.opensea_buyer_fee_basis_points = data['collection']['opensea_buyer_fee_basis_points']
                collection_.opensea_seller_fee_basis_points = data['collection']['opensea_seller_fee_basis_points']
                collection_.buyer_fee_basis_points = data['asset_contract']['buyer_fee_basis_points']
                collection_.seller_fee_basis_points = data['asset_contract']['seller_fee_basis_points']
                collection_.payout_address = data['asset_contract']['payout_address']

                stats = Stat(id=str(uuid.uuid4()),
                             one_minute_volume=data['collection']['stats']['one_minute_volume'],
                             one_minute_change=data['collection']['stats']['one_minute_change'],
                             one_minute_sales=data['collection']['stats']['one_minute_sales'],
                             one_minute_sales_change=data['collection']['stats']['one_minute_sales_change'],
                             one_minute_average_price=data['collection']['stats']['one_minute_average_price'],
                             one_minute_difference=data['collection']['stats']['one_minute_difference'],
                             five_minute_volume=data['collection']['stats']['five_minute_volume'],
                             five_minute_change=data['collection']['stats']['five_minute_change'],
                             five_minute_sales=data['collection']['stats']['five_minute_sales'],
                             five_minute_sales_change=data['collection']['stats']['five_minute_sales_change'],
                             five_minute_average_price=data['collection']['stats']['five_minute_average_price'],
                             five_minute_difference=data['collection']['stats']['five_minute_difference'],
                             fifteen_minute_volume=data['collection']['stats']['fifteen_minute_volume'],
                             fifteen_minute_change=data['collection']['stats']['fifteen_minute_change'],
                             fifteen_minute_sales=data['collection']['stats']['fifteen_minute_sales'],
                             fifteen_minute_sales_change=data['collection']['stats']['fifteen_minute_sales_change'],
                             fifteen_minute_average_price=data['collection']['stats']['fifteen_minute_average_price'],
                             fifteen_minute_difference=data['collection']['stats']['fifteen_minute_difference'],
                             thirty_minute_volume=data['collection']['stats']['thirty_minute_volume'],
                             thirty_minute_change=data['collection']['stats']['thirty_minute_change'],
                             thirty_minute_sales=data['collection']['stats']['thirty_minute_sales'],
                             thirty_minute_sales_change=data['collection']['stats']['thirty_minute_sales_change'],
                             thirty_minute_average_price=data['collection']['stats']['thirty_minute_average_price'],
                             thirty_minute_difference=data['collection']['stats']['thirty_minute_difference'],
                             one_hour_volume=data['collection']['stats']['one_hour_volume'],
                             one_hour_change=data['collection']['stats']['one_hour_change'],
                             one_hour_sales=data['collection']['stats']['one_hour_sales'],
                             one_hour_sales_change=data['collection']['stats']['one_hour_sales_change'],
                             one_hour_average_price=data['collection']['stats']['one_hour_average_price'],
                             one_hour_difference=data['collection']['stats']['one_hour_difference'],
                             six_hour_volume=data['collection']['stats']['six_hour_volume'],
                             six_hour_change=data['collection']['stats']['six_hour_change'],
                             six_hour_sales=data['collection']['stats']['six_hour_sales'],
                             six_hour_sales_change=data['collection']['stats']['six_hour_sales_change'],
                             six_hour_average_price=data['collection']['stats']['six_hour_average_price'],
                             six_hour_difference=data['collection']['stats']['six_hour_difference'],
                             one_day_volume=data['collection']['stats']['one_day_volume'],
                             one_day_change=data['collection']['stats']['one_day_change'],
                             one_day_sales=data['collection']['stats']['one_day_sales'],
                             one_day_sales_change=data['collection']['stats']['one_day_sales_change'],
                             one_day_average_price=data['collection']['stats']['one_day_average_price'],
                             one_day_difference=data['collection']['stats']['one_day_difference'],
                             seven_day_volume=data['collection']['stats']['seven_day_volume'],
                             seven_day_change=data['collection']['stats']['seven_day_change'],
                             seven_day_sales=data['collection']['stats']['seven_day_sales'],
                             seven_day_average_price=data['collection']['stats']['seven_day_average_price'],
                             seven_day_difference=data['collection']['stats']['seven_day_difference'],
                             thirty_day_volume=data['collection']['stats']['thirty_day_volume'],
                             thirty_day_change=data['collection']['stats']['thirty_day_change'],
                             thirty_day_sales=data['collection']['stats']['thirty_day_sales'],
                             thirty_day_average_price=data['collection']['stats']['thirty_day_average_price'],
                             thirty_day_difference=data['collection']['stats']['thirty_day_difference'],
                             total_volume=data['collection']['stats']['total_volume'],
                             total_sales=data['collection']['stats']['total_sales'],
                             total_supply=data['collection']['stats']['total_supply'],
                             count=data['collection']['stats']['count'],
                             num_owners=data['collection']['stats']['num_owners'],
                             average_price=data['collection']['stats']['average_price'],
                             num_reports=data['collection']['stats']['num_reports'],
                             market_cap=data['collection']['stats']['market_cap'],
                             floor_price=data['collection']['stats']['floor_price'],
                             )

                collection_.stats = [stats]

                ready_fees = []
                for i in data['collection']['fees']:
                    name = next(iter(i))  # Получение ключа первого уровня ('opensea_fees')
                    address, fee_percentage = next(
                        iter(i[name].items()))  # Получение пары ключ-значение из вложенного словаря

                    fee = Fee(id=str(uuid.uuid4()),
                              name=name,
                              address=address,
                              fee_perccentage=fee_percentage
                              )

                    ready_fees.append(fee)

                collection_.fees = ready_fees

            except:
                pass

        paymentToken = session.query(PaymentToken).filter(
            PaymentToken.name == payload['payload']['payment_token']['name']).first()
        if paymentToken is None:
            paymentToken = PaymentToken(id=str(uuid.uuid4()),
                                        address=payload['payload']['payment_token']['address'],
                                        decimals=payload['payload']['payment_token']['decimals'],
                                        eth_price=payload['payload']['payment_token']['eth_price'],
                                        name=payload['payload']['payment_token']['name'],
                                        symbol=payload['payload']['payment_token']['symbol'],
                                        usd_price=payload['payload']['payment_token']['usd_price']
                                        )
            session.add(paymentToken)

        item.listed_data = []

        session.commit()

    elif payload['event_type'] == 'item_sold':

        # pprint(payload)

        collection = payload['payload']['collection']['slug']
        collection_ = session.query(Collection).filter(Collection.collection_slug == collection).first()
        if collection_ is None:
            collection_ = Collection(collection_slug=collection)
            session.add(collection_)

        id = payload['payload']['item']['nft_id']

        item = session.query(Item).filter(Item.id == id).first()
        if item is None:
            item = Item(id=id,
                        chain=payload['payload']['item']['chain']['name'],
                        permalink=payload['payload']['item']['permalink'],
                        token_id=payload['payload']['item']['chain']['name'],

                        collection=collection_
                        )

            session.add(item)

            MD = Metadata(id=str(uuid.uuid4()),
                          animation_url=payload['payload']['item']['metadata']['animation_url'],
                          image_url=payload['payload']['item']['metadata']['image_url'],
                          metadata_url=payload['payload']['item']['metadata']['metadata_url'],
                          name=payload['payload']['item']['metadata']['name'],

                          item=item)

            session.add(MD)

            try:
                data = GetNFTData(id.split('/')[1], id.split('/')[2])

                item.num_sales = data['num_sales']
                item.background_color = data['background_color']
                item.image_url = data['image_url']
                item.image_preview_url = data['image_preview_url']
                item.image_thumbnail_url = data['image_thumbnail_url']
                item.image_original_url = data['image_original_url']
                item.animation_url = data['animation_url']
                item.animation_original_url = data['animation_original_url']
                item.name = data['name']
                item.description = data['description']
                item.external_link = data['external_link']

                for trait in data['traits']:
                    trait_ = Trait(id=str(uuid.uuid4()),
                                   trait_type=trait['trait_type'],
                                   display_type=trait['display_type'],
                                   max_value=trait['max_value'],
                                   trait_count=trait['trait_count'],
                                   order=trait['order'],
                                   value=trait['value'],

                                   item=item
                                   )

                    session.add(trait_)

                collection_.asset_contract_criteria = data['asset_contract']['address']
                collection_.asset_contract_type = data['asset_contract']['asset_contract_type']
                collection_.chain_identifier = data['asset_contract']['chain_identifier']
                collection_.created_date = data['collection']['created_date']
                collection_.name = data['collection']['name']
                collection_.nft_version = data['asset_contract']['nft_version']
                collection_.opensea_version = data['asset_contract']['opensea_version']
                collection_.owner = data['asset_contract']['owner']
                collection_.schema_name = data['asset_contract']['schema_name']
                collection_.symbol = data['asset_contract']['symbol']
                collection_.total_supply = data['asset_contract']['total_supply']
                collection_.description = data['collection']['description']
                collection_.external_link = data['asset_contract']['external_link']
                collection_.image_url = data['asset_contract']['image_url']
                collection_.default_to_fiat = data['asset_contract']['default_to_fiat']
                collection_.dev_buyer_fee_basis_points = data['collection']['dev_buyer_fee_basis_points']
                collection_.dev_seller_fee_basis_points = data['collection']['dev_seller_fee_basis_points']
                collection_.only_proxied_transfers = data['collection']['only_proxied_transfers']
                collection_.opensea_buyer_fee_basis_points = data['collection']['opensea_buyer_fee_basis_points']
                collection_.opensea_seller_fee_basis_points = data['collection']['opensea_seller_fee_basis_points']
                collection_.buyer_fee_basis_points = data['asset_contract']['buyer_fee_basis_points']
                collection_.seller_fee_basis_points = data['asset_contract']['seller_fee_basis_points']
                collection_.payout_address = data['asset_contract']['payout_address']

                stats = Stat(id=str(uuid.uuid4()),
                             one_minute_volume=data['collection']['stats']['one_minute_volume'],
                             one_minute_change=data['collection']['stats']['one_minute_change'],
                             one_minute_sales=data['collection']['stats']['one_minute_sales'],
                             one_minute_sales_change=data['collection']['stats']['one_minute_sales_change'],
                             one_minute_average_price=data['collection']['stats']['one_minute_average_price'],
                             one_minute_difference=data['collection']['stats']['one_minute_difference'],
                             five_minute_volume=data['collection']['stats']['five_minute_volume'],
                             five_minute_change=data['collection']['stats']['five_minute_change'],
                             five_minute_sales=data['collection']['stats']['five_minute_sales'],
                             five_minute_sales_change=data['collection']['stats']['five_minute_sales_change'],
                             five_minute_average_price=data['collection']['stats']['five_minute_average_price'],
                             five_minute_difference=data['collection']['stats']['five_minute_difference'],
                             fifteen_minute_volume=data['collection']['stats']['fifteen_minute_volume'],
                             fifteen_minute_change=data['collection']['stats']['fifteen_minute_change'],
                             fifteen_minute_sales=data['collection']['stats']['fifteen_minute_sales'],
                             fifteen_minute_sales_change=data['collection']['stats']['fifteen_minute_sales_change'],
                             fifteen_minute_average_price=data['collection']['stats']['fifteen_minute_average_price'],
                             fifteen_minute_difference=data['collection']['stats']['fifteen_minute_difference'],
                             thirty_minute_volume=data['collection']['stats']['thirty_minute_volume'],
                             thirty_minute_change=data['collection']['stats']['thirty_minute_change'],
                             thirty_minute_sales=data['collection']['stats']['thirty_minute_sales'],
                             thirty_minute_sales_change=data['collection']['stats']['thirty_minute_sales_change'],
                             thirty_minute_average_price=data['collection']['stats']['thirty_minute_average_price'],
                             thirty_minute_difference=data['collection']['stats']['thirty_minute_difference'],
                             one_hour_volume=data['collection']['stats']['one_hour_volume'],
                             one_hour_change=data['collection']['stats']['one_hour_change'],
                             one_hour_sales=data['collection']['stats']['one_hour_sales'],
                             one_hour_sales_change=data['collection']['stats']['one_hour_sales_change'],
                             one_hour_average_price=data['collection']['stats']['one_hour_average_price'],
                             one_hour_difference=data['collection']['stats']['one_hour_difference'],
                             six_hour_volume=data['collection']['stats']['six_hour_volume'],
                             six_hour_change=data['collection']['stats']['six_hour_change'],
                             six_hour_sales=data['collection']['stats']['six_hour_sales'],
                             six_hour_sales_change=data['collection']['stats']['six_hour_sales_change'],
                             six_hour_average_price=data['collection']['stats']['six_hour_average_price'],
                             six_hour_difference=data['collection']['stats']['six_hour_difference'],
                             one_day_volume=data['collection']['stats']['one_day_volume'],
                             one_day_change=data['collection']['stats']['one_day_change'],
                             one_day_sales=data['collection']['stats']['one_day_sales'],
                             one_day_sales_change=data['collection']['stats']['one_day_sales_change'],
                             one_day_average_price=data['collection']['stats']['one_day_average_price'],
                             one_day_difference=data['collection']['stats']['one_day_difference'],
                             seven_day_volume=data['collection']['stats']['seven_day_volume'],
                             seven_day_change=data['collection']['stats']['seven_day_change'],
                             seven_day_sales=data['collection']['stats']['seven_day_sales'],
                             seven_day_average_price=data['collection']['stats']['seven_day_average_price'],
                             seven_day_difference=data['collection']['stats']['seven_day_difference'],
                             thirty_day_volume=data['collection']['stats']['thirty_day_volume'],
                             thirty_day_change=data['collection']['stats']['thirty_day_change'],
                             thirty_day_sales=data['collection']['stats']['thirty_day_sales'],
                             thirty_day_average_price=data['collection']['stats']['thirty_day_average_price'],
                             thirty_day_difference=data['collection']['stats']['thirty_day_difference'],
                             total_volume=data['collection']['stats']['total_volume'],
                             total_sales=data['collection']['stats']['total_sales'],
                             total_supply=data['collection']['stats']['total_supply'],
                             count=data['collection']['stats']['count'],
                             num_owners=data['collection']['stats']['num_owners'],
                             average_price=data['collection']['stats']['average_price'],
                             num_reports=data['collection']['stats']['num_reports'],
                             market_cap=data['collection']['stats']['market_cap'],
                             floor_price=data['collection']['stats']['floor_price'],
                             )

                collection_.stats = [stats]

                ready_fees = []
                for i in data['collection']['fees']:
                    name = next(iter(i))  # Получение ключа первого уровня ('opensea_fees')
                    address, fee_percentage = next(
                        iter(i[name].items()))  # Получение пары ключ-значение из вложенного словаря

                    fee = Fee(id=str(uuid.uuid4()),
                              name=name,
                              address=address,
                              fee_perccentage=fee_percentage
                              )

                    ready_fees.append(fee)

                collection_.fees = ready_fees

            except:
                print('Error')

                pass

        paymentToken = session.query(PaymentToken).filter(
            PaymentToken.name == payload['payload']['payment_token']['name']).first()
        if paymentToken is None:
            paymentToken = PaymentToken(id=str(uuid.uuid4()),
                                        address=payload['payload']['payment_token']['address'],
                                        decimals=payload['payload']['payment_token']['decimals'],
                                        eth_price=payload['payload']['payment_token']['eth_price'],
                                        name=payload['payload']['payment_token']['name'],
                                        symbol=payload['payload']['payment_token']['symbol'],
                                        usd_price=payload['payload']['payment_token']['usd_price']
                                        )
            session.add(paymentToken)

        item.listed_data = []

        if item.price_history == None:
            item.price_history = f"{payload['payload']['taker']['address']}|{payload['payload']['transaction']['hash']}|{payload['payload']['transaction']['timestamp']}|{payload['payload']['sale_price']};;;"
        else:
            item.price_history += f"{payload['payload']['taker']['address']}|{payload['payload']['transaction']['hash']}|{payload['payload']['transaction']['timestamp']}|{payload['payload']['sale_price']};;;"

        session.commit()

    return

def GetNFTData(address, id) -> dict:

    url = f"https://api.opensea.io/api/v1/asset/{address}/{id}/?include_orders=false"

    response = requests.get(url, headers={'X-API-KEY': api_key})

    # pprint(response.json())
    return response.json()



def thread():

    slugs = []
    with open('SLUGs.txt', 'r') as file:
        for i in file:
            slugs.append(i.rstrip())

    asyncio.set_event_loop(asyncio.new_event_loop())

    Client = OpenseaStreamClient(api_key, Network.MAINNET)

    for slug in slugs:

        Client.onItemReceivedBid(slug, callback)
        Client.onItemListed(slug, callback)
        Client.onItemSold(slug, callback)

        Client.onTraitOffer(slug, callback)
        Client.onItemMetadataUpdated(slug, callback)
        Client.onItemReceivedOffer(slug, callback)
        Client.onCollectionOffer(slug, callback)
        Client.onItemCancelled(slug, callback)
        Client.onOrderInvalidate(slug, callback)
        Client.onOrderRevalidate(slug, callback)
        Client.onItemTransferred(slug, callback)


    Client.startListening()


if __name__ == '__main__':


    # GetNFTData('', 8955)

    while True:
        thread_ = multiprocessing.Process(target=thread, args=())
        thread_.start()

        time.sleep(3600)

        thread_.terminate()
