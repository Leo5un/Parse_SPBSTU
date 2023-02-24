
try:
    open('1234.txt')
except Exception as ex:
    print(ex)


k=int(input())
url=''
link = 'ульянова нина'
link = link.replace('/', '%2F').replace(' ', '%20')
if k==1:
    url = 'https://ruz.spbstu.ru/search/groups?q='+link
    print(url)
else:
    url = 'https://ruz.spbstu.ru/search/teacher?q='+link
    print(url)


