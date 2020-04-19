
import time
import requests
from bs4 import BeautifulSoup
import glob
import fitz
import os


def timeCount():
    for num in range(60):
        time.sleep(1)
        print(num)

def getTitle(soup):


    title = soup.h1.get_text()
    '''
    if(len(title)<=50):
        return title
    temp = title.find(']')
    title = title[temp + 1:]
    while(True):
        temp = title.rfind('[')
        if(temp==-1):
            break
        title = title[:temp - 1]
    '''
    title=title.replace('[','(')
    title=title.replace(']',')')
    return title

def picToPdf(path,fileName):

    doc = fitz.open()

    temp=glob.glob(path)
    number=temp[0].rfind('\\')
    temp.sort(key= lambda x:int(x[number+1:-4]))

    for img in temp:
        print("load"+img)
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    if os.path.exists(fileName):
        os.remove(fileName)
    doc.save(fileName)
    doc.close()



def savePicture(url,path,headers):
	response = requests.get(url,headers=headers)
	with open(path, 'wb') as f:
		f.write(response.content)
		f.flush()


def getWebUrl(target,headers):
    req = requests.get(url=target, headers=headers)
    content = req.text
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gl3c glname')
    pageNum = 0
    webUrl = []
    for div in divs:
        webUrl.append(div.a.get('href'))
    return webUrl

def getPicture(target,headers):

    title=''
    req=requests.get(url=target,headers=headers)
    print("\nSuccess open website")
    content=req.text
    soup = BeautifulSoup(content, 'lxml')
    title=getTitle(soup)
    if(title=='Content Warning'):
        path=target+'?nw=session'
        req = requests.get(url=path, headers=headers)
        content = req.text
        soup = BeautifulSoup(content, 'lxml')
        title = getTitle(soup)
    webUrls=[]
    webUrls.append(target)
    while(True):
        req = requests.get(url=target, headers=headers)
        content = req.text
        soup = BeautifulSoup(content, 'lxml')
        urls = soup.find_all(onclick="document.location=this.firstChild.href")
        for url in urls:
            nextUrl = url.a.get('href')
        if(len(urls)==0):
            break
        if nextUrl in webUrls:
            break
        else:
            webUrls.append(nextUrl)
            target=nextUrl
    print("load "+str(len(webUrls))+" webpages\n")
    webPictureUrl = []
    for url in webUrls:
        req = requests.get(url=url, headers=headers)
        content = req.text
        soup = BeautifulSoup(content, 'lxml')
        divs=soup.find_all(class_='gdtm')
        for div in divs:
            webPictureUrl.append(div.a.get('href'))
    print("load " + str(len(webPictureUrl)) + " photo web pages\n")
    pictureUrl=[]
    for count in range(len(webPictureUrl)):
        req=requests.get(url=webPictureUrl[count],headers=headers)
        content=req.text
        soup=BeautifulSoup(content,'lxml')
        imgs=soup.find_all(id='img')
        for imgUrl in imgs:
            pictureUrl.append(imgUrl['src'])
    banChar=['/','\\',':','*','?','"','<','>','|']
    for char in banChar:
        if title.find(char)>=0:
            title=title.replace(char," ")

    countFile=1
    while (True):
        try:
            if (countFile > 1):

                os.mkdir('./' + title + "(" + str(countFile) + ")")
                title = title + "(" + str(countFile) + ")"
            else:
                os.mkdir('./' + title)
            break
        except FileExistsError:
            countFile = countFile + 1

    print("\n")
    print(title)
    for count in range(len(pictureUrl)):
        savePicture(pictureUrl[count],'./'+title+'/'+str(count)+'.jpg',headers)
        print("save "+title+" "+str(count)+".jpg")
    path='./'+title+'/*'

    picToPdf(path,title+'.pdf')




if __name__=="__main__":

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'}

    target = 'https://e-hentai.org/tag/hane+ame'
    nextUrl = ""
    while(True):
        webUrl = getWebUrl(target, headers)
        for url in webUrl:

            getPicture(url, headers)

            print("sleep 20 seconds")
            time.sleep(20)

        req = requests.get(url=target, headers=headers)
        content = req.text
        soup = BeautifulSoup(content, 'lxml')
        urls = soup.find_all(onclick="document.location=this.firstChild.href")
        for url in urls:
            nextUrl = url.a.get('href')
        if(nextUrl==target):
            break
        target=nextUrl
        timeCount()






