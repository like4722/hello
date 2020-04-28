#!/usr/bin/python
# -*- coding: utf-8 -*-

def txt_sr(file_name):
    print("处理sr文件")
    with open(file_name) as file_object:
        lines = file_object.readlines()  # 读取每一行存在一个列表中
    data = []
    for line in lines:
        if (line[0:2] in 'CZ') or (line[0:2] in 'Fl'):
            data.append(line)
    with open(file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        f.writelines(data)
        f.close()
    print("sr文件已完成")
def txt_flp(file_name):
    print("处理flp文件")
    with open(file_name) as file_object:
        lines = file_object.readlines()  # 读取每一行存在一个列表中
    data = []
    for line in lines:
        if(len(line)>25):
            if ((line[16] == ',') and (line[19] == ',')) or (line[0:2] in 'FL'):
                data.append(line)
    with open(file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        f.writelines(data)
        f.close()
    print("flp文件已完成")
def txt_avj(file_name):
    print("处理avj文件")
    with open(file_name) as file_object:
        lines = file_object.readlines()  # 读取每一行存在一个列表中
    data = []
    for line in lines:
        if (line[0:2] in 'CZ') or (line[0:2] in 'Fl'):
            data.append(line)
    with open(file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        f.writelines(data)
        f.close()
    print("avj文件已完成")
def main():
    #file_name1 = r'C:\Users\atom\Desktop\FLVoutput\sr.txt'
    #file_name2 = r'C:\Users\atom\Desktop\FLVoutput\FLP.txt'
    #file_name3 = r'C:\Users\atom\Desktop\FLVoutput\AVJ.txt'
    #file_name1 = r'C:\Users\like\Desktop\FLVoutput\sr.txt'
    #file_name2 = r'C:\Users\like\Desktop\FLVoutput\FLP.txt'
    #file_name3 = r'C:\Users\like\Desktop\FLVoutput\AVJ.txt'
    file_name1 = r'C:\Users\north\Desktop\FLVoutput\SR.txt'
    file_name2 = r'C:\Users\north\Desktop\FLVoutput\FLP.txt'
    file_name3 = r'C:\Users\north\Desktop\FLVoutput\AVJ.txt'

    txt_sr(file_name1)
    txt_flp(file_name2)
    txt_avj(file_name3)

if __name__ == '__main__':
    main()
