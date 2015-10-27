#### login to heroku
```
cd projects/alinafoto/
sudo heroku login
```

#### create heroku app
```
sudo heroku create
```

#### push changes to heroku remote from git master branch
```
sudo git push heroku master
```

#### ensure we have one dyno running
```
sudo heroku ps:scale web=1
```

#### list running dynos
```
sudo heroku ps
```

#### visit app in web browser 
```
sudo heroku open
```

#### view information about running app
```
sudo heroku logs --tail
```

#### open bash terminal
```
sudo heroku run bash
```

#### manage config variables
__[heroku settings](https://dashboard.heroku.com/apps/alinafoto/settings)__
```
sudo heroku config
sudo heroku config:set PYTHONPATH=/app
sudo heroku config:set SERVER_ENVIRON=production
sudo heroku config:set PORT=5000
sudo heroku config:remove PYTHONPATH
FRONTEND_SERVER_PORTS = [int(os.environ.get('PORT', 5000)), ]
```

#### restart dynos
```
sudo heroku ps:restart
```

#### manage domains
```
sudo heroku domains
sudo heroku domains:add www.alinafoto.lv
sudo heroku domains:add alinafoto.lv
```

#### view the amount of free quota remaining
```
sudo heroku ps -a alinafoto
```

#### default dns
__[nowww naked domain redirect](http://www.arecord.net/)__
```
NS: ns1.dns.lv, ns2.dns.lv
A - Hostname: alinafoto.lv, IP - 122.248.244.139
CNAME - Hostname: alinafoto.herokuapp.com, Alias: www.alinafoto.lv
```

#### cloudflare dns
__[free dns + cdn](https://www.cloudflare.com/a/dns/alinafoto.lv)__
```
NS: ada.ns.cloudflare.com, kurt.ns.cloudflare.com
CNAME - Name: www, Domain name: alinafoto.herokuapp.com
CNAME - Name: alinafoto.lv, Domain name: alinafoto.herokuapp.com
```

#### mx record
__[mailgun](https://mailgun.com/app/domains)__
```
- register a free account at mailgun
- add a mailgun MX record to your cloudflare dns
- set up a forwarding rule at mailgun
```

#### dyno needs to sleep 6h of 24h, sleep mode enables after 30m of inactivity
__[ping your web once a hour](https://uptimerobot.com/dashboard#777048782)__
