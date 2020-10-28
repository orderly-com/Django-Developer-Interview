# 說明
- 改用 django q
- 補 Linux 之 selenium
- 解釋一下: 
  - 原設計為爬取網頁後存放於檔案(沒有包入上傳repo)，點擊網頁後若無檔案則重爬，並於背景驅動不斷更新
  - 此次上傳，補上預先抓取之檔案


# linux 懶人包
```
請先使用`LSetupChromeDriver.sh`設定chrome for linux
使用`Linux_pipenv_settings.sh`依序執行選項: 
1 & 2
手動create_su
3 開啟排程
4 runserver
查看網頁及排程
http://127.0.0.1:8000/admin/django_q/schedule/
http://127.0.0.1:8000
```

# TODO 20201028 UPDATE 
- [x] django q
- [x] chrome and setups for linux
- [] add logging



---


### 挑戰一: Django 熟悉度 (folder: x_1)

> 請用 Django 實作以下功能

```
爬取 momo購物網(https://www.momoshop.com.tw/main/Main.jsp) 中與促銷活動、特價活動有關的資訊，並將爬回來的資料呈現出來
```

加分項目：
- [x] 排程功能
- [x] 使用 D3.js 呈現資料
- [ ] 使用 CBV
- [x] 使用 async





# Design
- async 抓取二資料進倉
- 瀏覽時自cache file取並用d3呈現
- 背景job定時更新資料至cache (亦使用async)



# TODO
- [x] d3
- [ ] chrome and setups for linux
- [ ] django q
- [ ] pytest


# Others
- 定時job安排方式有多種，this proj 可用
除django_apscheduler 也用其他套件、軟體/OS設定，`5w_job.bat` call的func也可手動turn on/off
