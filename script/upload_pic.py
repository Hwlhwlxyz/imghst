import requests


loginurl = 'http://localhost:5000/'
email = 'test@email.com'
password = 'test'
uploadurl = 'http://localhost:5000/api/upload'
localfile_path = 'C:/test.jpg'


h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",

    "Connection": "keep-alive",
    #"Content-Type": "multipart/form-data",
    }


session = requests.Session()

r = session.post(loginurl, data={'email':email, 'password':password})
print(r.status_code)

file ={
'picture': open(localfile_path,'rb')
}
r = session.post(uploadurl, files=file)
print(r.text)
print(r.content)