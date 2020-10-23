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


# SOLVED: no such table
message: `django.db.utils.OperationalError: no such table: django_apscheduler_djangojob`

or longtime: `Performing system checks...`
1. please comment out `wcmomo\app\views.py`: `@register_job(...)`
1. after exec: 2w_mig.bat and 3w_run.bat
1. comment it in


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
