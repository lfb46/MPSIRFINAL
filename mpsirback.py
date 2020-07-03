import math
import firebase_admin
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials
from firebase_admin import db
import sys

#SALES LISTSss
salesAddreses = []
salesPrices = []
coverSalesPhotos = []
fullSalesPhotos = []
salesLinks = []
salesBeds = []
salesBaths = []
salesArea = []
salesDesc = []
salesAmenities = []
salesAgents = []

#RENTAL LISTS
rentalAddreses = []
rentalPrices = []
coverRentalPhotos = []
fullRentalPhotos = []
rentalLinks = []
rentalBeds = []
rentalBaths = []
rentalArea = []
rentalDesc = []
rentalAmenities = []


#THIS STARTS SALES SCRAPING
#MAKE SOUP FOR SALES SCRAPES
page = requests.get("https://www.themaurypeople.com/nantucket-real-estate?filter_waterfront=&filter_pool_type=&filter_mpsir=&filter_vtour=&filter_search=&filter_beds=&filter_baths=&filter_price_min=&filter_price_max=&filter_cat=&filter_region%5B%5D=&filter_sorted=p.created&filter_direction=DESC&commit=")
soup = BeautifulSoup(page.content, 'html.parser')
totalNumSalesHouses = soup.find_all('span', { "class" : "hidden-phone" })[0].text
totalNumSalesHouses = int(totalNumSalesHouses[totalNumSalesHouses.find("of")+2:].strip())
if (totalNumSalesHouses%30 > 0):
    salesRange = math.floor(totalNumSalesHouses/30)+1
else:
    salesRange = math.floor(totalNumSalesHouses/30)
print(totalNumSalesHouses)
for scrapeSalesNum in range(salesRange):
    page = requests.get("https://www.themaurypeople.com/nantucket-real-estate?filter_region[0]=&filter_sorted=p.created&filter_direction=DESC&start=" +  str(scrapeSalesNum*30))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(scrapeSalesNum)
    #GET THE SALESADDRESES
    salesAddresesRaw = soup.find_all('a', { "class" : "gridaddress" })
    for address in salesAddresesRaw:
        salesAddreses.append(address.text.replace('\n', ''))
        salesLinks.append("https://www.themaurypeople.com/" + address["href"])
    coverPhotoSoup = soup.find_all('img', { "class" : "img-polaroid ip-overview-thumb"})
    for photo in coverPhotoSoup:
        coverSalesPhotos.append(photo["src"].replace("https://linkvac.s3.amazonaws.com/photos/", "")strip())
    #GET THE SALESPRICES
    salesPricesRaw = soup.find_all('span', { "class" : "ip-newprice" })
    for price in salesPricesRaw:
        salesPrices.append(price.text)
    
    salesBedBath = soup.find_all('div', { "class" : "griddetailslg" })
    for detail in salesBedBath:
        if "BEDROOMS" in detail.text:
            salesBeds.append(detail.text.replace('BEDROOMS', '').replace('\n', ''))
        if "BATHROOMS" in detail.text:
          if '/' in detail.text:
            salesBaths.append(detail.text.replace('BATHROOMS', '').replace('\n', '').split('/', 1)[0] + '.5')
          else:
            salesBaths.append(detail.text.replace('BATHROOMS', '').replace('\n', ''))
print(salesBeds)
print(salesBaths)
#GET DETAILS
#for list in fullSalesPhotos:
    #coverSalesPhotos.append(list[0])
for link in salesLinks:
    tempcounter = 0
    detailsList = []
    tempList = []
    tempList2 = []
    pageDetail = requests.get(link)
    soupDetail = BeautifulSoup(pageDetail.content, 'html.parser')
    salesDesc.append(soupDetail.find_all('div', { "class" : "pull-left ip-desc-wrapper" })[0].text)
    detailsList = soupDetail.find_all('div', { "class" : "exdetailslg" })
    #landBool = 0
    for detail in detailsList:
        if "AREA" in detail.text:
            salesArea.append(detail.text.replace('AREA', ''))
    stext = soupDetail.text.lower()
    if "central a/c" in stext:
        tempList2.append("Central A/C")
    if "deck" in stext:
        tempList2.append("Deck")
    if "garden" in stext:
        tempList2.append("Garden")
    if "patio" in stext:
        tempList2.append("Patio")
    if "gym" in stext:
        tempList2.append("Gym")
    if "private pool" in stext:
        tempList2.append("Private Pool")
    if "outdoor shower" in stext:
        tempList2.append("Outdoor Shower")
    if "private tennis court" in stext:
        tempList2.append("Private Tennis Court")
    if "waterviews" in stext or "water views" in stext:
        tempList2.append("Waterviews")
    if "waterfront" in stext:
        tempList2.append("Waterfront")
    if "washer" in stext:
        tempList2.append("Washer")
    if "dryer" in stext:
        tempList2.append("Dryer")
    if "single family" in stext or "condo" in stext or "commercial" in stext or "co-op" in stext:
        tempList2.append("Single Family")
    else:
        tempList2.append("Land")
    salesAmenities.append(tempList2)
    fullPhotoSoup = soupDetail.find_all('a', { "data-fancybox" : "gallery" })
    for photo in fullPhotoSoup:
          tempList.append(photo["href"].replace("https://linkvac.s3.amazonaws.com/photos/", "").strip())
    fullSalesPhotos.append(tempList)
    tempcounter+=1
    #print(tempList)
print(salesAddreses)
print(salesPrices)
print(salesBeds)
print(salesArea)
print(salesAmenities)
#print(fullSalesPhotos)
#THIS STARTS RENTAL SCRAPING
#MAKE SOUP FOR RENTAL SCRAPES
page = requests.get("https://www.themaurypeople.com/nantucket-rentals?start=")
soup = BeautifulSoup(page.content, 'html.parser')
totalNumRentalHouses = soup.find_all('span', { "class" : "hidden-phone" })[0].text
totalNumRentalHouses = int(totalNumRentalHouses[totalNumRentalHouses.find("of")+2:].strip())
if (totalNumRentalHouses%30 > 0):
    rentalRange = math.floor(totalNumRentalHouses/30)+1
else:
    rentalRange = math.floor(totalNumRentalHouses/30)
print(totalNumRentalHouses)
if (rentalRange >= 5):
 rentalRange = 5
for scrapeRentalNum in range(rentalRange):
    page = requests.get("https://www.themaurypeople.com/nantucket-rentals?start=" + str(scrapeRentalNum*30))
    soup = BeautifulSoup(page.content, 'html.parser')
    #GET THE RENTALADDRESES
    rentalAddresesRaw = soup.find_all('a', { "class" : "gridaddress" })
    for address in rentalAddresesRaw:
        rentalAddreses.append(address.text.replace('\n', ''))
        rentalLinks.append("https://www.themaurypeople.com/" + address["href"])
    print(rentalAddreses)
    #GET THE RENTALPRICES
    rentalPricesRaw = soup.find_all('span', { "class" : "priceclass" })
    for price in rentalPricesRaw:
     tempvar = price.text[1:].split('$', 1)[0].strip()
     if 'price' in tempvar:
         rentalPrices.append('C' + tempvar)
     else:
         rentalPrices.append('$' + tempvar)
    print(rentalPrices)
print(rentalAddreses)
#GET DETAILS
for link in rentalLinks:
    tempcounter = 0
    detailsList = []
    tempList = []
    tempList2 = []
    pageDetail = requests.get(link)
    soupDetail = BeautifulSoup(pageDetail.content, 'html.parser')
    rentalDesc.append(soupDetail.find_all('div', { "class" : "pull-left ip-desc-wrapper" })[0].text)
    detailsList = soupDetail.find_all('div', { "class" : "exdetailslg" })
    count = 0
    for detail in detailsList:
          if "BEDROOMS" in detail.text:
              rentalBeds.append(detail.text.replace('BEDROOMS', ''))
          elif "BATHROOMS" in detail.text:
              rentalBaths.append(detail.text.replace('BATHROOMS', ''))
          elif "AREA" in detail.text:
              rentalArea.append(detail.text.replace('AREA', ''))
          else:
              count = count
          count+=1
    stext = soupDetail.text.lower()
    if "central a/c" in stext:
        tempList2.append("Central A/C")
    if "deck" in stext:
        tempList2.append("Deck")
    if "garden" in stext:
        tempList2.append("Garden")
    if "patio" in stext:
        tempList2.append("Patio")
    if "gym" in stext:
        tempList2.append("Gym")
    if "pool" in stext:
        tempList2.append("Pool")
    if "outdoor shower" in stext:
        tempList2.append("Outdoor Shower")
    if "private tennis court" in stext:
        tempList2.append("Private Tennis Court")
    if "beach umbrella" in stext:
        tempList2.append("Beach Umbrella")
    if "coffee maker" in stext:
        tempList2.append("Coffee Maker")
    if "fireplace" in stext:
        tempList2.append("Fireplace")
    if "lobster pot" in stext:
        tempList2.append("Lobster Pot")
    if "waterviews" in stext or "water views" in stext:
        tempList2.append("Waterviews")
    if "waterfront" in stext:
        tempList2.append("Waterfront")
    if "pets" in stext:
        tempList2.append("Pets Allowed")
    if "a/c" in stext:
        tempList2.append("A/C")
    tempList2.append("Washer")
    tempList2.append("Dryer")
    rentalAmenities.append(tempList2)
    fullPhotoSoup = soupDetail.find_all('img', { "class" : "lazy" })
    for photo in fullPhotoSoup:
       tempList.append(photo["data-src"].replace("https://mpsir-rentals.com/media/com_iproperty/pictures/", "").strip())
    fullRentalPhotos.append(tempList)
    tempcounter+=1
for list in fullRentalPhotos:
   coverRentalPhotos.append(list[0])

print("Updating Database")

#UPDATE THE DATABASE
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "mpsir-5bbcd",
  "private_key_id": "cabfe05f588fed614da6d059fc285822d2094aaf",
  "private_key": "-----BEGIN PRIVATE KEY-----\n" + str(sys.argv[1]) + "\n" + str(sys.argv[2]) + "\n" + str(sys.argv[3]) +  "\n" + str(sys.argv[4]) + "\npyp+z6iikta5074jcC41+JxZDL/TsEmPIk3nOWQCB/Jg4L59BfF8JzPVRIRex7e7\nx6zhoOY6pDQmEH0HENyA1Eo37nuYa2yA+IwQfiN/1gFGqSTBHBFD0vgzkf6eLCon\ndj1If1dVAgMBAAECggEAEiR5ZNCaLnx+2cL1rAxO6hx5zDN6C6523/381M89Uqa5\nCGFW9xQZhK5wwin2lsB02EVBgFG8LDYL9nJwShvmCm+rC+fIv6eSmzb/a1XR3elx\n0fnloRiChKuADLc4h6MaErIp8gZE2N2yqfy/upf823/71u0AIzYnogMRyATEEjhk\n+vkjlt1YeFr1hqzyZympGGUhYcgBEjhoErLiWC/Y31wE74dHhSrPuxDVkiZj9oN0\nkg1/Co0NkiWAiHRUnb6xI1Xbw5deGYp+ZmDcilz1cRHl6e2MBx5NsklTI2spt82e\nwetAlFm554hdupm4qceLE3qRcPBewsXyiE8JCucQgQKBgQD32CxFWqONb+z5CIFv\nVp2I6fae5FnwRiUbqt5I/SiKQ36B27EoPaSW0Q/TS6iKwYIKKyQYVOvA25brThYL\nFMbYOh4v5n0B0eBtDGPmWtJeADKxokVS7TDlglb4nSZM7FDhVgoriv0UyV9Nf66Z\n" + str(sys.argv[5]) + "\nUWroj2lN/C1YeKMG8Dt1PBdNgbChARUabjV2T9xX35C8f//Btcdf0l2S236HGqCT\nLtIPb1fQOABCeSv9ieEDWV/rbjHonCpU5Jjop1kZdgT6iUPqO6mEDTBp4BPfrrql\nEh3eC5iwdQKBgFsmxwluz24KNwZUCX6QRXoASjKf2zASLD2jtwLzEIDhV9qcmOgq\n26iYFRDp53+4sYHZ4fmM6fPRDw1Vd6f1qTgHD+kgBOOxc6/HecpTpsDpo7tO6d4Y\n" + str(sys.argv[6]) + "\nOfMWrfnu1voXwxDM9gYELgzHWWehrk4ZtLVpLeagh7UQ6yKPJPNOJnM1oLCvUgRa\n346VACEJlxZkaWFvU7MhsjposLdxJHhEPdgrGtBJd/SXK3qIPonh5qrlNbL0GJEo\n2Zhao9QhWoSLodwL1zZxGcG+cM9jUNzLDRc/vE0CgYAQB+5fzfVm0+GgpG/6crA6\naKseaVE1ff5fxIoTaBfAZ7kzHwAgaM2Jfav5b2UOet1Bjzddwn33IbuhIxInO38X\nhEeuGZAHYiRLs8U0ahjsbvTVKiuGLalAW0Yp8ai5Zq8Url3nCZnuK0RG9+uvo6cf\n8gua/vmdobWaAwMMyFlk3Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-n7q1u@mpsir-5bbcd.iam.gserviceaccount.com",
  "client_id": "109034846376944652581",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-n7q1u%40mpsir-5bbcd.iam.gserviceaccount.com"
})
# INITIALIZE THE APP WITHIN THE SERVICE ACCOUNT GRANTING ADMIN PRIVILIGES
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mpsir-5bbcd.firebaseio.com/'
})


salesRef = db.reference('Sales')
salesRef.update({
    'Addreses': salesAddreses,
    'Prices': salesPrices,
    'coverPhotos': coverSalesPhotos,
    'fullPhotos': fullSalesPhotos,
    'Area': salesArea,
    'Beds': salesBeds,
    'Baths': salesBaths,
    'Desc': salesDesc,
    'Amenities': salesAmenities,
    'AgentEmails': salesAgents
})
rentalsRef = db.reference('Rentals')
rentalsRef.update({
    'Addreses': rentalAddreses,
    'Prices': rentalPrices,
    'coverPhotos': coverRentalPhotos,
    'fullPhotos': fullRentalPhotos,
    'Area': rentalArea,
    'Beds': rentalBeds,
    'Baths': rentalBaths,
    'Desc': rentalDesc,
    'Amenities': rentalAmenities
})
