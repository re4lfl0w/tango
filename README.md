# How To Tango With Django 1.7

<img src="http://www.tangowithdjango.com/book17/_static/twd200x200.jpg" width=200 />

- [책 소개](http://www.tangowithdjango.com/book17/index.html)
- [tango with django on github](https://github.com/leifos/tango_with_django)
- [Tutorial 따라해서 Django로 만든 Rango Homepage](http://re4lfl0w.pythonanywhere.com/rango/)

<img src="https://github.com/re4lfl0w/tango/blob/master/static/images/capture_index.png?raw=true" width=600 alt="capture index">

## 이 책을 선택한 이유

- django로 뭔가 만들어보고 싶어서
- 다른 책들도 참고를 했는데 너무 기본적인 내용들만 있어서..
  - [django로 배우는 쉽고 빠른 웹 개발 - 파이썬 웹 프로그래밍 on github](https://github.com/re4lfl0w/django_python_web_programming): 기본기 잡기에는 정말 좋았음
  - [django 공식 홈페이지](https://docs.djangoproject.com/en/1.7/): 양이 너무 많아서 힘들고 Polls Tutorial 이후로는 거의 Reference로 봐야되기 때문
  - [날로 먹는 django - 중급자용](http://blog.hannal.com/category/start-with-django-webframework/): 재미있게 읽었다. 특히 정적 파일에 대한 부분을 자세히 다뤄줬음. 아직 완결이 안되서 다른 책 볼 필요가 생겨서

## 이 책을 정리하면서 들었던 생각

- Fuunction Based Views라서 Class Based Views의 장점을 활용하지 못했다. 이건 [django로 배우는 쉽고 빠른 웹 개발 - 파이썬 웹 프로그래밍 on github](https://github.com/re4lfl0w/django_python_web_programming)를 참고하면 좋겠다. CBV로 해볼 수도 있었지만 일단은 책 내용대로 따라해봐야 정신건강에 이롭다..
- bootstrap, AJAX 등 알고는 있었는데 실제 웹 사이트에 적용해보니 신세계.. 지금까지는 단편적으로 연동되는 사이트 단위가 아니라서 그다지 느낌은 없었다.

## 다음으로 배워보고 싶은 것

- Social Login
- TDD
- AWS Deploy

## 실습하면서 느꼈든 문제점들

### 14장 Template Tags

- \_\_init\_\_.py 제대로 작성했는데 문제가 생겼네..
- 무슨 문제인지는 모르겠지만 다른 파일을 덮어씌웠더니 문제가 해결됐음
- 아...그냥 만들어만 놓고 저장을 하지 않아서 그런가..?
- [Django: Unable to load template tags \- Stack Overflow](http://stackoverflow.com/questions/4486288/django-unable-to-load-template-tags): 여기에서 보듯이 파일명을 잘못쓴 줄 알고 확인했는데 아니어서 그냥 덮어씌워버리니까 해결... 이유가 뭘까..?!

### {% get_category_list category %}

- category를 어디서 받아서 넘기냐?
- 어쨋든 결과적으로 보면 결과가 제대로 css에 active class가 적용이 되긴 됐는데
- 저 category를 어디서 받는지를 모르니 답답한 노릇이네
- templatetags를 내가 몰라서 그런가??

### Bing API

- [Bing Search API Quick Start and Code Samples.docx \- Microsoft Word Online](https://onedrive.live.com/view.aspx?resid=9C9479871FBFA822!112&app=Word&authkey=!ANNnJQREB0kDC04): Bing Search API 설명서 잘 나옴
- [15.5. optparse — Parser for command line options — Python 2.7.10 documentation](https://docs.python.org/2/library/optparse.html): 많이 쓰는거라서 외우고 있어야 될 것 같은데..?

### 20. Automated Testing

#### can't compare offset-naive and offset-aware datetimes

- [Django: can’t compare offset\-naive and offset\-aware datetimes error | Wael BEN ZID ELGUEBSI](https://benzidwael.wordpress.com/2013/12/11/django-cant-compare-offset-naive-and-offset-aware-datetimes-error/): 시간 정보 짜증나는군. datetime.now()가 aware라서 pytz로 naive로 바꿔줘야 되는듯

### deploy

- [python \- Django gives Bad Request (400) when DEBUG = False \- Stack Overflow](http://stackoverflow.com/questions/19875789/django-gives-bad-request-400-when-debug-false)
- **settings.py** 에서 **DEBUG = False**만 하면 **Bad Request(400)**이 뜹니다. 어떻게 해결해야 될까요? 검색해서 찾아보니 **ALLOWED_HOST = ['\*']** 을 넣으면 된다고 하는데 저 같은 경우는 그래도 계속 Bad Request(400)이 뜨네요.
- [Settings | Django documentation | Django](https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts)
