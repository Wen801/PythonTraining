import nmap
from bs4 import BeautifulSoup
import requests
from cryptography.fernet import Fernet

nm=nmap.PortScanner()
#find the current port number. 
nm.scan('127.0.0.1','3000-3077')
port= nm['127.0.0.1']['tcp'].keys()
for port_number in port:
    print(port_number)

#find the correct URL
url_list = []
url = "http://localhost:"+str(port_number)+"/first"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'lxml')
print(soup.prettify())
for link in soup.find_all("a"):
    if str(port_number) in link.get("href"):      
        print(link.get("href"))
        url_list.append(link.get("href"))    
for item in url_list:
    if item.find("localhost")!=-1:
        correct_url=item
        print ("THIS IS THE PASS PHRASE"+correct_url)
pass_phrase = requests.get(correct_url).text
print (pass_phrase)

#Find the correct passphrase
start_pt = pass_phrase.find("\"")
end_pt = pass_phrase.find("\"", start_pt + 1)  # add one to skip the opening "
quote = pass_phrase[start_pt + 1: end_pt]
print(quote)


p=requests.post(correct_url, data={port_number: quote})
#use reponse from post to find key and encrytped password.
data=p.json()
print(data)
print(data["key"])
print(data["encrypted_password"])

#decrypted the password
key_d= data["key"]
my_key_byte=str.encode(key_d)
print(my_key_byte)
cipher_suite = Fernet(my_key_byte)
cipher_text=data["encrypted_password"]
cipher_text_byte=str.encode(cipher_text)
print(cipher_text_byte)

plain_text = cipher_suite.decrypt(cipher_text_byte)
phrase=plain_text.decode()
print(f"PASSWORD IS {phrase}")








