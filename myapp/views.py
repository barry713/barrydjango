import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Account, History

# Create your views here.

#----首頁----------------------------------------------------------------------------------------------------------------

def search(request):
    return render(request, 'search.html', )


#----註冊或登入-----------------------------------------------------------------------------------------------------------

def signnRegister(request):
    return render(request, 'signnRegister.html', )


#----將註冊資料儲存至資料庫(crud的create)-----------------------------------------------------------------------------------
def create(request):
    global account
    account = Account(
        name=request.POST.get("name"),
        user=request.POST.get("user"),
        passwd=request.POST.get("passwd"),
        email=request.POST.get("email"),
    )

    user = request.POST.get("user")
    member = Account.objects.all()
    listUser = []
    for elt in member:
        listUser.append(elt.user)
    if user in listUser:
        # return HttpResponse("您已註冊或帳號已存在!")
        return render(request, 'repeatreg2.html', )
    else:
        account.save()
        return redirect(registerSuccess2)  # return HttpResponse("註冊成功!")

#----註冊成功------------------------------------------------------------------------------------------------------------

def registerSuccess2(request):
    return render(request, 'registerSuccess2.html', )


#----登入,比對資料庫資料(crud的retrieve,讀取資料庫資料)-----------------------------------------------------------------------
def retrieve(request):
    user = request.POST.get("user")
    passwd = request.POST.get("passwd")

    obj = Account.objects.all()
    listUser = []
    for elt in obj:
        listUser.append(elt.user)
    if user in listUser:
        p = Account.objects.get(user=user).passwd
        if passwd == p:
            return redirect(loginSuccess2)  # return HttpResponse("登入成功!")
        else:
            return redirect(loginAgain2)
    else:
        return redirect(loginAgain2)




#----登入成功------------------------------------------------------------------------------------------------------------

def loginSuccess2(request):
    return render(request, 'loginSuccess2.html', )

def searchlogin(request):
    return render(request, 'searchlogin.html', )



#----登入失敗------------------------------------------------------------------------------------------------------------

def loginAgain2(request):
    return render(request, 'loginAgain2.html', )


# ----登入成功,進入搜尋頁面------------------------------------------------------------------------------------------------


# ----搜尋輸入錯誤--------------------------------------------------------------------------------------------------------
def searchError(request):
    return render(request, 'searchError.html', )



# ----關於--------------------------------------------------------------------------------------------------------------


#----爬蟲程式------------------------------------------------------------------------------------------------------------
class searchProduct():
    def yahoo_search(sss):
        
        import requests
        from bs4 import BeautifulSoup


        # product = 'iphone 13 pro 256g'  # product = input("請輸入查詢商品:")
        product = str(sss)
        url = "https://tw.buy.yahoo.com/search/product?p=" + product
        # 本機測試-------------------------------------------------------------------------------------------------------
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }
        
        driver = requests.get(url, headers=header)
        soup = BeautifulSoup(driver.text, 'lxml')
        items = soup.find_all('a', 'sc-hTBuwn guxDGq')
        # print(items.html)
        list_y = []
        logo_y = "https://smartscheduler.com.tw/TMP/Wsch/IMG/yahoo.jpg"
        for item in items:
            t = item.find('span', 'sc-ftTHYK sc-pyfCe sc-iOeugr gRqvdT dRIYXN nqfeD').text
            p = item.find('span', 'sc-ftTHYK sc-pyfCe fLdRlM ensNm').text
            p = p.replace("$", "")
            p = p.replace(",", "")
            l = item.get('href')
            urll = l
            driverr = requests.get(urll, headers=header)
            soupp = BeautifulSoup(driverr.text, 'lxml')
            i = soupp.find('img', 'LensImage__img___3khRA').get('src')
        
            list_y.append([t, int(p), l, i, logo_y])
        
        
        return list_y

    def momo_search(sss):
        from bs4 import BeautifulSoup
        from selenium import webdriver

        # product = 'iphone 13 pro 256g'  # product = input("請輸入查詢商品:")
        product = str(sss)
        url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + product + '&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType'
        # 本機測試-------------------------------------------------------------------------------------------------------
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        path = '/Users/barry/chromedriver'
        driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        # 佈署heroku----------------------------------------------------------------------------------------------------
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # --------------------------------------------------------------------------------------------------------------
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.find_all('h3', class_="prdName")
        price = soup.find_all("span", class_="price")
        link = soup.find_all('a', class_='goodsUrl')
        count = 0

        list_m = []
        logo_m = "https://fashionstw.com/wp-content/uploads/2020/05/momo購物-LOGO.jpg"
        for item, p, l in zip(title, price, link):
            count += 1
            if count == 6:
                break
            title = item.text + '\n'  # 商品名稱

            price = p.text  # 商品價格
            price = price.replace("$", "")
            price = price.replace(",", "")

            ll = l.get("href")
            link = 'https://www.momoshop.com.tw' + ll  # 商品連結

            img = l.find("img", class_="prdImg lazy lazy-loaded").get("src")  # 商品圖片

            list_m.append([title, int(price), link, img, logo_m])
        driver.quit()

        return list_m

    def pchome_search(sss):
        import requests
        import json
    
        # product = 'iphone 13 pro 256g'  # product = input("請輸入查詢商品:")
        product = str(sss)
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + product
        # 本機測試-------------------------------------------------------------------------------------------------------
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            
            }
        
        pchome = requests.get(url, headers=header).text
        
        goods = json.loads(pchome)
        goods = goods['prods']
        
        list_pc = []
        logo_pc = "http://2pir-sport.com/wp-content/uploads/2018/08/pchomelogo-730x350.jpg"
        for pch in goods:
            title = pch['name']
            price = pch['price']
            link = 'https://24h.pchome.com.tw/prod/' + pch['Id']
            img = 'https://cs-a.ecimg.tw/' + pch['picS']
            print(title)
            print(price)
            print(link)
            print(img)
            print()
    
            list_pc.append([title, int(price), link, img, logo_pc])
    
        return list_pc

    def etmall_search(sss):
        from bs4 import BeautifulSoup
        from selenium import webdriver

        # product = 'iphone'  # product = input("請輸入查詢商品:")
        product = str(sss)
        url = "https://www.etmall.com.tw/Search?keyword=" + product
        # 本機測試-------------------------------------------------------------------------------------------------------
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # path = '/Users/barry/chromedriver'
        # driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        # 佈署heroku----------------------------------------------------------------------------------------------------
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # --------------------------------------------------------------------------------------------------------------
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.find_all('p', class_="n-name")
        # price = soup.find_all("span", class_="n-price--16")
        price = soup.find_all("div", class_="n-price__wrap")
        link = soup.find_all('a', class_='n-pic')
        image = soup.find_all('img', class_='n_flag_wrap_Mid')
        # print(price)
        count = 0

        list_et = []
        logo_et = "https://img.scupio.com/gym/image/logo/etmall.png"
        for t, p, l, i in zip(title, price, link, image):
            title = t.text  # 商品名稱

            count += 1
            if count == 6:
                break
            price = p.find("span", class_="n-price--16").next_sibling
            pp = price.text  # 商品價格
            price = pp.replace(",", "")

            link = l.get('href')
            ll = 'https://www.etmall.com.tw' + link  # 商品連結

            image = i.get('src')  # 商品圖片
            img = 'https:' + image
            list_et.append([title, int(price), ll, img, logo_et])
        driver.quit()

        return list_et


#----搜尋結果------------------------------------------------------------------------------------------------------------

def shoplist(request):
    sss = request.GET.get("sss")  # 即老師的 year=request.POST.get('year')

    global list_all
    list_all = []

    list_all.extend(searchProduct.yahoo_search(sss))
    # list_all.extend(searchProduct.momo_search(sss))
    list_all.extend(searchProduct.pchome_search(sss))
    # list_all.extend(searchProduct.etmall_search(sss))


    sort_list_all = sorted(list_all, key=lambda x: x[1])

    list_title, list_price, list_link, list_img, list_logo = [], [], [], [], []

    for n in range(len(sort_list_all)):
        list_title.append(sort_list_all[n][0])
        list_price.append(sort_list_all[n][1])
        list_link.append(sort_list_all[n][2])
        list_img.append(sort_list_all[n][3])
        list_logo.append(sort_list_all[n][4])

    mylist = zip(list_title, list_price, list_link, list_img, list_logo, )
    content = {'mylist': mylist, 'sss': sss, }

    if len(sort_list_all) == 0:
        return redirect(searchError)  # return HttpResponse("找不到符合的商品")
    else:
        return render(request, 'shoplist.html', content)



#----搜尋結果排序_價格由小到大-----------------------------------------------------------------------------------------------------------
def indexSearchResult_lowToHigh(request):


    sort_list_all = sorted(list_all, key=lambda x: x[1])  # 價格由小到大

    list_title, list_price, list_link, list_img, list_logo = [], [], [], [], []

    for n in range(len(sort_list_all)):
        list_title.append(sort_list_all[n][0])
        list_price.append(sort_list_all[n][1])
        list_link.append(sort_list_all[n][2])
        list_img.append(sort_list_all[n][3])
        list_logo.append(sort_list_all[n][4])

    mylist = zip(list_title, list_price, list_link, list_img, list_logo, )
    content = {'mylist': mylist, }

    if len(sort_list_all) == 0:
        return redirect(searchError)  # return HttpResponse("找不到符合的商品")
    else:
        return render(request, 'shoplist.html', content)




#----搜尋結果排序_價格由大到小-----------------------------------------------------------------------------------------------------------
def indexSearchResult_highToLow(request):


    sort_list_all = sorted(list_all, key=lambda x: x[1])  # 價格由小到大
    reversed_list_all = list(reversed(sort_list_all))  # 價格由大到小

    list_title, list_price, list_link, list_img, list_logo = [], [], [], [], []

    for n in range(len(reversed_list_all)):
        list_title.append(reversed_list_all[n][0])
        list_price.append(reversed_list_all[n][1])
        list_link.append(reversed_list_all[n][2])
        list_img.append(reversed_list_all[n][3])
        list_logo.append(reversed_list_all[n][4])

    mylist = zip(list_title, list_price, list_link, list_img, list_logo, )
    content = {'mylist': mylist, }

    if len(sort_list_all) == 0:
        return redirect(searchError)  # return HttpResponse("找不到符合的商品")
    else:
        return render(request, 'shoplist.html', content)




#----搜尋結果排序_title_sort-----------------------------------------------------------------------------------------------------------
def indexSearchResult_title(request):


    sort_list_all = sorted(list_all, key=lambda x: x[1])  # 價格由小到大
    title_sort = sorted(sort_list_all, key=lambda y: y[0])  # 價格由大到小

    list_title, list_price, list_link, list_img, list_logo = [], [], [], [], []

    for n in range(len(title_sort)):
        list_title.append(title_sort[n][0])
        list_price.append(title_sort[n][1])
        list_link.append(title_sort[n][2])
        list_img.append(title_sort[n][3])
        list_logo.append(title_sort[n][4])

    mylist = zip(list_title, list_price, list_link, list_img, list_logo, )
    content = {'mylist': mylist, }

    if len(sort_list_all) == 0:
        return redirect(searchError)  # return HttpResponse("找不到符合的商品")
    else:
        return render(request, 'shoplist.html', content)

#----將點擊過的超連結存入資料庫---------------------------------------------------------------------------------------------
def link(request):

    # history = History(
    #     title=request.GET.get("t"),
    #     price=request.GET.get("p"),
    #     link=request.GET.get("l"),
    #     image=request.GET.get("i"),
    # )
    # history.save()
    l = request.GET.get("l")

    return redirect( l )  # return HttpResponse( l )

#----點擊紀錄的頁面-------------------------------------------------------------------------------------------------------
def history(request):
    obj = History.objects.all().order_by('-id')
    list_title, list_price, list_link, list_img = [], [], [], []
    for elt in obj:
        list_title.append(elt.title)
        list_price.append(elt.price)
        list_link.append(elt.link)
        list_img.append(elt.image)

    mylist = zip(list_title, list_price, list_link, list_img)
    content = {'mylist': mylist}

    return render(request, 'history.html', content)



#-----------------------------------------------------------------------------------------------------------------------