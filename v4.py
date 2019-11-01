import urllib.request
import re
import os
import time
# from tqdm import tqdm
# from tqdm._tqdm import trange
                                        # # # # # # # # 
                                        # 高清图爬取版 #
                                        # # # # # # # #  
# 从第几页开始爬取
start = 1
# 搜爬取多少页   
page = 3
# 爬取关键字,空 则默认爬取网站页面全部图片 || 可以搜画师名,人物罗马音(izayoi_miku),英文单词(tattoo)
# 禁止“/”等字符输入 , 支持下划线 fate_stay_night
keyword = "tattoo"

print('起始页:'+str(start)+' 爬取页数:'+str(page)+' 爬取关键字:'+str(keyword))
while start <= page:
    if(start==1):
        if(keyword==""):
            baseurl = "https://yande.re/post"
        else:
            baseurl = "https://yande.re/post?tags="+str(keyword)
    else:
        if(keyword==""):
            baseurl = "https://yande.re/post?page="+str(start)
        else:
            baseurl = "https://yande.re/post?page="+str(start)+'&tags='+str(keyword)
    print('爬取页面地址: '+baseurl)
    print('开始第'+str(start)+'页下载中...')
    start+=1
    def pagedownload(baseurl):
        basehtml_bytes = urllib.request.urlopen(baseurl).read()
        basehtml = basehtml_bytes.decode("UTF-8")
        def basereg(html):
            reg = r'(id="p)([0-9]+?)(")'
            all = re.compile(reg)
            alllist = re.findall(all, html)
            return alllist
        baseimgurls = basereg(basehtml)
        # print(baseimgurls)

        def download(baseurl):
            url = "https://yande.re/post/show/"+str(baseurl)
            os.makedirs('./image/', exist_ok=True)
            html_bytes = urllib.request.urlopen(url).read()
            html = html_bytes.decode("UTF-8")
            def reg(html):
                reg = r'(id="image" class="image")(.+?)(src=")(.+?)(")'
                all = re.compile(reg)
                alllist = re.findall(all, html)
                return alllist
            imgurls = reg(html)
            def urllib_download():
                for imgurl in imgurls:
                    from urllib.request import urlretrieve
                    IMAGE_URL = imgurl[3]
                    IMAGE_URL = IMAGE_URL.replace("sample", "image", 1);
                    def cbk(a,b,c):  
                        '''''回调函数 
                        @a:已经下载的数据块 
                        @b:数据块的大小 
                        @c:远程文件的大小 
                        '''  
                        per=100.0*a*b/c  
                        if per>100:  
                            per=100  
                        print('%.2f%%' % per)
                    try:              
                        urlretrieve(IMAGE_URL, './image/img'+str(baseurl)+'.jpg', cbk)
                        state="true"
                        return state
                    except:
                        IMAGE_URL = IMAGE_URL.replace("jpg", "png", 1);
                        urlretrieve(IMAGE_URL, './image/img'+str(baseurl)+'.png', cbk)
                        state="true"
                        return state
                    else:
                        state="false"
                        return state
                        pass
                return state
            return urllib_download()

        num = 1
        for baseimgurl in baseimgurls:
            state=download(baseimgurl[1])
            if(state=="true"):
                print('第'+str(num)+'张图下载成功')
            else:
                print('第'+str(num)+'张图下载失败')
            num+=1
    pagedownload(baseurl)



