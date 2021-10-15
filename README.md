# caculator
## 使⽤heroku佈署flask app的流程
透過heroku可以免費且快速的佈署⼩玩具上線，主要步驟簡述如下:
### PART 1 : Heroku設定
1. 註冊Heroku
2. 在本地安裝 Heroku CLI 及 GIT
### PART2 : python專案設定
需要在python專案內添加幾個設定⽂件<br>
1. Procfile: 如何啟動app，Heroku官⽅使⽤gunicorn，記得加到requirements.txt內<br>
  基本使⽤⽅法<br>
  `web gunicorn <your app name>:app`
2. requirements.txt
  所安裝的套件，注意命名⼀定要對<br>
  可以透過下⾯命令直接輸出<br>
  `pip freeze > requirements.txt`
3. runtime.txt 
  python所使⽤的環境<br>
  e.g. `python-3.7.12`
### PART3 : 佈署
其實可以同步GitHub，但這邊⽤Heroku Git來舉例<br>
先移動到本地專案⽬錄下執⾏以下命令將專案push到heroku<br>
```shell
$ heroku login
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
### PART4 : 其他
* 取log<br>
```power shell
heroku logs -n 1500 | findstr POST > logs_20211015.csv
```
* 解決⼀些佈署上的⼩問題<br>
1. 免費時數只有450⼩時，綁信⽤卡則可以增加到950⼩時
2. 免費版每半⼩時會休眠，為了不影響使⽤體驗，可以透過cron-job定時呼叫
參考:
* https://github.com/twtrubiks/Deploying-Flask-To-Heroku
* https://ctaohe.github.io/2019/11/06/2019-11-6_keep_heroku_alive/

