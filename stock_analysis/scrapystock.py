import requests
from bs4 import BeautifulSoup
import traceback
import re
import csv

def getHTMLtext(url,code = "utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        print("test")
        return  r.text
    except:
        return ""

def getStockList(list,stockURL):
    html = getHTMLtext(stockURL,"GB2312")
    print("getstockList start")
    soup = BeautifulSoup(html,"html.parser")
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            list.append(re.findall(r"[s][hz]\d{6}",href)[0])
        except:
            continue

def getStockInfo(list,stockURL,filePath):
    count = 0
    for stock in list:
        url = stockURL + stock + ".html"
        html = getHTMLtext(url)
        try:
            if html=="":
                continue

            infoDict = {}
            soup = BeautifulSoup(html,"html.parser")
            stockInfo = soup.find('div',attrs={'class':'stock-bets'})

            name = stockInfo.find_all(attrs = {'class':'bets-name'})[0]
            infoDict.update({'stocking name':name.next.split()[0]})

            keylist = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keylist)):
                key = keylist[i].text
                value = valueList[i].text
                infoDict[key] = value

            with open(filePath,'a',encoding='UTF-8') as f:
               # f.writer(str(infoDict))
                f.write(str(infoDict) + '\n')
                count = count + 1
                print(count)
                print("\r processing: {:.2f}".format(count*100/len(list)))

        except:
            count = count + 1
            print('error')
            print("\r processing: {:.2f}%".format(count*100/len(list)))
            continue

def main():
    print("start")
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_infor_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'BaiduStockInfor.txt'
    slist = []
    getStockList(slist,stock_list_url)
    getStockInfo(slist,stock_infor_url,output_file)
    print("end")

if __name__ == '__main__':
    main()