import os

def imageDecode(f,fn):
    dat_read = open(f, "rb")
    #自己新建一个文件路径，用于存放导出的图片
    out='D:\\picture\\'+fn+".png"
    png_write = open(out, "wb")
    for now in dat_read:
        for nowByte in now:
            newByte = nowByte ^ 0x8D#用wxMEdit打开微信.dat文件，读取前两个十六进制值数，然后和FFD8做异或计算，取前两位用十六进制表示
            png_write.write(bytes([newByte]))
    dat_read.close()
    png_write.close()

#全部输出，需要具体到日期前的文件夹(如果太多，请清理内存，以免卡死)
def AllOutput(path):
    list = os.listdir(path) #当前目录下的文件列表
    print(list)
    for i in list:
        pathi = os.path.join(path, i)#pathi:当前文件夹路径
        print(pathi)
        list1 = os.listdir(pathi) #list1:当前文件夹下文件集合
        for fn in list1:
            temp_path = os.path.join(pathi,fn)
            if not os.path.isdir(temp_path):
                imageDecode(temp_path,fn)
                print("批处理"+temp_path+"完成")
            else:
                print(temp_path+"丢失")

#按文件夹输出，path需要具体到某一文件夹
def FolderAllOut(f):
    fsinfo = os.listdir(f)
    print(fsinfo)
    for fn in fsinfo:
        temp_path = os.path.join(f, fn)
        print(temp_path)
        if not os.path.isdir(temp_path):
            print('文件路径: {}' .format(temp_path))
            print(fn)
            imageDecode(temp_path,fn)
        else:
            ...
#要读取的文件路径
path = r'D:\Program Files (x86)\Tencent\Tencent Files\WeChat\WeChat Files\ys1019172727\FileStorage\Image'
#FolderAllOut(path)
AllOutput(path)
