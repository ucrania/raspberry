import smtplib

if dep<5 and not mailwassent: 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	mymail="seic2017g2@gmail.com"
	mypass="seic2017321"
	igormail="ucrania95@gmail.com"
	tomail=igormail
	server.login(mymail, mypass)
 
	msg = "Alerta! O deposito encontra-se vazio."

	server.sendmail(mymail,tomail, msg)
	server.quit()
	mailwassent=True

elif mailwassent and dep>10
	mailwassent=False
	
	 
