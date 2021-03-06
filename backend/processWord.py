from requests import get as reqGet
from bs4 import BeautifulSoup
from os import getcwd, path 
from json import loads as jloads
import threading
import sys


cwd = getcwd()
savedir = path.join(path.dirname(cwd) + "\\tsauruselectron\\temp")

a = '-'
b = '-'
c = '-'

def setImage(word):        #---------------#
    try:
        img_url = "" 
        img_url = "https://www.pixabay.com/en/photos/" +word + "/"
        htmlContents = reqGet(img_url).content
        soup  =  BeautifulSoup(htmlContents,'lxml')
        image_tags = soup.find_all('img')
        count = 0
        file = open(savedir+"\\imageurls.txt","w")
        for image_tag in image_tags:
            if count>=4:
                break
            img_src = image_tag.get('src')
            if ('svg' not in img_src) and ('gif' not in img_src):
                file.write(img_src+" #&#  ")
                count += 1
        if count < 4:
            rem = 4 - count
            for i in range(rem):
                file.write(savedir+"\\errorImage.jpg"+" #&#  ")
        file.close()
        global a 
        a = '+'
    except:
        file = open(savedir+"\\imageurls.txt","w")
        for i in range(5):
            file.write(savedir+"\\errorImage.jpg"+" #&#  ")

def setDescription(word):      #--------------#
    try:
        url = ""
        url = 'https://www.britannica.com/search?query='+ word
        content = reqGet(url).content
        soup = BeautifulSoup(content,'lxml')
        div_tag = soup.find("li",class_="mb-45")
        a = div_tag.find('a')
        a['href'] = "https://www.britannica.com" + a['href']
        file = open(savedir+"\\description.txt","w")
        file.write(str(div_tag))
        file.close()
        global b
        b = '+'
    except:
        file = open(savedir+"\\description.txt","w")
        file.write("Oops! Mr. Taurus could not find the word in encyclopedia ! #&#  ")
        file.close()



def setDictionary(word):
    try:
        api_key = '750c98f0-f83f-4604-a78d-9065f53e5804'
        url = "https://www.dictionaryapi.com/api/v3/references/sd2/json/"+ word.lower() + "?key=" + api_key
        resp = reqGet(url)
        data = jloads(resp.text)
        defis = data[0]['def'][0]['sseq']
        count = 0
        file = open(savedir+"\\dictionary.txt","w")
        
        for defi in defis:
            count += 1 
            if(count>=4):
                break
            text = defi[0][1]['dt'][0]
            text = text[1][4:]+"."
            text = text.replace("{it}", "\"")
            text = text.replace("{/it}","\"")
            text = text.replace("{bc}","")
            text = text.replace("{sx","")
            text = text.replace("|}","")
            text = text.replace("}","|")
            file.write("=> " + text + " #&#  ")
        file.write( "< " + data[0]['fl'] + " > #&#  ")
        file.close()
        global c 
        c = '+'
    except:
        file = open(savedir+"\\dictionary.txt","w")
        file.write("Oops! Mr.Tsaurus could not find the word! #&#  ")
        file.close()





def main():

    word = sys.argv[1]
    t1=threading.Thread(target=setImage(word),args=())
    t2=threading.Thread(target=setDictionary(word),args=())
    t3=threading.Thread(target=setDescription(word),args=())
    t1.start()
    t2.start()
    t3.start()


main()
status = a+b+c
print(status)



