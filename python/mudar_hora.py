import os

ano=2017
mes=05
dia=14

hora=20
minutos=23

str="echo %d-%d-%d %d:%d > fake-hwclock2.data" %(ano,mes,dia,hora-1,minutos)
os.system(str)
os.system("sudo mv fake-hwclock2.data /etc/fake-hwclock.data")
os.system("cat /etc/fake-hwclock.data")
os.system("sudo /sbin/fake-hwclock load force")

