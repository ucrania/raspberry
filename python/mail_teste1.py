import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
mymail="esp8266seicg1@gmail.com"
mypass="passesp8266"
igormail="ucrania95@gmail.com"
alexmail=""
mariomail="2140237@my.ipleiria.pt"
tomail=igormail
server.login(mymail, mypass)
 
msg = "Alex o deposito esta vazio!\nDevias passar aqui para o encher!"
msg = "http://naelshiab.com/tutorial-send-email-python/"
n=0
while n<1:
	server.sendmail(mymail,tomail, msg)
	n=n+1
	print "\tMail %d sent" %n
server.quit()

