#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。——————————————————————————————————————————
#。
#。  language_words.py
#。  语言支持文件（中、英文）
#。
#。 @Time    : 2018/7/26 00:09
#。 @Author  : capton
#。 @Software: PyCharm
#。 @Blog    : http://ccapton.cn
#。 @Github  : https://github.com/ccapton
#。 @Email   : chenweibin1125@foxmail.com
#。__________________________________________

from ip_source import is_chinese_user

en = {
    'po':'Port',
    'si':'Size',
    'wa':'Warning',
    'ce':'Connect Error',
    'ip':'Input Port : ',
    'tf':'The File :',
    'td':'The Dir (And All Files In This Dir):',
    'ya':'You Are Going To Transport ',
    'ct':'Continue To Transport? ',
    'gvm':'Give Up Mission...Continue',
    'ctt':'Continue To Transport? ',
    'pit':'Please Input The Target Host:',
    'pmb':'Port Must Be Positive Number!',
    'cdd':'Connection Disconnected',
    'ci':'Connection Interrupted',
    'rcd':'Remote Conenction Destoried',
    'sin':'Socket Is None',
    'ffi':'Finding Files In ',
    'ff':'Found File: ',
    'fd':'Found Dir: ',
    'm_s':'Mission_Size',
    'mc':'Mission Complished!',
    'pif':'Please Input File Or Dir Path:',
    'pde':'Path Doesn\'t Exist!',
    'nrth':'No Route To Host',
    'pttmoa':'Please Try The Mission Once Again',
    'cd':'Creating Dir',
    'cf':'Transporting File',
    'picfp':'Please Input Correct File path',
    'ms':'Mission Start',
    'tsbd':'The Server Is Working,But Data Socket Is Not Working On Port',
    'pct':'Please Confirm The Server Is Working Well',
    'octs':'Or Check The Server\'s Address Is The Same As The Parameters You Key In',
    'thap':'The Host And Port You Key In Is ',
    'ftcp':'FileTransporter Client Program',
    'ftsp':'FileTransporter Server Program',
    'id':'Is Disabled',
    'fi':'finished',
    'pki':'Please Key In Other Number',
    'tpif':'The Path Is A File',
    'total':'Total ',
    'Author':'Author',
    'Blog':'Blog',
    'Email':'Email',
    'Github':'Github',
    'Project':'Project',
    'tpws':'The Path Which File Will Send',
    'tptp':'The Port That Program Data Will Transport',
    'thtp':'The HostIp That Program Data Will Transport To',
    'ctcs':'Connected To Command Socket ',
    'cara':'Can\'t Assisn Requested Address',
    'fsd':'File Save Dir: ',
    'shs':"Server Started",
    'ra':"Server is Running at",
    'wfft':"Waiting For Transportation",
    'nc':'New Client',
    'ctds':'Connected to data socket :',
    'aoc':'An Old Connection Is Trying To Restored,But Failed',
    'st':'Start Transporting :',
    'dd':' Downloaded',
    'pidp':'Please Input Dir Path:',
    'dpif':'The Path Is A File!',
    'tdpw':'The Dir Which File Will Save There',
    'yhim':'You Have Interrupted Mission',
    'cmct': 'Cost Time：',
    'fe': 'File Already Existed：',
}
cn = {
    'po':'端口',
    'si':'大小',
    'wa':'警告',
    'ce':'连接错误',
    'ip':'输入端口号： ',
    'tf':'文件 ：',
    'td':'文件夹（包括在内的所有文件）:',
    'ya':'您准备发送的是',
    'ct':'继续发送？ ',
    'gvm':'放弃任务...继续',
    'ctt':'继续发送？',
    'pit':'请输入目标主机：',
    'pmb':'端口号必须为正整数',
    'cdd':'连接断开',
    'ci': '连接中断',
    'rcd':'远端连接断开',
    'sin':'Socket套接字为None',
    'ffi':'在此查找文件：',
    'ff': '找到文件: ',
    'fd': '找到文件夹: ',
    'm_s':'任务大小',
    'mc':'任务完成',
    'pif':'请输入文件或者文件夹的路径：',
    'pde':'该路径下不存在任何东西',
    'nrth':'无法路由到主机',
    'pttmoa':'请重新尝试此任务',
    'cd':'创建文件夹',
    'cf':'发送文件中',
    'picfp':'请输入正确的文件路径',
    'ms':'任务开始',
    'tsbd':'服务端正在工作，但是数据套接字没有工作在端口上',
    'pct':'请确认服务端是否正常运行',
    'octs':'或者确认服务端的地址和端口号是否和您输入的一致',
    'thap':'您输入的主机和端口号是',
    'ftcp':'文件传输发送端程序',
    'ftsp':'文件传输接收端程序',
    'id':'不可用',
    'fi':'完成',
    'pki':'请输入其他的数字',
    'tpif': '此路径指向一个文件',
    'total': '总计',
    'Author':'作者',
    'Blog':'博客',
    'Email':'电子邮箱',
    'Github':'Github',
    'Project':'项目地址',
    'tpws':'将要发送的文件(夹)路径',
    'tptp':'程序传输数据的端口号',
    'thtp':'将要发送的目的主机',
    'ctcs':'连接到指令套接字：',
    'cara':'无法绑定到目标地址',
    'fsd':"文件保存目录",
    'shs':"服务开启",
    'ra':"程序运行在",
    'wfft':"等待文件传输过来",
    'nc':'新客户进入',
    'ctds':'连接到数据套接字：',
    'aoc':'一个旧连接正在尝试恢复，但失败了',
    'st':'开始传输 ',
    'dd':'下载完毕',
    'pidp':'请输入文件夹路径',
    'dpif':'这个路径指向一个文件',
    'tdpw':'文件保存的路径',
    'yhim':'主动取消传输任务',
    'cmct':'完成任务耗时：',
    'fe':'文件已存在：',
}


class LanguageSelecter:
    def __init__(self):
        #print('LanguageSelecter create')
        self.lang = 'cn'
    def select_language(self,lang = 'cn'):
        self.lang = lang

    def auto_judge(self):
        if is_chinese_user():self.select_language('cn')
        else:self.select_language('en')

    def dict(self,key):
        if self.lang == 'cn':return cn.get(key)
        return en.get(key)

languageSelecter = LanguageSelecter()
languageSelecter.auto_judge()