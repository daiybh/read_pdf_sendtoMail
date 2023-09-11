import  pdfplumber

def filter_NoWindowChar(text):
    return text.replace("：","").replace(
        " ","").replace("）","").replace(
            "¥","").replace("￥","").replace(":","").replace(
                ")","").replace("*","")
    
def gotValue(text,key):
    num = text.find(key)
    if num==-1:
        print(f"can not fond {key}")
        raise
    num +=len(key)
    num_end = text.find("\n",num)    
    value = text[num:num_end]
    return filter_NoWindowChar(value)

def findKey(textLines,keys):
    for i,line in enumerate( textLines):
        for key in keys:
            if line.find(key)!=-1:
                return i
    return -1
    
def gotTitle(textLines):
    r= findKey(textLines,["税率","税 率"])
    
    if r==-1:
        return "None"
    
    nextLine = textLines[r+1]
    if nextLine.find("合计")!=-1:
        return "None"
    
    if nextLine.find("合 计")!=-1:
        return "None"

    title = nextLine[0:nextLine.find(" ",1)]   
    
    return filter_NoWindowChar(title)

import os

source_path= "C:/Users/yg/Desktop/fapiao/all"
def changePdfName(pdfPath):
    newfileName=None
    with pdfplumber.open(pdfPath) as pdf:
        page01= pdf.pages[0]
        text = page01.extract_text()

        #print(text)
        textLines= text.split("\n")
        num1 = gotValue(text,"发票代码")

        num2 = gotValue(text,"发票号码")

        title=gotTitle(textLines)

        
        num3 = gotValue(text,"小写")
        

        
        
        
        newfileName=f"BBB-{num3}-{title}-{num1}-{num2}.pdf"        
        
    if newfileName !=None:

        oldpath = os.path.split(pdfPath)

        b = os.path.join(oldpath[0],newfileName)
        print(pdfPath,b)        
        try:
            os.rename(pdfPath,b)
        except Exception as e:            
            print(e)
            oldpath= os.path.split(pdfPath)
            newfileName=f"{num3}-{num1}-{num2}.pdf"
        return b

#a= changePdfName('a.pdf')    


def findALLFile(base,filterName):
    for root,ds,fs in os.walk(base):
        for f in fs:            
            if f.endswith('.pdf') :
                fullname = os.path.join(root,f)
                yield fullname,f[0:4]!=filterName


def ReadAll_and_rename_SendMail():
    import sendMailBase

    allCount={}
    bc=0
    for p,isBBB in findALLFile(source_path,"BBB-"):
        p1= p
        if isBBB:
            p1 = changePdfName(p)
        title= p1.replace(source_path,"").replace("BBB-","")
        
        title= title.split("-")[0].split("\\")
        
        print(title)
        if title[0] not in allCount:
            allCount[title[0]]=0

        allCount[title[0]]+= float(title[1])
        bc+= float(title[1])
        fileShortName = p1.split("\\")[-1]
        sendMailBase.sendMail(title,p1,p1,fileShortName)    

    print("++++++++++++++")
    print(allCount)
    print(bc)

def ReadAll():
    for p,isBBB in findALLFile(source_path,""):
        p1= p
        print(p)
        changePdfName(p)

ReadAll_and_rename_SendMail()
    
    





