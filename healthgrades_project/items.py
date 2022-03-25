# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class HealthgradesProjectItem(scrapy.Item):
    url = Field()
    name_tag = Field()
    # speciality = Field()
    gender = Field()
    credential = Field()
    first_name = Field()
    last_name = Field()

    response_count = Field()
    practice_name = Field()

    zip_code = Field()
    state = Field()
    city = Field()
    street_address = Field()

    phone = Field()
    accepting_new_patients = Field()

    five_star_review_count = Field()
    four_star_review_count = Field()
    three_star_review_count = Field()
    two_star_review_count = Field()
    one_star_review_count = Field()

    average_rating = Field()
    speciality1 = Field()
    specialty2 = Field()
    middle_name = Field()

    education = Field()