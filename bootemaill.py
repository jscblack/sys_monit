'''
Author       : Gehrychiang
LastEditTime : 2021-01-22 11:03:31
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
ProbTitle    : automatic monitor
'''

import smtplib
import time
import wmi
import os
import sys
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
#开始使用之前您需要修改以下参数
sender_addr='sender@sender.com'
sender_server='smtp.sender.com'
sender_port=994
sender_pwd='sender_pwd'
receiver_addr='receiver@receiver.com'
receiver_mob='receiver_mob'

# 0. 准备开机信息
local_time = time.localtime()

cur_time=str(local_time[0])+"."+str(local_time[1])+"."+str(local_time[2])+" "
if(local_time[3]/10<1):
    cur_time=cur_time+"0"+str(local_time[3])+":"
else:
    cur_time=cur_time+str(local_time[3])+":"
if(local_time[4]/10<1):
    cur_time=cur_time+"0"+str(local_time[4])+":"
else:
    cur_time=cur_time+str(local_time[4])+":"
if(local_time[5]/10<1):
    cur_time=cur_time+"0"+str(local_time[5])
else:
    cur_time=cur_time+str(local_time[5])
w = wmi.WMI()
for BIOSs in w.Win32_ComputerSystem():
        name=BIOSs.Caption

record=open('record.txt',mode='a')

# 1. 连接邮箱服务器
flg=0
for i in range(1,20):#尝试20次
    try:
        con = smtplib.SMTP_SSL(sender_server, sender_port)
    except:
        time.sleep(20)
    else:
        flg=1
        break
if flg==0:
    #连接失败
    #将当前记录追加到文件当中
    record.write(str(str(name)+" "+str(cur_time)+"\n"))
    record.close()
    sys.exit(0)
# 2. 登录邮箱
con.login(sender_addr, sender_pwd)

# 2. 准备数据
# 创建邮件对象
msg = MIMEMultipart()

# 设置邮件主题
subject = Header('SYSTEM AUTOMATIC MONITOR', 'utf-8').encode()
msg['Subject'] = subject

# 设置邮件发送者
msg['From'] = sender_addr

# 设置邮件接受者
msg['To'] = receiver_addr

# 添加文字内容
r=requests.get('http://ip.360.cn/IPShare/info',headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75','Referer':'http://ip.360.cn/'})
s=r.json()
#发送短信(这里使用的是又拍云)
#h=requests.post('https://sms-api.upyun.com/api/messages',headers={'Content-Type':'application/json','Authorization':''},json={'template_id':'','mobile':'','vars':})
htmlcont='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>	<title>Email Message</title>	<style type="text/css">						#outlook a {padding:0;} 		body{width:100% !important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0;}				.ExternalClass {width:100%;} 		.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {line-height: 100%;} 		#backgroundTable {margin:0; padding:0; width:100% !important; line-height: 100% !important;}						img {outline:none; text-decoration:none; -ms-interpolation-mode: bicubic;}		a img {border:none;}		.image_fix {display:block;}				p {margin: 1em 0;}				h1, h2, h3, h4, h5, h6 {color: black !important;}		h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {color: blue !important;}		h1 a:active, h2 a:active,  h3 a:active, h4 a:active, h5 a:active, h6 a:active {			color: red !important; 		 }		h1 a:visited, h2 a:visited,  h3 a:visited, h4 a:visited, h5 a:visited, h6 a:visited {			color: purple !important; 		}				table td {border-collapse: collapse;}				table { border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; }				a {color: orange;}								@media only screen and (max-device-width: 480px) {						a[href^="tel"], a[href^="sms"] {						text-decoration: none;						color: black; 						pointer-events: none;						cursor: default;					}			.mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {						text-decoration: default;						color: orange !important; 						pointer-events: auto;						cursor: default;					}		}				@media only screen and (min-device-width: 768px) and (max-device-width: 1024px) {									a[href^="tel"], a[href^="sms"] {						text-decoration: none;						color: blue; 						pointer-events: none;						cursor: default;					}			.mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {						text-decoration: default;						color: orange !important;						pointer-events: auto;						cursor: default;					}		}		@media only screen and (-webkit-min-device-pixel-ratio: 2) {					}				@media only screen and (-webkit-device-pixel-ratio:.75){					}		@media only screen and (-webkit-device-pixel-ratio:1){					}		@media only screen and (-webkit-device-pixel-ratio:1.5){					}			</style>				</head><body>		<table cellpadding="0" cellspacing="0" border="0" id="backgroundTable">	<tr>		<td>				<table cellpadding="0" cellspacing="0" border="0" align="center"height="83" width="800" style="background-color: #70bbda;">						<tr>				<td width="100%" valign="top" align="center">				<span style=" font-family: sans-serif; font-weight: 700; font-size: 20px; color: #133841; letter-spacing: 14px; text-transform: uppercase; padding-top: 33px; padding-bottom: 15px; display: block;">System Automatic Monitor</span>				</td>			</tr>								</table>						<table cellpadding="0" cellspacing="0" border="0" align="center" width="600">			<tr>				<td width="100%" valign="top">					<h2 style="font-family: sans-serif; font-size: 30px; color: #133841 !important; padding: 0 30px; margin-top: 45px; margin-bottom: 25px;">设备{device_name}<br></br></h2>				</td>			</tr>			<tr>				<td width="100%" valign="top">					<span style="padding: 0 30px; font-family: sans-serif; font-weight: 400; font-size: 20px; color: #133841; margin-bottom: 30px; line-height: 20px; display: block;">已于{up_time}开机</span>				</td>							</tr>			<tr>			<td width="100%" valign="top">				<span style="padding: 0 30px; font-family: sans-serif; font-weight: 400; font-size: 16px; color: #133841; margin-bottom: 30px; line-height: 20px; display: block;">当前设备的IP为{device_ip}<br></br>{device_location}</span>			</td>			</tr>		</table>																<table cellpadding="0" cellspacing="0" border="0" align="center" width="800" style="background-color: #ef4c51;">			<tr>				<td valign="top">					<table cellpadding="0" cellspacing="0" border="0" align="center" width="100%">						<tr>							<td valign="top"align="center" >								<span style="font-family: sans-serif; font-weight: 400; font-size: 17px; color: #fff; margin: 30px 0;  line-height: 20px;padding: 0 30px; display: block;">倚栏听风云监控 2019-2021</span>							</td>						</tr>					</table>				</td>							</tr>		</table>				</td>	</tr>	</table>	</body></html>'
htmlcont=htmlcont.replace("{device_name}",name)
htmlcont=htmlcont.replace("{up_time}",cur_time)
htmlcont=htmlcont.replace("{device_ip}",s['ip'])
htmlcont=htmlcont.replace("{device_location}",s['location'])
text = MIMEText(htmlcont, 'html', 'utf-8')
msg.attach(text)
# 补充之前的历史记录
if(os.path.getsize('record.txt')>0):#文件有大小
    att1 = MIMEText(open('record.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="record.txt"'
    msg.attach(att1)

# 3.发送邮件
print("yes")
flag=0
for i in range(1,20):#尝试20次
    try:
        con.sendmail(sender_addr, receiver_addr, msg.as_string())
    except:
        time.sleep(20)
    else:
        flag=1
        break
#只要成功发送则删除开机历史记录
if flag==0:
    #发送失败
    record.write(str(str(name)+" "+str(cur_time)+"\n"))
    record.close()
else:
    record.seek(0)
    record.truncate()
    record.close()
con.quit()
