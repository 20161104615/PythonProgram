import requests
import json
import urllib.request
import os
import pymysql


class QQmusic:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.sl = []
        self.ad = []
        self.musicList = []

    # 获取页面
    def getPage(self,url,headers):
        res = requests.get(url,headers = headers)
        res.encoding = 'utf-8'
        return res


    # 获取音乐songmid
    def getSongmid(self):
        num = int(input('请输入获取条数：'))
        # num = 20
        name = input('请输入歌名或歌手：')
        # name = '张学友'
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=%d&w=%s'%(num,name)
        # 搜索音乐
        res = self.getPage(url,headers=self.headers)
        html = res.text
        html = html[9:]
        html = html[:-1]
        # 获取songmid
        js = json.loads(html)
        songlist = js['data']['song']['list']
        for song in songlist:
            print(song)
            singername = song['singer']
            albumid = song['albumid']
            songmid = song['songmid']
            songname = song['songname']
            self.sl.append((songname,songmid,albumid,singername))
            print('获取成功songmid')

    #打印albumid
    def printalbumid(self):
        print('输出albumID：')
        print(self.sl)
        
        print('——————————————分解开始————————————————')
        for songing in self.sl:
            print('歌曲内容',songing[0],songing[3])
            print('______________________________________________________________')
            for b in songing[3]:
                print(b['name'])
            print('——————————————分解结束————————————————')
            
           
            

    # 获取音乐资源，guid是登录后才能获取，nin也是
    def getVkey(self):
        #guid = input('请输入ts_uid：')
        guid = '5229440472'
        #uin = input('请输入QQ号：')
        uin = '1019172727'
        for s in self.sl:
            print('开始获取资源')
            # 获取vkey,purl
            name = s[0]
            songmid = s[1]
            keyUrl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}'%(guid,guid,songmid,uin,uin)
            res = self.getPage(keyUrl,headers=self.headers)
            html = res.text
            keyjs = json.loads(html)
            purl = keyjs['req_0']['data']['midurlinfo'][0]['purl']
            # 拼凑资源url
            url = 'http://dl.stream.qqmusic.qq.com/' + purl
            self.musicList.append((name,url))
            print('资源地址获取成功')

    #   下载音乐
    def downloadMusic(self):
        for m in self.musicList:
            url = m[1]
            res = self.getPage(url,headers=self.headers)
            music = res.content
            name = m[0] + '.mp3'
            with open(name, 'wb') as f:
                f.write(music)
                print('下载OK')
                f.closed
        path='D:/PythonProgram/PythonProgram/img'
        for songimg in self.sl:
            singerName=''
            imgurl = 'http://imgcache.qq.com/music/photo/album_300/%i/300_albumpic_%i_0.jpg'%(list(songimg)[2]%100,list(songimg)[2])
            for singerN in songimg[3]:
                if (singerN['name']!= 0):
                    singerName+='-'
                    singerName+=singerN['name']
                else:
                    singerName=singerName
            urllib.request.urlretrieve(imgurl,os.path.join(path,list(songimg)[0]+singerName+'.jpg'))
            print('下载图片：'+list(songimg)[0])
        print('下载完成')


    #存储到数据库,路径均为"http://localhost:8080/media"+文件名称
    def uploadtoMySQL(self):
        connect = pymysql.Connect(host='localhost',port=3306,user='root',password='root',database='omss',charset='utf8')
        cursor = connect.cursor()
        sql = "insert into music (music_name,music_singer,music_storagepath,music_img) values ('%s','%s','%s','%s')"
        for song in self.sl:
            #获取音乐名称
            singerName=''
            musicURL = 'http://localhost:8080/media/'
            musicIMGURL = 'http://localhost:8080/media/img/'
            musicURL+=song[0]
            musicURL+='.m4a'
            musicIMGURL+=song[0]
            #获取歌手名称
            for singerN in song[3]:
                if (singerN['name']!= 0):
                    singerName+='-'
                    singerName+=singerN['name']
                else:
                    singerName=singerName
            musicIMGURL += singerName
            musicIMGURL +='.jpg'
            data = (str(song[0]),str(singerName)[1:],str(musicURL),str(musicIMGURL))
            cursor.execute(sql % data)
            connect.commit()
        print('插入数据成功')
        cursor.close()
        connect.close()
        print('关闭连接')
            
        
        
    
QQ = QQmusic()
QQ.getSongmid()
QQ.getVkey()
#QQ.printalbumid()
QQ.downloadMusic()
QQ.uploadtoMySQL()
