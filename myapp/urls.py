"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
#-----------------------------------------------------------------------------------------------------------------------

    path('search/',views.search),  # 首頁

#-----------------------------------------------------------------------------------------------------------------------

    path('create/',views.create),  # 將註冊資料儲存至資料庫(crud的create)
    path('retrieve/',views.retrieve),  # 登入,比對資料庫資料(crud的retrieve,讀取資料庫資料)


    path('signnRegister/', views.signnRegister),  # 註冊或登入
    path('loginSuccess2/',views.loginSuccess2),  # 登入成功
    path('loginAgain2/',views.loginAgain2),  # 登入失敗
    path('registerSuccess2/', views.registerSuccess2),  # 註冊成功
    path('retrieve2/', views.retrieve),  # 登入,比對資料庫資料(crud的retrieve,讀取資料庫資料)
    path('searchError/', views.searchError),  # 搜尋輸入錯誤
#-----------------------------------------------------------------------------------------------------------------------

    path('indexSearchResult_lowToHigh/', views.indexSearchResult_lowToHigh),  # 搜尋結果排序_價格由小到大
    path('indexSearchResult_highToLow/', views.indexSearchResult_highToLow),  # 搜尋結果排序_價格由大到小
    path('indexSearchResult_title/', views.indexSearchResult_title),  # 搜尋結果排序_title_sort

    path('shoplist/',views.shoplist),  # 搜尋結果
    path('searchlogin/', views.searchlogin),  # 登入成功,進入搜尋頁面

#-----------------------------------------------------------------------------------------------------------------------

    path('link/',views.link),  # 將點擊過的超連結存入資料庫
    path('history/',views.history),  # 點擊紀錄的頁面
]
