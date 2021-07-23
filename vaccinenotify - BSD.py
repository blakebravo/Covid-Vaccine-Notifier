import urllib.request
import csv
from datetime import datetime
import os
import smtplib
import time

while True:

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('Beginning file download with urllib on', dt_string)

    try:
        url = 'https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv'
        urllib.request.urlretrieve(url, 'Insert File Path Here') #File path to where pulled vaccine availability info should be stored
     
        file1 = open('vaccineold.csv', 'r')
        file2 = open('vaccineupdated.csv', 'r')
        old = list(csv.reader(file1))
        new = list(csv.reader(file2))
        file1.close()
        file2.close()

        differences = []
        for nentry in new:
            for oentry in old:    
                if (oentry[0] == nentry[0]) and (oentry[8] != nentry[8] or oentry[9] != nentry[9]) and (nentry[12] != '0') and (nentry[5].lower() == 'harris' or nentry[5].lower() == 'fort bend' or nentry[5].lower() == 'waller' or nentry[5].lower() == 'austin' or nentry[5].lower() == 'brazoria'):
                    differences.append(nentry)
                    differences.append(oentry)
    
        justadded = []
        isnew = True
        for nentry in new:
            for oentry in old:
                if nentry[0] == oentry[0]:
                    isnew = False
            if isnew and (nentry[12] != '0') and (nentry[5].lower() == 'harris' or nentry[5].lower() == 'fort bend' or nentry[5].lower() == 'waller' or nentry[5].lower() == 'austin' or nentry[5].lower() == 'brazoria'):
                justadded.append(nentry)
            else:
                isnew = True
    
        if differences != []:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            gmail_user = 'Notification Address' #Notification email address here
            gmail_password = 'Notification Address Password' #Notification email address password here

            sent_from = gmail_user
            to = ['Emails Here'] #Array of emails that should be notified here
            subject = "COVID Vaccine Doses Update " + dt_string

            j = 0
            while j < len(differences): 
                try:
                    body = 'Texas Department of State Health Services has issued an update to the number of vaccine doses available. New doses have arrived. See the old and new information below:'
                    email_text = """
                    From: %s
                    To: %s
                    Subject: %s
            
                    %s
                
                    New Information - 
                    Name: %s
                    Type: %s
                    TSA: %s
                    Street: %s
                    City: %s
                    County: %s
                    Address: %s
                    Zip: %s
                    Last Day Update: %s
                    Last Time Update: %s
                    Pfizer Available: %s
                    Moderna Available: %s
                    Total Available: %s
                    Total Shipments over Time: %s
                    Public Phone: %s
                    Website: %s
            
                    Old Information - 
                    Name: %s
                    Type: %s
                    TSA: %s
                    Street: %s
                    City: %s
                    County: %s
                    Address: %s
                    Zip: %s
                    Last Day Update: %s
                    Last Time Update: %s
                    Pfizer Available: %s
                    Moderna Available: %s
                    Total Available: %s
                    Total Shipments over Time: %s
                    Public Phone: %s
                    Website: %s
                    """ % (sent_from, ', '.join(to), subject, body, differences[j][0], differences[j][1], differences[j][2], differences[j][3], differences[j][4], differences[j][5], differences[j][6], differences[j][7], differences[j][8], differences[j][9], differences[j][10], differences[j][11], differences[j][12], differences[j][13], differences[j][14], differences[j][15], differences[j+1][0], differences[j+1][1], differences[j+1][2], differences[j+1][3], differences[j+1][4], differences[j+1][5], differences[j+1][6], differences[j+1][7], differences[j+1][8], differences[j+1][9], differences[j+1][10], differences[j+1][11], differences[j+1][12], differences[j+1][13], differences[j+1][14], differences[j+1][15])
                
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text)
                    server.close()
            
                    print('Email sent!')
                except:
                    print('Something went wrong...')


                j += 2
                
        for item in justadded:
            try:
                body = 'Texas Department of State Health Services has just added a new vaccine provider with available doses. See the new provider below:'
                email_text = """
                From: %s
                To: %s
                Subject: %s
            
                %s
                    
                New Provider - 
                Name: %s
                Type: %s
                TSA: %s
                Street: %s
                City: %s
                County: %s
                Address: %s
                Zip: %s
                Last Day Update: %s
                Last Time Update: %s
                Pfizer Available: %s
                Moderna Available: %s
                Total Available: %s
                Total Shipments over Time: %s
                Public Phone: %s
                Website: %s
                
                    
                """ % (sent_from, ', '.join(to), subject, body, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15])
                    

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.close()
                
                print('Email sent!')
            except:
                print('Something went wrong...')
        if os.path.exists("vaccineold.csv"):
            os.remove("vaccineold.csv")
        else:
            print("The file does not exist")
            
        if os.path.exists("vaccineupdated.csv"):
            os.rename(r'',r'') #File path for renaming new vaccine info into old vaccine information
        else:
            print("The file does not exist")
        
        
        time.sleep(58)
    except:
        print("Connection Error")
