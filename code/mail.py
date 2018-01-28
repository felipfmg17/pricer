import smtplib

gmail_user = 'felipedevcrypto@gmail.com'
gmail_password = 'didu.2015'

sent_from = gmail_user
to = ['felipfmg17@gmail.com']
subject = 'OMG Super Important Message'
body = 'Hey, whats up?\n\n- You'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(gmail_user, gmail_password)
server.sendmail(sent_from, to, email_text)
server.close()

print('Email sent!')