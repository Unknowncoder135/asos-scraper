
import os
import time
import urllib
import urllib.request
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
# ASOS SCRIPT................................................................
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
# mms = driver.findElement(By.xpath("//div[contains(@class, 'D_Gh') and contains(@class, 'D_wG')]")).text
driver = webdriver.Chrome()

master_list = []
main_list = []

# main_url = "https://www.asos.com/only-sons/only-sons-oversized-crew-neck-jumper-with-sketch-print-in-black/prd/24503779?colourwayid=60588537&cid=27110"
# main_url = "https://www.asos.com/adidas-originals/adidas-originals-retro-revival-track-top-in-navy/prd/23889606?colourwayid=60520948&cid=6993"
main_url = "https://www.asos.com/adidas-originals/adidas-originals-retro-revival-track-top-in-navy/prd/23889606?colourwayid=60520948&cid=6993"
# main_url = "https://www.asos.com/asos-design/asos-design-skinny-suit-in-green-tartan-check/grp/54220?cid=27110"
# main_url = "https://www.asos.com/asos-design/asos-design-skinny-suit-jacket-in-green-tartan-check-with-gold-button/prd/22664180"

driver.get(main_url)
time.sleep(2)

ssd= []
# main = finder.find_element_by_css_selector('li.item[aria-label="Product Details"]')
try:
    prod1 = driver.find_element_by_xpath('//*[@id="mix-and-match"]/ul/li[1]/a')
    prod1 = prod1.get_attribute('href')
    ssd.append(prod1)
except:
    prod1 = 'nn'
try:
    prod2 = driver.find_element_by_xpath('//*[@id="mix-and-match"]/ul/li[2]/a')
    prod2 = prod2.get_attribute('href')
    ssd.append(prod2)
except:
    prod2 = 'nn'

print(len(ssd))

if len(ssd)==2:

    for x in range(0,len(ssd)):
        main_url = ssd[x]
        driver.get(ssd[x])
        time.sleep(2)
        url = main_url.split('?')[0]
        url = url.split('/')[-1]
        print(url)
        product_id = int(url)
        api = f'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={url}&store=ROW&currency=GBP&keyStoreDataversion=hgk0y12-29'
        data = requests.get(api).json()
        hh = data[0]

        date_time = hh['productPrice']['startDateTime']
        print(date_time)
        try:
            name = driver.find_element_by_xpath("//*[@id='aside-content']/div[1]/h1").text.strip()
    
        except:
            name = 'not found'
        try:
            curr_price = driver.find_element_by_css_selector(".product-prev-price[data-id='previous-price']").text
            curr_price = curr_price.replace("\u00a3", "")
            curr_price = curr_price.replace("Was", "")
            curr_price = float(curr_price)
        except:
            try:
                curr_price = driver.find_element_by_css_selector(".product-price-discounted[data-id='current-price']").text
                curr_price = curr_price.replace("\u00a3", "")
                curr_price = curr_price.replace("Now", "")
                curr_price = float(curr_price)
            except:
                curr_price = "null"

        # print(price)
        try:
            discount_price = driver.find_element_by_css_selector(".product-price-discounted[data-id='current-price']").text
            discount_price = discount_price.replace("\u00a3", "")
            discount_price = discount_price.replace("Now", "")
            discount_price = float(discount_price)
        except:
            discount_price = "Not Found"

            # print(discount_price)


        try:
            color = driver.find_element_by_class_name("product-colour").text
        except:
            color = "Not Found"


        try:
            free_delivery = driver.find_element_by_xpath(
                "//*[@id='aside-content']/div[1]/div[3]/a").get_attribute('href')
        except:
            free_delivery = "Not Found"

        try:
            ma = driver.find_element_by_id("main-size-select-0")
            drp = Select(ma)
            lens = drp.options
            size = []
            for x in lens:
                ss = x.text
                size.append(ss)
            size = size[1:]
            # print(size)
        except:
            size = "Not Found"


        # print(size)


        try:
            product_code = driver.find_element_by_xpath("//*[@id='product-details-container']/div[2]/div[1]/p").text.strip()

        except:
            product_code = "Not Found"

        # print(product_code)

        try:
            # dic = driver.find_element_by_class_name("product-description")
            main_dic = driver.find_element_by_xpath(
                "//*[@id='product-details-container']/div[1]/div/ul").text
            main_dic = main_dic.replace("\n", ",")

            # print(dic)
        except:
            main_dic = "Not Found"



        # stock = driver.find_element_by_xpath("//*[@id='product-size']/section/div/div[2]/span[2]").text
        # if stock=="":
        #     stock = "IN STOCK"


        try:
            brand = driver.find_element_by_xpath(
                "//*[@id='product-details-container']/div[2]/div[2]/p").text.strip()
            brand = brand.replace('\u2013', '-')
            brand = brand.replace('\u2019', "'")


        except:
            brand = "Not Found"


        try:
            img = driver.find_elements_by_class_name("gallery-image")
            img_list = []

            for x in img:
                mx = x.get_attribute("src")
                img_list.append(mx)
        except:
            img_list = "Not Found"


        try:
            size_fit = driver.find_element_by_xpath(
                "//*[@id='product-details-container']/div[3]/div[1]/p").text
            size_fit = size_fit.replace("\n", "")
            size_fit = size_fit.replace('"', ' ')
            size_fit = size_fit.replace('\u201d', '')
            ss = []
            ss.append(size_fit)
            if ss[0] == "  ":
                size_fit = "Not Found"
        except:
            size_fit = "Not Found"
            # //*[@id="product-details-container"]/div[3]/div[1]
        try:
            look_after_me = driver.find_element_by_xpath(
                "//*[@id='product-details-container']/div[3]/div[2]/p").text
            look_after_me = look_after_me.replace('\n', '')

        except:
            look_after_me = "Not Found"


        try:
            about_me = driver.find_element_by_class_name("about-me").text
            ab = []
            ss.append(size_fit)
            if ab[0] == "":
                about_me = "Not Found"
            about_me = about_me.replace("\n", " ")
            about_me = about_me.replace("ABOUT ME", "")
            # about_me = about_me.replace("\n", "")

        except:
            about_me = "Not Found"

        rating = "null"
        rating_count = 'null'

        # for size variants....

        size_dic = {
            "sizes": size,
            "Product_color": color,
        }


        # for item variants.............


        item_variants = {
            'datetime': date_time,
            "original_price": curr_price,
            "final_price": discount_price,
            "rating": rating,
            "rating_count": rating_count,
            "product_code":product_code,
            "item_brand": brand,
            "look_after_me_section": look_after_me,
            "item_size_fit_section": size_fit,
            "free_delivery_link": free_delivery

        }
        item_variants1 = []
        item_variants1.append(item_variants)


        # for parent variants.................

        parent_dir = {
            "product_id": product_id,
            "name": name,
            "url": main_url,
            "discription": main_dic,
           
            "variants": size_dic,
            "images": img_list,

        }

        # for main_dir................................................................

        main_dir = {
            "item_parent": parent_dir,
            "item_variants": item_variants1,
        }

        master_list.append(main_dir)





if len(ssd)==0:

    url = main_url.split('?')[0]
    url = url.split('/')[-1]
    print(url)


    api = f'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={url}&store=ROW&currency=GBP&keyStoreDataversion=hgk0y12-29'
    data = requests.get(api).json()
    hh = data[0]


    date_time = hh['productPrice']['startDateTime']


    # print(data)

    product_id  = int(url)
    try:
        name = driver.find_element_by_xpath(
            "//*[@id='aside-content']/div[1]/h1").text.strip()
        
    except:
        name = 'not found'


    # print(name)

    try:
        curr_price = driver.find_element_by_css_selector(".product-prev-price[data-id='previous-price']").text
        curr_price = curr_price.replace("\u00a3", "")
        curr_price = curr_price.replace("Was", "")
        curr_price = float(curr_price)
    except:
        try:
            curr_price = driver.find_element_by_css_selector(".product-price-discounted[data-id='current-price']").text
            curr_price = curr_price.replace("\u00a3", "")
            curr_price = curr_price.replace("Now", "")
            curr_price = float(curr_price)
        except:
            curr_price = "null"

    # print(price)
    try:
        discount_price = driver.find_element_by_css_selector(".product-price-discounted[data-id='current-price']").text
        discount_price = discount_price.replace("\u00a3", "")
        discount_price = discount_price.replace("Now", "")
        discount_price = float(discount_price)
    except:
        discount_price = "Not Found"
        # print(discount_price)


    try:
        color = driver.find_element_by_class_name("product-colour").text
    except:
        color = "Not Found"


    # print(color)

    try:
        free_delivery = driver.find_element_by_xpath(
            "//*[@id='aside-content']/div[1]/div[3]/a").get_attribute('href')
    except:
        free_delivery = "Not Found"

    try:
        ma = driver.find_element_by_id("main-size-select-0")
        drp = Select(ma)
        lens = drp.options
        size = []
        for x in lens:
            ss = x.text
            size.append(ss)
        size = size[1:]
        # print(size)
    except:
        size = "Not Found"


    # print(size)


    try:
        product_code = driver.find_element_by_xpath(
            "//*[@id='product-details-container']/div[2]/div[1]/p").text.strip()
    except:
        product_code = "Not Found"

    # print(product_code)

    try:
        # dic = driver.find_element_by_class_name("product-description")
        main_dic = driver.find_element_by_xpath(
            "//*[@id='product-details-container']/div[1]/div/ul").text
        main_dic = main_dic.replace("\n", ",")

        # print(dic)
    except:
        main_dic = "Not Found"



    # stock = driver.find_element_by_xpath("//*[@id='product-size']/section/div/div[2]/span[2]").text
    # if stock=="":
    #     stock = "IN STOCK"


    try:
        brand = driver.find_element_by_xpath(
            "//*[@id='product-details-container']/div[2]/div[2]/p").text.strip()
        brand = brand.replace('\u2013', '-')
        brand = brand.replace('\u2019', "'")


    except:
        brand = "Not Found"


    try:
        img = driver.find_elements_by_class_name("gallery-image")
        img_list = []

        for x in img:
            mx = x.get_attribute("src")
            img_list.append(mx)
    except:
        img_list = "Not Found"


    try:
        size_fit = driver.find_element_by_xpath(
            "//*[@id='product-details-container']/div[3]/div[1]/p").text
        size_fit = size_fit.replace("\n", "")
        size_fit = size_fit.replace('"', ' ')
        size_fit = size_fit.replace('\u201d', '')
        ss = []
        ss.append(size_fit)
        if ss[0] == "  ":
            size_fit = "Not Found"
    except:
        size_fit = "Not Found"
        # //*[@id="product-details-container"]/div[3]/div[1]
    try:
        look_after_me = driver.find_element_by_xpath(
            "//*[@id='product-details-container']/div[3]/div[2]/p").text
        look_after_me = look_after_me.replace('\n', '')

    except:
        look_after_me = "Not Found"


    try:
        about_me = driver.find_element_by_class_name("about-me").text
        ab = []
        ss.append(size_fit)
        if ab[0] == "":
            about_me = "Not Found"
        about_me = about_me.replace("\n", " ")
        about_me = about_me.replace("ABOUT ME", "")
        # about_me = about_me.replace("\n", "")

    except:
        about_me = "Not Found"

    rating = "null"
    rating_count  = "null"

    # for size variants....

    size_dic = {
        "sizes": size,
        "Product_color": color,
    }


    # for item variants.............


    item_variants = {
        'datetime': date_time,
        "original_price": curr_price,
        "final_price": discount_price,
        "product_code": product_code,
        "rating": rating,
        "rating_count": rating_count,
        "item_brand": brand,
        "look_after_me_section": look_after_me,
        "item_size_fit_section": size_fit,
        "free_delivery_link": free_delivery

    }
    item_variants1 = []
    item_variants1.append(item_variants)


    # for parent variants.................

    parent_dir = {
        "product_id": product_id,
        "name": name,
        "url": main_url,
        "discription": main_dic,
        "variants": size_dic,
        "images": img_list,
    }

    # for main_dir................................................................

    main_dir = {
        "item_parent": parent_dir,
        "item_variants": item_variants1,
    }

    master_list.append(main_dir)
# for json formate...................................
df = pd.DataFrame(master_list)
df.to_json('asosOutput.json', orient='records')


print("script run successfully")

driver.quit()
