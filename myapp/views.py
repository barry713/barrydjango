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




# ----搜尋輸入錯誤--------------------------------------------------------------------------------------------------------
def searchError(request):
    return render(request, 'searchError.html', )




#----爬蟲程式------------------------------------------------------------------------------------------------------------
class searchProduct():
    def yahoo_search(sss):
        
        import requests
        from bs4 import BeautifulSoup


        # product = 'iphone 13'  # product = input("請輸入查詢商品:")
        product = str(sss)
        url = "https://tw.buy.yahoo.com/search/product?p=" + product
        # 本機測試-------------------------------------------------------------------------------------------------------
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }
        
        driver = requests.get(url, headers=header)
        soup = BeautifulSoup(driver.text, 'lxml')
        items = soup.find_all('a', 'sc-1drl28c-1 nQTUb')
        # print(items.html)
        list_y = []
        logo_y = "https://smartscheduler.com.tw/TMP/Wsch/IMG/yahoo.jpg"
        for item in items:
            t = item.find('span', 'sc-dlGagL sc-gKBqHi sc-1drl28c-5 gkgFep iSWDmq hnGvZF').text
            p = item.find('span', 'sc-dlGagL sc-gKBqHi dkipYY cWhwYS').text
            p = p.replace("$", "")
            p = p.replace(",", "")
            l = item.get('href')
            urll = l
            driverr = requests.get(urll, headers=header)
            soupp = BeautifulSoup(driverr.text, 'lxml')
            ii = soupp.find('div', 'ProductItemPage__contentWrap___2Oace')
            i = ii.find('img').get('src')
        
            list_y.append([t, int(p), l, i, logo_y])
        
        
        return list_y

    # def momo_search(sss):
    #     from bs4 import BeautifulSoup
    #     from selenium import webdriver

    #     # product = 'iphone 13 pro 256g'  # product = input("請輸入查詢商品:")
    #     product = str(sss)
    #     url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + product + '&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType'
    #     # 本機測試-------------------------------------------------------------------------------------------------------
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--headless')
    #     path = '/Users/barry/chromedriver'
    #     driver = webdriver.Chrome(executable_path=path, chrome_options=options)
    #     # 佈署heroku----------------------------------------------------------------------------------------------------
    #     # chrome_options = webdriver.ChromeOptions()
    #     # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #     # chrome_options.add_argument("--headless")
    #     # chrome_options.add_argument("--disable-dev-shm-usage")
    #     # chrome_options.add_argument("--no-sandbox")
    #     # driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    #     # --------------------------------------------------------------------------------------------------------------
    #     driver.get(url)
    #     soup = BeautifulSoup(driver.page_source, "html.parser")

    #     title = soup.find_all('h3', class_="prdName")
    #     price = soup.find_all("span", class_="price")
    #     link = soup.find_all('a', class_='goodsUrl')
    #     count = 0

    #     list_m = []
    #     logo_m = "https://fashionstw.com/wp-content/uploads/2020/05/momo購物-LOGO.jpg"
    #     for item, p, l in zip(title, price, link):
    #         count += 1
    #         if count == 6:
    #             break
    #         title = item.text + '\n'  # 商品名稱

    #         price = p.text  # 商品價格
    #         price = price.replace("$", "")
    #         price = price.replace(",", "")

    #         ll = l.get("href")
    #         link = 'https://www.momoshop.com.tw' + ll  # 商品連結

    #         img = l.find("img", class_="prdImg").get("src")  # 商品圖片

    #         list_m.append([title, int(price), link, img, logo_m])
    #     driver.quit()

    #     return list_m

    def pchome_search(sss):
        import requests
        import json
    
        # product = 'iphone'  # product = input("請輸入查詢商品:")
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
        import requests
        import json
        
        # product = 'iphone'  # product = input("請輸入查詢商品:")
        product = str(sss)
        
        header = {
            'authority': 'www.etmall.com.tw',
            'method': 'GET',
            'path': '/Search/Get?Keyword=iphone&Fn=&Fa=&Token=&BucketId=&ShopId=&FilterType=&SortType=&MoneyMinimum=&MoneyMaximum=&PageSize=48&PageIndex=0',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
            'cookie': '_gac_UA-36865869-1=1.1678601541.Cj0KCQiA6rCgBhDVARIsAK1kGPIbzME7dqAxw8zSULNNW6ZUYOtLNc230qRddDFgmFtSvK1l5HylSLMaAtYzEALw_wcB; _fbp=fb.2.1678601540960.1377914619; __BWfp=c1678601541618x555981b72; __BWfp=c1678601541618x555981b72; __BWtransf=c1678601541618x555981b72; __BWtransf=c1678601541618x555981b72; _bwEces=true; _gcl_aw=GCL.1678601543.Cj0KCQiA6rCgBhDVARIsAK1kGPIbzME7dqAxw8zSULNNW6ZUYOtLNc230qRddDFgmFtSvK1l5HylSLMaAtYzEALw_wcB; _gcl_au=1.1.1606179248.1678601543; _atrk_siteuid=De8fcY41Dr-JbHBw; etmall-com-tw__zc=3.640d6d481fc0341a8b44dd85.43.0.0.0.; etmall-com-tw__zc_store={%22cv%22:null}; dcs_local_cid=snecvyzzk4; SERVERID=eWeb142; ETMall.CurrentReferrer=https%3A%2F%2Ftw.search.yahoo.com%2F; _gid=GA1.3.760271351.1681890741; crazyAD=one; _atrk_ssid=0Fh0D2mxSXjriT914ynq3N; appier_utmz=%7B%22csr%22%3A%22yahoo%22%2C%22timestamp%22%3A1681890742%2C%22lcsr%22%3A%22yahoo%22%7D; _gat=1; _bwgaid=351511822.1678601541; _gat_gtag_UA_36865869_1=1; appier_page_isView_c135ec63c719c66=0e6c20bf45d69798c059a027bf6458be22130da57d46c289675fa52735c02ce5; appier_pv_counter47a9d95fb44ac66=1; appier_page_isView_47a9d95fb44ac66=0e6c20bf45d69798c059a027bf6458be22130da57d46c289675fa52735c02ce5; appier_pv_counterc135ec63c719c66=2; _atrk_sessidx=9; etmall-com-tw__zc_us=643f9dba7822db1b57e2662a.0.3.1681890746059; _uetsid=1e887720de8711ed876acbd517eafe4a; _uetvid=d943cee0c09c11ed8cc7fb61f1db369d; _uetmsclkid=_uet000eea41da561b649bfa8e737365a1c7; cto_bundle=wsvaEV9vcHM3bEl2OVpjcTM5S1ZzN1dLRno2cnRPR21OeGJCcHBvdW91dm42ak8zQk9NYUE2JTJGWTdJbVZNNmlxV3VVNUpTRUV3TWJUajIlMkJxV2R3QnhOMkZrcHBKcXd2dDBGY21OODVUSFZ0UDJRbDdDUXlWNFFnRmhDWlNmRWZHS2M2dlFjQiUyQkN1ZXpUdWtCM1Y0dFNlTFVadGclM0QlM0Q; _ga_BDNVG31MZY=GS1.1.1681890742.8.1.1681890767.35.0.0; _ga=GA1.3.351511822.1678601541',
            'referer': 'https://www.etmall.com.tw/Search?keyword=iphone',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }
        
        url = "https://www.etmall.com.tw/Search/Get?Keyword=" + product + "&Fn=&Fa=&Token=&BucketId=&ShopId=&FilterType=&SortType=&MoneyMinimum=&MoneyMaximum=&PageSize=48&PageIndex=0"
        res = requests.get(url, headers=header).text
        
        goods = json.loads(res)
        datas = goods['SearchProductResult']
        datas = datas['products']
        count = 0
        


        list_et = []
        logo_et = "https://img.scupio.com/gym/image/logo/etmall.png"
        for data in datas:
            count += 1
            if count == 21:
                break
            title = data['title']
            price = data['finalPrice']
            link = 'https://www.etmall.com.tw' + data['pageLink']
            img = 'https:' + data['imageUrl']

            list_et.append([title, int(price), link, img, logo_et])
        

        return list_et


#----搜尋結果------------------------------------------------------------------------------------------------------------

def shoplist(request):
    sss = request.GET.get("sss")

    global list_all
    list_all = []

    list_all.extend(searchProduct.yahoo_search(sss))
    # list_all.extend(searchProduct.momo_search(sss))
    list_all.extend(searchProduct.pchome_search(sss))
    list_all.extend(searchProduct.etmall_search(sss))


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