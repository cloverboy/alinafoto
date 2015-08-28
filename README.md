### login to heroku
```
cd projects/alinafoto/
sudo heroku login
```

### create heroku app
```
sudo heroku create
```

### push changes to heroku remote from git master branch
```
sudo git push heroku master
```

### ensure we have one dyno running
```
sudo heroku ps:scale web=1
```

### lists the running dynos of your application
```
sudo heroku ps
```

### visit the app in our browser 
```
sudo heroku open
```

### view information about your running app
```
sudo heroku logs --tail
```

### open bash terminal
```
sudo heroku run bash
```

### change config variables
__[heroku settings](https://dashboard.heroku.com/apps/alinafoto/settings)__
```
sudo heroku config
sudo heroku config:set PYTHONPATH=/app
sudo heroku config:set SERVER_ENVIRON=production
sudo heroku config:set PORT=5000
sudo heroku config:remove PYTHONPATH
FRONTEND_SERVER_PORTS = [int(os.environ.get('PORT', 5000)), ]
```

### restart dynos
```
sudo heroku ps:restart
```

### manage domains
```
sudo heroku domains
sudo heroku domains:add www.alinafoto.lv
sudo heroku domains:add alinafoto.lv
```

### view the amount of free quota remaining
```
sudo heroku ps -a alinafoto
```

### dns
__[nowww naked domain redirect](http://www.arecord.net/)__
```
A - Hostname: alinafoto.lv, IP - 122.248.244.139
CNAME - Hostname: alinafoto.herokuapp.com, ALias: www.alinafoto.lv
```
