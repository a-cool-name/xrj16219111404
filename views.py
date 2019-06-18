from django.shortcuts import render,HttpResponse
import time,os
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from django.views import View
from django.http import HttpResponseRedirect
# Create your views here.


class Code:

    def __init__(self, browser):
        self.browser = browser

    #确定验证码的位置
    def get_position(self):
        time.sleep(1)
        element = self.browser.find_element_by_class_name('touclick-img-par')
        time.sleep(1)
        location = element.location
        size = element.size
        position= (location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height'])
        return position

    # 截取整个网页页面
    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        url = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media/login.png')
        self.browser.get_screenshot_as_file(url)
        return screenshot

    #从截取的网页，裁剪出验证码图片，并保存到本地
    def get_touclick_img(self, name = 'captcha.png'):
        position = self.get_position()
        print('验证码的位置:', position)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop(position)
        url = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media/captcha.png')
        captcha.save(url)
    #
    # # 缩小并转为jpg
    # def change_img(self):
    #     url = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media/captcha.png')
    #     im = Image.open(url)
    #     im = im.convert('RGB')
    #     x = int(im.size[0] / 2)
    #     y = int(im.size[1] / 2)
    #     im = im.resize((x, y), Image.ANTIALIAS)
    #     im.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media/captcha.jpg'))

    def move(self,num):
        try:
            element = self.browser.find_element_by_class_name('touclick-img-par')
            for i in num:
                a = int(i)
                if a <= 4:
                    ActionChains(self.browser).move_to_element_with_offset(element,40+72*(a-1),73).click().perform()
                else :
                    a -= 4
                    ActionChains(self.browser).move_to_element_with_offset(element,40+72*(a-1),145).click().perform()
        except:
            print('元素不可选！')

    def main(self,num):
        self.get_touclick_img()
        # self.change_img()
        self.move(num)




class Index(View):
    sava_info ={}

    def get(self,request):
        browser = webdriver.Chrome()
        browser.set_window_size(800, 600)
        browser.get('https://kyfw.12306.cn/otn/login/init')
        code = Code(browser)
        button = browser.find_element_by_id('loginSub')

        self.sava_info['brower'] = browser
        self.sava_info['button'] = button
        self.sava_info['code'] = code

        input_name = browser.find_element_by_id('username')
        input_pd = browser.find_element_by_id('password')
        time.sleep(1)
        input_name.send_keys('18815012086')
        input_pd.send_keys('2a335357')
        code.get_touclick_img()
        # code.change_img()
        return render(request, '12306.html')

    def post(self,request):
        num = request.POST.get('num')
        brower = self.sava_info['brower']
        code = self.sava_info['code']
        button = self.sava_info['button']

        code.move(num.split())
        button.click()
        time.sleep(2)
        return HttpResponseRedirect('/')