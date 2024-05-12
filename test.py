 
import re

text = 'List(http://secure.kakaocdn.net/dna/bURwc6/K6bg9BX2NY/XXX/img_org.jpg?credential=Kq0eSbCrZgKIq51jh41Uf1jLsUh7VWcz&expires=1715533090&allow_ip=&allow_referer=&signature=XniR5UUYCarZ%2BUsdItbSlkSuFaQ%3D,http://secure.kakaocdn.net/dna/bURwc6/K6bg9BX2NY/XXX/img_org.jpg?credential=Kq0eSbCrZgKIq51jh41Uf1jLsUh7VWcz&expires=1715533090&allow_ip=&allow_referer=&signature=XniR5UUYCarZ%2BUsdItbSlkSuFaQ%33)'

# 정규표현식을 사용하여 URL 추출
urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

# 결과를 리스트로 변환하여 출력
# print(urls)
url_list = list(urls)
res = eval("['"+url_list[0].replace(',', "','")[:-1]+"']")
print(res)
print(eval(res))