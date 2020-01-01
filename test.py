from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import os
import sys

featuresList = []
imagesList = []

# URL to web scrap from.
page_url = sys.argv[1]

cmd = 'wget -O web ' + page_url
os.system(cmd)

# open webpage
file = open('web', mode='r')
# read all lines at once
html = file.read()
# close the file
file.close()

# parses html into a soup data structure to traverse html
page_soup = soup(html, "html.parser")

# find name of the product
productName_container = page_soup.findAll("span", {"id": "productTitle"})
productName = productName_container[0].text.strip()

# find price of the product
productPrice_container = page_soup.find_all(
    "span", {"id": "priceblock_ourprice"})
if productPrice_container:
    productPrice = productPrice_container[0].text.strip().replace("\xa0", "")
elif productPrice_container:
    productPrice = page_soup.find_all("span", {"id": "priceblock_dealprice"})[
        0].text.strip().replace("\xa0", "")
else:
    productPrice = page_soup.find_all("span", {"id": "priceblock_saleprice"})[
        0].text.strip().replace("\xa0", "")

# find features of the product
productFeature_container = page_soup.find_all("div", {"id": "feature-bullets"})
for productFeature in productFeature_container:
    features = productFeature.find_all(
        "span", {"class": "a-list-item"})
    i = 0
    for feature in features:
        featuresList.insert(i, feature.text.strip())
        i = i+1

# find images of the product
productImages_container = page_soup.find_all(
    "li", {"class": "a-spacing-small item"})
i = 0
for productImage in productImages_container:
    image_raw = productImage.span.span.img["src"]
    # fetch orignal image
    image_filter_1 = image_raw.replace("._SX38_SY50_CR,0,0,38,50_", "")
    image_filter_2 = image_filter_1.replace("._SS40_", "")
    image_filter_3 = image_filter_2.replace("._SR38,50_", "")
    imagesList.insert(i, image_filter_3)
    i = i+1

html = """
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link
      href="https://fonts.googleapis.com/css?family=Sarabun:100,200,300,400,500,600,700,800&display=swap"
      rel="stylesheet"
    />
    <style>
      body {
        background-color: rgb(26, 30, 34);
        font-family: "Sarabun", sans-serif;
        margin: 0px;
      }
      .main {
        align-items: center;
        display: flex;
        flex-direction: column;
        height: 100vh;
        justify-content: center;
      }
      .welcome-text {
        color: rgb(0, 112, 243);
        margin: 0px;
      }
      p {
        color: rgb(200, 225, 255);
        margin: 30px
      }
      ul {
        margin: 50px;
        padding: 0px;
      }
      li {
        color: rgb(200, 225, 255);
      }
      @media (max-width: 600px) {
        .welcome-text {
          color: rgb(0, 112, 243);
          font-size: 2rem;
          text-align: center;
        }
      }
    </style>
    <title>Amascrap</title>
  </head>
  <body>
    <center>
      <h1 class="welcome-text">""" + productName + """</h1>
    </center>
      """

bottom = """
    </ul>
  </body>
  </html>
"""
print(html)

print("<p>Cost: " + productPrice + "</p>")

print("<ul>")
productFeature_container = page_soup.find_all("div", {"id": "feature-bullets"})
for productFeature in productFeature_container:
    features = productFeature.find_all(
        "span", {"class": "a-list-item"})
    i = 0
    for feature in features:
        print("<li>" + feature.text.strip() + "</li>")
        i = i+1
print("</ul>")

print("<ul>")
i = 0
for productImage in productImages_container:
    image_raw = productImage.span.span.img["src"]
    # fetch orignal image
    image_filter_1 = image_raw.replace("._SX38_SY50_CR,0,0,38,50_", "")
    image_filter_2 = image_filter_1.replace("._SS40_", "")
    image_filter_3 = image_filter_2.replace("._SR38,50_", "")
    print("<li>" + image_filter_3 + "</li>")
    i = i+1
print("</ul>")

print(bottom)
