import os,time,json,re
from selenium import webdriver
from bs4 import BeautifulSoup
import arabic_reshaper
from bidi.algorithm import get_display

def loading_print():
    for x in range (0,10):  
        b= "Loading" + "." * x
        print (b, end="\r")
        time.sleep(1) 

driver=webdriver.Chrome(executable_path=r'c:\Program Files (x86)\chromedriver.exe')
driver.minimize_window()
os.system('cls')
loading_print()

def converter_farsi_text(text):
    text_reshap=arabic_reshaper.reshape(text)
    convert=get_display(text_reshap)
    return convert


def get_cars():
    driver.get('https://esale.ikco.ir/api/services/OnlineSales/priceList/GetLotterySalesPlanList')
    time.sleep(5)
    source=BeautifulSoup(driver.page_source)
    text_to_dict=json.loads(source.find("body").text)
    list_of_car=text_to_dict['result']['currentLotteryplanList']
    return list_of_car


def print_cars_and_seperate_ditail():
    list_of_car=get_cars()
    cars={}
    for i in range(0,len(list_of_car)):
        car_item=list_of_car[i]
        cars[car_item['rowNumber']]=[car_item['carTypeID'],car_item['sailID'],car_item['carType'],car_item['saleDescription']]
        print('-'*40)
        print(car_item['rowNumber'],end='-')
        print(converter_farsi_text(car_item['carType']),end='---')
        print(converter_farsi_text(car_item['saleDescription']))
    return cars



def get_user_number_of_car():
    cars=print_cars_and_seperate_ditail()
    number_of_cars=cars.keys()
    while True:
        print('*'*40)
        text_input=converter_farsi_text(':لطفا شماره خودرو مورد نظر را وارد کنید')
        user_get=int(input(text_input))
        print('*'*40)
        if user_get in number_of_cars:
            return user_get,cars
        print(f'input invalid please enter number betwin 1 and {len(number_of_cars)}')

       

def main():
    user_get,cars=get_user_number_of_car()
    salid_id=cars[user_get][1]
    car_type_id=cars[user_get][0]
    os.system('cls')
    loading_print()
    driver.get(f'https://esale.ikco.ir/api/services/OnlineSales/priceList/GetLotteryWinnerList?SaleID={salid_id}&CarTypeID={car_type_id}')
    time.sleep(5)
    s=driver.page_source
    count=0
    print('-'*20,end='')
    print(converter_farsi_text(cars[user_get][2]),end='---')
    print(converter_farsi_text(cars[user_get][3]),end='')
    print('-'*20)
    for i in ['مهر','آبان','شهریور','آذر','دی','بهمن','اسفند','فروردین','اردیبهشت','خرداد','مرداد','تیر']:
        find_mounth=re.findall(i,s)
        find_year=re.findall(f'"{i} 14([^"]+)"',s)
        if len(find_mounth)!=0:
            count+=len(find_mounth)
            print(len(find_mounth),end='')
            print(f' :14{find_year[0]}',end='')
            print(converter_farsi_text(f' تعداد تحویل  {i} '))
            print('-'*20)
    print(converter_farsi_text(f' تعداد کل : {count} '))

main()
driver.close()
