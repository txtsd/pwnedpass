import requests
import csv
import hashlib
from time import sleep

api_link = 'https://api.pwnedpasswords.com/range/'

ses = requests.Session()
with open('pass.csv', newline='') as csvfile:
    file = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in file:
        # print(row['Password'])
        raw_pass = row['Password']
        sha1_pass = hashlib.sha1(raw_pass.encode()).hexdigest()
        sha1_five = sha1_pass[:5]
        # sha1_rest = sha1_pass[5:]
        result = ses.get(api_link + sha1_five)
        if result.status_code == 200:
            # print('   ', result.text)
            result_file = result.text
            lines = result_file.split('\r\n')
            for line in lines:
                # print(line)
                sha1_rest, num_breaches = line.split(':')
                # if (sha1_five + sha1_rest == sha1_pass) and (num_breaches > 0):
                if (sha1_five + sha1_rest.lower() == sha1_pass):
                    print(row['Title'] + '[' + row['Username'] + '] [' + raw_pass + '] has been compromised', num_breaches, 'times.')
        sleep(1.5)
        # break
