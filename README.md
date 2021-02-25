## Introduction
一个简单、方便的Cloudflare DNS管理脚本  
基于 Cloudflare API 实现对DNS记录的增删改查，配合crontab也可以当DDNS用  
对DNS的修改记录至文件，默认日志文件路径：`/var/log/cloudflare_dns.log`

## Requirement
修改脚本中以下4个变量  
`cf_id` = "cloudflare账号(邮箱)"   
`cf_key` = "global api key"  
`zone_id` = "域名的zone_id"  
`zone_name` = '根域名名称'

- Read more  
[cloudflare_dns_manipulate](https://blog.kwin.win/2021/02/25/cloudflare-dns-manipulate/)  