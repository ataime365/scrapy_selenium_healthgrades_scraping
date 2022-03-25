# -*- coding: utf-8 -*-
import scrapy
from ..utils import open_chrome_headless_browser
from ..items import HealthgradesProjectItem
from time import sleep
from random import randint

class HealthgradesScraperSpider(scrapy.Spider):
    name = 'healthgrades_scraper'
    allowed_domains = ['www.healthgrades.com']
    start_urls = ['https://www.healthgrades.com']

    def parse(self, response):
        link1 = response.xpath("//ul[@class='pop-searches pop-searches--specialties']/li[1]/a/@href").get()
        yield scrapy.Request(url = response.urljoin(link1), callback=self.parse_mid_pages)

    def parse_mid_pages(self, response):
        driver = open_chrome_headless_browser()
        mid_page_url = response.url
        print(mid_page_url)
        driver.get(mid_page_url)
        sleep(randint(10, 15))
        try:
            driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
            sleep(randint(3, 7))
        except Exception:
            pass
        for i in range(0, 2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(randint(3, 6))
        try:
            driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
            sleep(randint(3, 7))
        except Exception:
            pass
        doctors_links = driver.find_elements_by_xpath("//h3[@class='provider-details__provider-name']/a")
        # driver.quit()
        # nn_p = driver.find_element_by_xpath("//a[@aria-label='Page 2']").get_attribute('href')
        # print(nn_p)
        # print('*'*80)
        for link in doctors_links: #[0:5]
            link2 = response.urljoin(link.get_attribute('href'))
            yield scrapy.Request(url = link2, callback=self.parse_individual_pages)
        driver.quit()

        for i in range(2,6):
            next_page = f'https://www.healthgrades.com/usearch?what=family%20medicine&pageNum={i}&sort.provider=bestmatch'
            print('*'*80)
            sleep(randint(2, 4))
            yield scrapy.Request(url = next_page, callback=self.parse_mid_pages)
        

    def parse_individual_pages(self, response):
        
        item = HealthgradesProjectItem()
        item['url'] = response.url
        url = response.url
        print(url)
        # print('*'*80)
        name = response.xpath("//h1[@data-qa-target='ProviderDisplayName']/text()").get()
        item['name_tag'] = response.xpath("//h1[@data-qa-target='ProviderDisplayName']/text()").get()
        cred = name.split(',')
        item['credential'] = cred[1]
        item['first_name'] = cred[0].split(' ')[1]
        item['last_name'] = cred[0].split(' ')[2]
        item['middle_name'] = ''
        item['speciality1'] = response.xpath('//span[@data-qa-target="ProviderDisplaySpeciality"]/text()').get()
        item['specialty2'] = response.xpath("//div[@class='profile-subsection profile-subsection-compressed']//h3[contains(text(), 'Specialt')]/following-sibling::div/ul/li[2]//span/text()").get()
        item['gender'] = response.xpath('//span[@data-qa-target="ProviderDisplayGender"]/text()').get()
        item['average_rating'] = response.xpath("//div[@class='overall-rating']/p/strong/text()").get()
        try:
            response_count = response.xpath('//button[@class="star-reviews-count"]/text()').get()
            if 'Leave' in response_count:
                item['response_count'] = 0
            else:
                item['response_count'] = response_count.split(' ')[0]
        except:
            response_count = response.xpath('//button[@class="star-reviews-count star-reviews-count-sm"]/text()').get() 
            item['response_count'] = response_count.split(' ')[0]    

        addresses = response.xpath("//div[@class='location-box hg-track']/address[@data-qa-target='provider-office-address']/text()").getall()
        address_string = ''
        for ad in addresses:
            address_string = address_string + ad
        # print(address_string)

        five_star_review_count = response.xpath("//div[@class='rating-breakdown']/table/tbody/tr/td[@class='count']/text()").getall()
        if five_star_review_count:
            item['five_star_review_count'] = int(five_star_review_count[1])
            item['four_star_review_count'] = int(five_star_review_count[4])
            item['three_star_review_count'] = int(five_star_review_count[7])
            item['two_star_review_count'] = int(five_star_review_count[10])
            item['one_star_review_count'] = int(five_star_review_count[13])

        #Remove this from the bottom
        # driver = open_chrome_headless_browser()
        # driver.get(url)
        # sleep(randint(10, 15))
        # try:
        #     driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
        #     sleep(randint(3, 5)) 
        # except Exception:
        #     pass
        # try:
        #     driver.find_element_by_xpath("//button[contains(text(), 'No thanks')]").click()
        #     sleep(randint(3, 5))
        # except Exception:
        #     pass

        # if 'Education' in driver.find_element_by_xpath("//div[@class='about-me-collapse-title']/h3").text:
        #     li = []
        #     driver.find_element_by_xpath('//button[@data-qa-target="about-me-education-collapse-toggle"]').click()
        #     sleep(randint(3, 5))
        #     for tt in driver.find_elements_by_xpath("//div[@class='about-me-collapsible']//section[@class='about-me-subsection education-subsection']//div[@class='education-card-content']"):
        #         data_dict = {}
        #         data_dict['timeline_date'] = tt.find_element_by_xpath("//div[@class='timeline-date']").text
        #         data_dict['education_name'] = tt.find_element_by_xpath("//div[@class='education-name']").text
        #         data_dict['education_type'] = tt.find_element_by_xpath("//div[@class='education-completed']").text
        #         li.append(data_dict)
        #     item['education'] = li
        
        if response.xpath("//div[@class='appointment-cta-card']"):
            item['street_address'] = response.xpath("//div[@class='appointment-cta-card']//div[@data-qa-target='provider-office-address']/div/text()").get()
            item['city'] = ' '.join(response.xpath("//div[@class='appointment-cta-card']//div[@data-qa-target='provider-office-address']/following-sibling::span[1]/text()").getall())
            item['state'] = ' '.join(response.xpath("//div[@class='appointment-cta-card']//div[@data-qa-target='provider-office-address']/following-sibling::span[2]/text()").getall())
            item['zip_code'] = ' '.join(response.xpath("//div[@class='appointment-cta-card']//div[@data-qa-target='provider-office-address']/following-sibling::span[3]/text()").getall())
            item['phone'] = response.xpath("//div[@class='appointment-cta-card']//a[@class='click-to-call-button-primary hg-track']/text()").get()
            print(response.xpath("//div[@class='appointment-cta-card']//a[@class='click-to-call-button-primary hg-track']/@href").get())
            item['practice_name'] = response.xpath("//div[@class='appointment-cta-card']//span[@class='address-locator-practice-name js-profile-scroll-link']/strong/text()").get()
            accepting_tag = response.xpath("//div[@class='appointment-cta-card']//span[contains(text(), 'Accepting new patients')]/text()").get()
            if 'Accepting' in accepting_tag:
                item['accepting_new_patients'] = 'Yes'
            else:
                item['accepting_new_patients'] = 'No'

        elif response.xpath("//div[@class='summary-column location-container']//div[@class='accepts-new-patients']"):
            item['zip_code'] = address_string.split(',')[1].split(' ')[-1]
            item['state'] = address_string.split(',')[1].split(' ')[-2]
            item['city'] = address_string.split(',')[0].split(' ')[-1]
            item['street_address'] = ' '.join(address_string.split(',')[0].split(' ')[:-1])
            item['practice_name'] = response.xpath("//div[@class='location-box hg-track']/p[@data-qa-target='provider-practice-name']/text()").get()
            item['phone'] = response.xpath("//div[@class='summary-standard-button-row']/a[@class='toggle-phone-number-button']/text()").get()
            if 'Accepting' in response.xpath("//div[@class='accepts-new-patients']/span/text()").get():
                item['accepting_new_patients'] ='Yes'
            else:
                item['accepting_new_patients'] = 'No'

        else:
            item['zip_code'] = address_string.split(',')[1].split(' ')[-1]
            item['state'] = address_string.split(',')[1].split(' ')[-2]
            item['city'] = address_string.split(',')[0].split(' ')[-1]
            item['street_address'] = ' '.join(address_string.split(',')[0].split(' ')[:-1])
            item['practice_name'] = response.xpath("//div[@class='location-box hg-track']/p[@data-qa-target='provider-practice-name']/text()").get()
            #For phone number here, I first have to use selenium to click
            # driver = open_chrome_headless_browser()
            # driver.get(url)
            # sleep(randint(10, 15))
            # try:
            #     driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
            #     sleep(randint(3, 5)) 
            # except Exception:
            #     pass
            # driver.find_element_by_xpath("//div[@class='summary-standard-button-row']/a").click()
            # sleep(randint(3, 5))
            # ph = driver.find_element_by_xpath("//div[@class='summary-standard-button-row']/a").text
            # item['phone'] = ph
        # driver.quit()

        yield item