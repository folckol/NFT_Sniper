from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Настройка базы данных
engine = create_engine('sqlite:///OpenSeaDB.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Collection(Base):
    __tablename__ = 'collections'

    collection_slug = Column(String, primary_key=True)

    asset_contract_criteria = Column(String)
    asset_contract_type = Column(String)
    chain_identifier = Column(String)
    created_date = Column(String)
    name = Column(String)
    nft_version = Column(String)
    opensea_version = Column(String)
    owner = Column(Integer)
    schema_name = Column(String)
    symbol = Column(String)
    total_supply = Column(String)
    description = Column(String)
    external_link = Column(String)
    image_url = Column(String)
    default_to_fiat = Column(String)
    dev_buyer_fee_basis_points = Column(Integer)
    dev_seller_fee_basis_points = Column(Integer)
    only_proxied_transfers = Column(String)
    opensea_buyer_fee_basis_points = Column(Integer)
    opensea_seller_fee_basis_points = Column(Integer)
    buyer_fee_basis_points = Column(Integer)
    seller_fee_basis_points = Column(Integer)
    payout_address = Column(String)

    fees = relationship("Fee", backref="collection")
    stats = relationship("Stat", backref="collection")
    items = relationship("Item", backref="collection")
    offers = relationship("Offer", backref="collection")

class Fee(Base):
    __tablename__ = 'fees'
    id = Column(String, primary_key=True)

    name = Column(String)
    address = Column(String)
    fee_perccentage = Column(Integer)

    collection_asset_contract_criteria = Column(String, ForeignKey('collections.collection_slug'))

class Stat(Base):
    __tablename__ = 'stats'
    id = Column(String, primary_key=True)

    one_minute_volume = Column(Float)
    one_minute_change = Column(Float)
    one_minute_sales = Column(Float)
    one_minute_sales_change = Column(Float)
    one_minute_average_price = Column(Float)
    one_minute_difference = Column(Float)
    five_minute_volume = Column(Float)
    five_minute_change = Column(Float)
    five_minute_sales = Column(Float)
    five_minute_sales_change = Column(Float)
    five_minute_average_price = Column(Float)
    five_minute_difference = Column(Float)
    fifteen_minute_volume = Column(Float)
    fifteen_minute_change = Column(Float)
    fifteen_minute_sales = Column(Float)
    fifteen_minute_sales_change = Column(Float)
    fifteen_minute_average_price = Column(Float)
    fifteen_minute_difference = Column(Float)
    thirty_minute_volume = Column(Float)
    thirty_minute_change = Column(Float)
    thirty_minute_sales = Column(Float)
    thirty_minute_sales_change = Column(Float)
    thirty_minute_average_price = Column(Float)
    thirty_minute_difference = Column(Float)
    one_hour_volume = Column(Float)
    one_hour_change = Column(Float)
    one_hour_sales = Column(Float)
    one_hour_sales_change = Column(Float)
    one_hour_average_price = Column(Float)
    one_hour_difference = Column(Float)
    six_hour_volume = Column(Float)
    six_hour_change = Column(Float)
    six_hour_sales = Column(Float)
    six_hour_sales_change = Column(Float)
    six_hour_average_price = Column(Float)
    six_hour_difference = Column(Float)
    one_day_volume = Column(Float)
    one_day_change = Column(Float)
    one_day_sales = Column(Float)
    one_day_sales_change = Column(Float)
    one_day_average_price = Column(Float)
    one_day_difference = Column(Float)
    seven_day_volume = Column(Float)
    seven_day_change = Column(Float)
    seven_day_sales = Column(Float)
    seven_day_average_price = Column(Float)
    seven_day_difference = Column(Float)
    thirty_day_volume = Column(Float)
    thirty_day_change = Column(Float)
    thirty_day_sales = Column(Float)
    thirty_day_average_price = Column(Float)
    thirty_day_difference = Column(Float)
    total_volume = Column(Float)
    total_sales = Column(Float)
    total_supply = Column(Float)
    count = Column(Float)
    num_owners = Column(Float)
    average_price = Column(Float)
    num_reports = Column(Float)
    market_cap = Column(Float)
    floor_price = Column(Float)

    collection_asset_contract_criteria = Column(String, ForeignKey('collections.collection_slug'))


class Item(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)

    chain = Column(String)
    permalink = Column(String)
    token_id = Column(String)
    num_sales = Column(Integer)
    background_color = Column(String)
    image_url = Column(String)
    image_preview_url = Column(String)
    image_thumbnail_url = Column(String)
    image_original_url = Column(String)
    animation_url = Column(String)
    animation_original_url = Column(String)
    name = Column(String)
    description = Column(String)
    external_link = Column(String)

    price_history = Column(String)

    listed_data = relationship("Listing", backref="item")
    traits = relationship("Trait", backref="item")
    item_metadata = relationship("Metadata", backref="item")
    item_offers = relationship("Offer", backref="item")

    collection_asset_contract_criteria = Column(String, ForeignKey('collections.collection_slug'))

class Listing(Base):
    __tablename__ = 'listings'
    order_hash = Column(String, primary_key=True)

    listed_status = Column(Boolean)
    listing_price = Column(Integer)
    maker = Column(String)
    listing_expires = Column(DateTime)
    event_timestamp = Column(DateTime)

    protocol_data = relationship("ProtocolData", backref="listing")
    payment_token = relationship("PaymentToken", backref="listing")
    item_id = Column(String, ForeignKey('items.id'))

class Trait(Base):
    __tablename__ = 'traits'
    id = Column(String, primary_key=True)

    trait_type = Column(String)
    display_type = Column(String)
    max_value = Column(String)
    trait_count = Column(Integer)
    order = Column(String)
    value = Column(String)

    item_id = Column(String, ForeignKey('items.id'))

class Metadata(Base):
    __tablename__ = 'metadatas'
    id = Column(String, primary_key=True)

    animation_url = Column(String)
    image_url = Column(String)
    metadata_url = Column(String)
    name = Column(String)

    item_id = Column(String, ForeignKey('items.id'))



class Offer(Base):
    __tablename__ = 'offers'
    # id = Column(String, primary_key=True)

    order_hash = Column(String, primary_key=True)

    maker = Column(String)
    protocol_address = Column(String)
    quantity = Column(Integer)
    taker = Column(String)

    payment_token = relationship("PaymentToken", backref="offer")
    protocol_data = relationship("ProtocolData", backref="offer")

    item_id = Column(String, ForeignKey('items.id'))
    collection_asset_contract_criteria = Column(String, ForeignKey('collections.collection_slug'))

class PaymentToken(Base):
    __tablename__ = 'paymenttokens'
    id = Column(String, primary_key=True)

    address = Column(String)
    decimals = Column(Integer)
    eth_price = Column(Float)
    name = Column(String)
    symbol = Column(String)
    usd_price = Column(Float)

    order_hash_ = Column(String, ForeignKey('listings.order_hash'))
    order_hash_2 = Column(String, ForeignKey('offers.order_hash'))

class ProtocolData(Base):
    __tablename__ = 'protocoldatas'

    id = Column(String, primary_key=True)

    conduitKey = Column(String)
    counter = Column(Integer)
    endTime = Column(String)
    offerer = Column(String)
    orderType = Column(Integer)
    salt = Column(String)
    startTime = Column(String)
    totalOriginalConsiderationItems = Column(Integer)
    zone = Column(String)
    zoneHash = Column(String)
    signature = Column(String)

    protocol_data_offers_ = relationship("ProtocolDataOffer", backref="protocoldata")
    considerations_ = relationship("Consideration", backref="protocoldata")

    order_hash_ = Column(String, ForeignKey('listings.order_hash'))
    order_hash_2 = Column(String, ForeignKey('offers.order_hash'))

class Consideration(Base):
    __tablename__ = 'considerations'
    id = Column(String, primary_key=True)

    endAmount = Column(String)
    identifierOrCriteria = Column(String)
    itemType = Column(Integer)
    recipient = Column(String)
    startAmount = Column(String)
    token = Column(String)

    protocol_data_ = Column(String, ForeignKey('protocoldatas.conduitKey'))


class ProtocolDataOffer(Base):
    __tablename__ = 'protocol_data_offers'
    id = Column(String, primary_key=True)

    endAmount = Column(String)
    identifierOrCriteria = Column(String)
    itemType = Column(Integer)
    startAmount = Column(String)
    token = Column(String)

    protocol_data_ = Column(String, ForeignKey('protocoldatas.conduitKey'))



if __name__ == '__main__':

    Base.metadata.create_all(engine)