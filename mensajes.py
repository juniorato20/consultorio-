import smtplib
body = 'Subject: Subject Here .\nDear ContactName, \n\n' + 'Email\'s BODY text' + '\nYour :: Signature/Innitials'
try:
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
except Exception as e:
    print(e)
    smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
#type(smtpObj) 
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('jhunniorguerrero97@outlook.com', "citasmedicas2020@") 
smtpObj.sendmail('jhunniorguerrero97@outlook.com', 'jhunniorguerrero@gmail.com', body) # Or recipient@outlook

smtpObj.quit()