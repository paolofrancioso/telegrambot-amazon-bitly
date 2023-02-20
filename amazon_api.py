from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException
from response_parser import parse_response
from consts import *
from amazon_paapi import AmazonApi

# function that search amazon products
def search_items(keywords, search_index="All", item_page=1):
    default_api = DefaultApi(
        access_key=AMAZON_ACCESS_KEY,
        secret_key=AMAZON_SECRET_KEY,
        host=AMAZON_HOST,
        region=AMAZON_REGION,
    )

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
        SearchItemsResource.ITEMINFO_FEATURES,
        SearchItemsResource.OFFERS_LISTINGS_PROMOTIONS,
        SearchItemsResource.OFFERS_LISTINGS_CONDITION,
        SearchItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
    ]

    """ Forming request """
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=PARTNER_TAG,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=ITEMS_PER_PAGE,
            resources=search_items_resource,
            item_page=item_page,
            min_saving_percent=MIN_SAVING_PERCENT,
            condition=ITEM_CONDITION,
            min_reviews_rating=MIN_REVIEWS_RATING,
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    try:
        """Sending request"""
        response = default_api.search_items(search_items_request)
        print("Request received")
        res = parse_response(response)

        if response.errors is not None:
            print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
            print("Error code", response.errors[0].code)
            print("Error message", response.errors[0].message)
        return res

    except ApiException as exception:
        print("Error calling PA-API 5.0!")
        print("Status code:", exception.status)
        print("Errors :", exception.body)
        print("Request ID:", exception.headers["x-amzn-RequestId"])

    except TypeError as exception:
        print("TypeError :", exception)

    except ValueError as exception:
        print("ValueError :", exception)

    except Exception as exception:
        print("Exception :", exception)

# function that search amazon product by URL
def search_item(pCode):
    try:
        amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, PARTNER_TAG, COUNTRY_CODE)
        res = parse_response(amazon.get_items([pCode]))
        return res
    
    except Exception as exception:
        print("Exception :", exception)    
