import datetime
import random
import ssl
import time
from pprint import pprint
from threading import Thread

import capmonster_python
import requests
import cloudscraper
import tls_client
from capmonster_python import RecaptchaV2Task, RecaptchaV3Task

from bs4 import BeautifulSoup
from eth_account.messages import encode_defunct
from tqdm import tqdm
from web3.auto import w3
import imaplib
import email
from email.header import decode_header
import re

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

class OpenSea:

    def __init__(self, proxy, address, private):

        proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"

        self.proxy = {'http': proxy, 'https': proxy}
        self.address = address
        self.private = private

        self.session = tls_client.Session(

            client_identifier="chrome112",

            random_tls_extension_order=True

        )
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()



    def execute_task(self):

        print('Go')

        payload = {"id":"EventHistoryPaginationQuery",
                   "query":"query EventHistoryPaginationQuery(\n  $archetype: ArchetypeInputType\n  $bundle: BundleSlug\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collections: [CollectionSlug!]\n  $count: Int = 16\n  $cursor: String\n  $eventTimestamp_Gt: DateTime\n  $eventTypes: [EventType!]\n  $identity: IdentityInputType\n  $isRarityExpansionEnabled: Boolean!\n  $rarityFilter: RarityFilterType\n  $showAll: Boolean = false\n  $stringTraits: [TraitInputType!]\n) {\n  ...EventHistory_data_2Weyxc\n}\n\nfragment AccountLink_data on AccountType {\n  address\n  config\n  isCompromised\n  user {\n    publicUsername\n    id\n  }\n  displayName\n  ...ProfileImage_data\n  ...wallet_accountKey\n  ...accounts_url\n}\n\nfragment AssetMediaAnimation_asset on AssetType {\n  ...AssetMediaImage_asset\n  ...AssetMediaContainer_asset\n  ...AssetMediaPlaceholderImage_asset\n}\n\nfragment AssetMediaAudio_asset on AssetType {\n  backgroundColor\n  ...AssetMediaImage_asset\n}\n\nfragment AssetMediaContainer_asset on AssetType {\n  backgroundColor\n  ...AssetMediaEditions_asset_1mZMwQ\n  collection {\n    ...useIsRarityEnabled_collection\n    id\n  }\n}\n\nfragment AssetMediaContainer_asset_1LNk0S on AssetType {\n  backgroundColor\n  ...AssetMediaEditions_asset_1mZMwQ\n  collection {\n    ...useIsRarityEnabled_collection\n    id\n  }\n}\n\nfragment AssetMediaContainer_asset_4a3mm5 on AssetType {\n  backgroundColor\n  ...AssetMediaEditions_asset_1mZMwQ\n  defaultRarityData {\n    ...RarityIndicator_data\n    id\n  }\n  collection {\n    ...useIsRarityEnabled_collection\n    id\n  }\n}\n\nfragment AssetMediaEditions_asset_1mZMwQ on AssetType {\n  decimals\n}\n\nfragment AssetMediaImage_asset on AssetType {\n  backgroundColor\n  imageUrl\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n}\n\nfragment AssetMediaPlaceholderImage_asset on AssetType {\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n}\n\nfragment AssetMediaVideo_asset on AssetType {\n  backgroundColor\n  ...AssetMediaImage_asset\n}\n\nfragment AssetMediaWebgl_asset on AssetType {\n  backgroundColor\n  ...AssetMediaImage_asset\n}\n\nfragment AssetMedia_asset on AssetType {\n  animationUrl\n  displayImageUrl\n  imageUrl\n  isDelisted\n  ...AssetMediaAnimation_asset\n  ...AssetMediaAudio_asset\n  ...AssetMediaContainer_asset_1LNk0S\n  ...AssetMediaImage_asset\n  ...AssetMediaPlaceholderImage_asset\n  ...AssetMediaVideo_asset\n  ...AssetMediaWebgl_asset\n}\n\nfragment AssetMedia_asset_5MxNd on AssetType {\n  animationUrl\n  displayImageUrl\n  imageUrl\n  isDelisted\n  ...AssetMediaAnimation_asset\n  ...AssetMediaAudio_asset\n  ...AssetMediaContainer_asset_4a3mm5\n  ...AssetMediaImage_asset\n  ...AssetMediaPlaceholderImage_asset\n  ...AssetMediaVideo_asset\n  ...AssetMediaWebgl_asset\n}\n\nfragment CollectionCell_collection on CollectionType {\n  name\n  imageUrl\n  isVerified\n  ...collection_url\n}\n\nfragment CollectionCell_trait on TraitType {\n  traitType\n  value\n}\n\nfragment CollectionLink_assetContract on AssetContractType {\n  address\n  blockExplorerLink\n}\n\nfragment CollectionLink_collection on CollectionType {\n  name\n  slug\n  verificationStatus\n  ...collection_url\n}\n\nfragment EventHistory_data_2Weyxc on Query {\n  eventActivity(after: $cursor, bundle: $bundle, archetype: $archetype, first: $count, categories: $categories, collections: $collections, chains: $chains, eventTypes: $eventTypes, identity: $identity, includeHidden: true, stringTraits: $stringTraits, eventTimestamp_Gt: $eventTimestamp_Gt, rarityFilter: $rarityFilter) {\n    edges {\n      node {\n        collection {\n          ...CollectionCell_collection\n          id\n        }\n        traitCriteria {\n          ...CollectionCell_trait\n          id\n        }\n        itemQuantity\n        item @include(if: $showAll) {\n          __typename\n          relayId\n          verificationStatus\n          ...ItemCell_data\n          ...item_url\n          ...PortfolioTableItemCellTooltip_item\n          ... on AssetType {\n            defaultRarityData @include(if: $isRarityExpansionEnabled) {\n              rank\n              id\n            }\n            collection {\n              ...CollectionLink_collection\n              id\n            }\n            assetContract {\n              ...CollectionLink_assetContract\n              id\n            }\n          }\n          ... on AssetBundleType {\n            bundleCollection: collection {\n              ...CollectionLink_collection\n              id\n            }\n          }\n          ... on Node {\n            __isNode: __typename\n            id\n          }\n        }\n        relayId\n        eventTimestamp\n        eventType\n        orderStatus\n        customEventName\n        ...utilsAssetEventLabel\n        creatorFee {\n          unit\n        }\n        devFeePaymentEvent {\n          ...EventTimestamp_data\n          id\n        }\n        fromAccount {\n          address\n          ...AccountLink_data\n          id\n        }\n        perUnitPrice {\n          unit\n          eth\n          usd\n        }\n        endingPriceType {\n          unit\n        }\n        priceType {\n          unit\n        }\n        payment {\n          ...TokenPricePayment\n          id\n        }\n        seller {\n          ...AccountLink_data\n          id\n        }\n        sellOrder {\n          taker {\n            __typename\n            id\n          }\n          id\n        }\n        toAccount {\n          ...AccountLink_data\n          id\n        }\n        winnerAccount {\n          ...AccountLink_data\n          id\n        }\n        ...EventTimestamp_data\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment EventTimestamp_data on AssetEventType {\n  eventTimestamp\n  transaction {\n    blockExplorerLink\n    id\n  }\n}\n\nfragment ItemCell_data on ItemType {\n  __isItemType: __typename\n  __typename\n  displayName\n  ...item_url\n  ...PortfolioTableItemCellTooltip_item\n  ... on AssetType {\n    ...AssetMedia_asset\n  }\n  ... on AssetBundleType {\n    assetQuantities(first: 30) {\n      edges {\n        node {\n          asset {\n            ...AssetMedia_asset\n            id\n          }\n          relayId\n          id\n        }\n      }\n    }\n  }\n}\n\nfragment PortfolioTableItemCellTooltip_item on ItemType {\n  __isItemType: __typename\n  __typename\n  ...AssetMedia_asset_5MxNd\n  ...PortfolioTableTraitTable_asset\n  ...asset_url\n}\n\nfragment PortfolioTableTraitTable_asset on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  isCurrentlyFungible\n  tokenId\n  ...asset_url\n}\n\nfragment ProfileImage_data on AccountType {\n  imageUrl\n}\n\nfragment RarityIndicator_data on RarityDataType {\n  rank\n  rankPercentile\n  rankCount\n  maxRank\n}\n\nfragment TokenPricePayment on PaymentAssetType {\n  symbol\n}\n\nfragment accounts_url on AccountType {\n  address\n  user {\n    publicUsername\n    id\n  }\n}\n\nfragment asset_url on AssetType {\n  assetContract {\n    address\n    id\n  }\n  tokenId\n  chain {\n    identifier\n  }\n}\n\nfragment bundle_url on AssetBundleType {\n  slug\n  chain {\n    identifier\n  }\n}\n\nfragment collection_url on CollectionType {\n  slug\n  isCategory\n}\n\nfragment item_url on ItemType {\n  __isItemType: __typename\n  __typename\n  ... on AssetType {\n    ...asset_url\n  }\n  ... on AssetBundleType {\n    ...bundle_url\n  }\n}\n\nfragment useIsRarityEnabled_collection on CollectionType {\n  slug\n  enabledRarities\n}\n\nfragment utilsAssetEventLabel on AssetEventType {\n  isMint\n  isAirdrop\n  eventType\n}\n\nfragment wallet_accountKey on AccountType {\n  address\n}\n",
                   "variables":
                       {"archetype":None,
                        "bundle":None,
                        "categories":None,
                        "chains":None,
                        "collections":["link3-mini-shard-bnb"],
                        "count":16,
                        "cursor":None,
                        "eventTimestamp_Gt":"2023-04-04T17:35:46.664Z",
                        "eventTypes":["AUCTION_CREATED"],
                        "identity":None,
                        "isRarityExpansionEnabled":True,
                        "rarityFilter":None,
                        "showAll":True,
                        "stringTraits":None}}

        self.session.headers.update({'x-signed-query': ''})

        while True:

            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            print(formatted_date)

            try:
                response = self.session.post('https://opensea.io/__api/graphql/', json=payload)
                if response.json()['data']['eventActivity']['edges'][0]['node']['fromAccount']['address'] != '0x7ba3b8b2b31142cff00ba88780b80a8e9c7e2753':


                    pprint(response.json()['data']['eventActivity']['edges'][0])
                    return
                time.sleep(0.001)
            except:
                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
                print(f'Ошибка {formatted_date}')


    def Login(self):
        self.session.headers.update({'x-app-id': 'opensea-web',
                                     'x-viewer-address': self.address.lower(),
                                     'x-build-id': '6c8e2e948aede10c1233faaf8e48211ad8831596',
                                     'x-signed-query': '05649d324b3f3db988d5065ea33599bca390adf00e3f46952dd59ff5cc61e1e0',
                                     'accept': '*/*',
                                     'origin': 'https://opensea.io',
                                     'referer': 'https://opensea.io/'})

        payload = {"id":"challengeLoginMessageQuery",
                   "query":"query challengeLoginMessageQuery(\n  $address: AddressScalar!\n) {\n  auth {\n    loginMessage(address: $address)\n  }\n}\n",
                   "variables":{"address":self.address.lower()}}
        response = self.session.post('https://opensea.io/__api/graphql/', json=payload)
        message = response.json()['data']['auth']['loginMessage']
        # print(message)

        signed_message = w3.eth.account.sign_message(encode_defunct(text=message), private_key=self.private)
        self.signature = signed_message["signature"].hex()

        self.session.headers.update({'x-signed-query': '804a717e08ab2f12de3752b428dd9b6fd5d006f26e9f17ec4f4805db69b66e96'})


        payload = {"id":"authLoginMutation",
                   "query":"mutation authLoginMutation(\n  $address: AddressScalar!\n  $message: String!\n  $signature: String!\n  $chain: ChainScalar\n) {\n  auth {\n    login(address: $address, message: $message, signature: $signature, chain: $chain) {\n      token\n      account {\n        address\n        moonpayKycStatus\n        moonpayKycRejectType\n        isEmployee\n        id\n      }\n    }\n  }\n}\n",
                   "variables":
                       {"address":self.address.lower(),
                        "message":message,
                        "signature":self.signature.lower(),
                        "chain":"ETHEREUM"}}

        response = self.session.post('https://opensea.io/__api/graphql/', json=payload)
        token = response.json()['data']['auth']['login']['token']

        self.session.headers.update({'authorization': f'JWT {token}'})




    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-None-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-None-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-None-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-None-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-None-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


if __name__ == '__main__':
    acc = OpenSea(proxy='',
            address='',
            private='')

    acc.Login()
    acc.execute_task()