from django.shortcuts import render,HttpResponse

# Create your views here.
import requests
from lxml import etree
from douban.models import Movie,Jd
def pcdouban(request):
    top250 = []
    for j in range(0, 226, 25):
        url = 'https://movie.douban.com/top250?start=' + str(j)
        res = requests.get(url)
        tree = etree.HTML(res.text)


        for i in range(1, 26):
            movie = []
            movie += tree.xpath('//*[@id="content"]/div/div[1]/ol/li[' + str(i) +']/div/div[1]/em/text()')
            movie += tree.xpath('//*[@id="content"]/div/div[1]/ol/li[' + str(i) + ']/div/div[2]/div[1]/a/span[1]/text()')
            movie += tree.xpath('//*[@id="content"]/div/div[1]/ol/li[' + str(i)+']/div/div[2]/div[2]/p[1]/text()[1]')
            movie += tree.xpath('//*[@id="content"]/div/div[1]/ol/li[' + str(i)+']/div/div[2]/div[2]/p[1]/text()[2]')

            top250.append(movie)

    save_list = []
    for i in top250:
        save_list.append(Movie(uid=i[0], name=i[1], info1=i[2],info2=i[3]))
    if Movie.objects.count() == 0:
        Movie.objects.bulk_create(save_list)
        print(save_list)
    return HttpResponse('ok')

def douban(request):
    movie = Movie.objects.all()
    data = {
        'movies': movie
    }
    return render(request, 'douban.html', context=data)

def jd(request):
    jd = Jd.objects.all()
    data = {
        'phone': jd
    }
    return render(request, 'jd.html',context=data)