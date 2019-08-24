
import re

class metar(object):
    def __init__(self, rawmetar):
        raw = re.split(r'\s+', rawmetar)
        self.all = raw    #所有字段
        self.isspeci = False
        self.isauto = False
        self.iscor = False
        self.wind_dir = self.wind_speed = self.wind_gust = None
        self.wind_dir_from = self.wind_dir_to = None
        self.vis = None
        self.rw1 = self.rw2 = self.rw3 = self.rw4 = None
        self.rvr1 = self.rvr2 = self.rvr3 = self.rvr4 = None
        self.rvrtd1 = self.rvrtd2 = self.rvrtd3 = self.rvrtd4 = None
        self.rvr1v = self.rvr2v = self.rvr3v = self.rvr4v = None
        self.ww = []
        self.ww1 = self.ww2 = self.ww3 = None
        self.cl = []
        self.clcover1 = self.clcover2 = self.clcover3 = self.clcover4 = None
        self.clf1 = self.clf2 = self.clf3 = self.clf4 = None 
        self.clh1 = self.clh2 = self.clh3 = self.clh4 = None
        self.tt = self.td = None
        self.slp = None
        self.pww = None
        self.ws = False
        self.wsrw = None
        for ri,r in enumerate(raw):
            if re.search(r'NOSIG|BECMG|TEMPO', r):    #识别趋势报
                break
            if re.search(r'SPECI', r):    
                self.isspeci = True    #是否为SPECI报
            if re.search(r'AUTO', r):
                self.isauto = True    #是否为AUTO报
            if re.search(r'COR|AMD', r):
                self.iscor = True    #是否为COR/AMD报
            if ri<4 and re.search(r'^Z[A-Z]{3}$', r):
                self.airport = r    #机场四字码
            if re.search(r'\d{6}Z', r):
                self.time = r[0:6]    #发报时间
            wind = re.search(r'(\w{3})(\d{2})G?(\d{2})?MPS', r)
            if wind:
                self.wind_dir = wind.group(1)    #风向
                self.wind_speed = wind.group(2)    #平均风速
                self.wind_gust = wind.group(3)    #阵风风速
            if re.match(r'\d{3}V\d{3}', r):
                self.wind_dir_from = r[0:3]    #风向变化
                self.wind_dir_to = r[4:7]
            if re.search(r'^\d{4}$', r):
                self.vis = r        #能见度
            if re.search(r'CAVOK', r):
                self.vis = 9999
            rvr = re.search(r'^R(\w{2,3})/([MP]?\d{4})([UDN]?)V?([MP]?\d{4})?([UDN]?)', r)
            if rvr:                #RVR（最多4组）
                if self.rw1 is None:
                    self.rw1 = rvr.group(1)    #RVR跑道号
                    self.rvr1 = rvr.group(2)    #RVR值
                    if rvr.group(3):
                        self.rvrtd1 = rvr.group(3)    #RVR趋势
                    elif rvr.group(5):
                        self.rvrtd1 = rvr.group(5)
                    self.rvr1v = rvr.group(4)    #RVR变化组最大值（此时rvr1为最小值）
                elif (self.rw1 is not None) and (self.rw2 is None):
                    self.rw2 = rvr.group(1)
                    self.rvr2 = rvr.group(2)
                    if rvr.group(3):
                        self.rvrtd2 = rvr.group(3)
                    elif rvr.group(5):
                        self.rvrtd2 = rvr.group(5)
                    self.rvr2v = rvr.group(4) 
                elif (self.rw2 is not None) and (self.rw3 is None):
                    self.rw3 = rvr.group(1)
                    self.rvr3 = rvr.group(2)
                    if rvr.group(3):
                        self.rvrtd3 = rvr.group(3)
                    elif rvr.group(5):
                        self.rvrtd3 = rvr.group(5)
                    self.rvr3v = rvr.group(4)                   
                elif (self.rw3 is not None) and (self.rw4 is None):
                    self.rw4 = rvr.group(1)
                    self.rvr4 = rvr.group(2)
                    if rvr.group(3):
                        self.rvrtd4 = rvr.group(3)
                    elif rvr.group(5):
                        self.rvrtd4 = rvr.group(5)
                    self.rvr4v = rvr.group(4) 
            if ri>4 and re.search(r'(?<!RE)(SH|TS|DZ|RA|SN|SG|GS|GR|IC|PL|BR|FG|FU|DU|HZ|SA|VA|PO|SQ|FC|SS|DS)',r):
                self.ww.append(r)      #所有天气现象（列表）
                if self.ww1 is None:
                    self.ww1 = r       #单个天气现象（最多3组）
                elif (self.ww1 is not None) and (self.ww2 is None):
                    self.ww2 = r
                elif (self.ww2 is not None) and (self.ww3 is None):
                    self.ww3 = r
            cloud = re.search(r'^(FEW|SCT|BKN|OVC|VV)(\d{3})(CB|TCU)?', r)
            if cloud:
                self.cl.append(r)
                if self.clcover1 is None:
                    self.clcover1 = cloud.group(1)    #云量（含VV，最多4组）
                    self.clh1 = cloud.group(2)        #云高
                    self.clf1 = cloud.group(3)        #云状（CB或TCU）
                elif (self.clcover1 is not None) and (self.clcover2 is None):
                    self.clcover2 = cloud.group(1)
                    self.clh2 = cloud.group(2)
                    self.clf2 = cloud.group(3)
                elif (self.clcover2 is not None) and (self.clcover3 is None):
                    self.clcover3 = cloud.group(1)
                    self.clh3 = cloud.group(2)
                    self.clf3 = cloud.group(3)     
                elif (self.clcover3 is not None) and (self.clcover4 is None):
                    self.clcover4 = cloud.group(1)
                    self.clh4 = cloud.group(2)
                    self.clf4 = cloud.group(3)
            temp = re.match(r'(M?\d{2})/(M?\d{2})', r)
            if temp:
                self.tt = temp.group(1).replace('M','-')    #温度（并用-代替M）
                self.td = temp.group(2).replace('M','-')    #露点
            if re.search(r'^Q\d{4}', r):
                self.slp = r[1:5]        #海平面气压
            if re.search(r'^RE', r):
                self.pww = r[2:]      #过去天气
            if re.search(r'WS', r):
                self.ws = True         #是否有风切变
            if re.search(r'ALL', r):
                self.wsrw = 'ALL'      #风切变跑道
            if re.search(r'^RWY\w{2,3}', r):
                self.wsrw = r[3:]

    def info(self):      #显示分解后的信息
        lines = []
        lines.append('%s %sz' % (self.airport, self.time))

        typelist = ''
        if self.isspeci:
            typelist = typelist+' SPECI'
        if self.iscor:
            typelist = typelist+' COR'
        if self.isauto:
            typelist = typelist+' AUTO'
        if typelist:
            lines.append('Type:%s' % typelist)
        
        windlist = ''
        if self.wind_dir:
            windlist = windlist+' '+self.wind_dir+'°'
        if self.wind_dir_from:
            windlist = windlist+' ('+self.wind_dir_from+'°v'+self.wind_dir_to+'°)'
        if self.wind_speed:
            windlist = windlist+'  '+str(int(self.wind_speed))+'mps'
        if self.wind_gust:
            windlist = windlist+' Gale:'+str(int(self.wind_gust))+'mps'
        if windlist:
            lines.append('Wind:%s' % windlist)

        if self.vis:
            lines.append('VIS: %dm' % int(self.vis))

        rvrlist = ''
        if self.rw1:
            rvrlist = rvrlist+' R'+self.rw1
        if self.rvr1:
            if self.rvr1=='P2000':
                rvrlist = rvrlist+' '+self.rvr1+'m' 
            else:
                rvrlist = rvrlist+' '+str(int(self.rvr1))+'m' 
        if self.rvr1v:
            if self.rvr1v=='P2000':
                rvrlist = rvrlist+'-'+self.rvr1v+'m'
            else:
                rvrlist = rvrlist+'-'+str(int(self.rvr1v))+'m'
        if self.rvrtd1:
            rvrlist = rvrlist+' '+self.rvrtd1
        if self.rw2:
            rvrlist = rvrlist+' | R'+self.rw2
        if self.rvr2:
            if self.rvr2=='P2000':
                rvrlist = rvrlist+' '+self.rvr2+'m' 
            else:
                rvrlist = rvrlist+' '+str(int(self.rvr2))+'m' 
        if self.rvr2v:
            if self.rvr2v=='P2000':
                rvrlist = rvrlist+'-'+self.rvr2v+'m'
            else:
                rvrlist = rvrlist+'-'+str(int(self.rvr2v))+'m'
        if self.rvrtd2:
            rvrlist = rvrlist+' '+self.rvrtd2
        if self.rw3:
            rvrlist = rvrlist+' | R'+self.rw3
        if self.rvr3:
            if self.rvr3=='P2000':
                rvrlist = rvrlist+' '+self.rvr3+'m' 
            else:
                rvrlist = rvrlist+' '+str(int(self.rvr3))+'m' 
        if self.rvr3v:
            if self.rvr3v=='P2000':
                rvrlist = rvrlist+'-'+self.rvr3v+'m'
            else:
                rvrlist = rvrlist+'-'+str(int(self.rvr3v))+'m'
        if self.rvrtd3:
            rvrlist = rvrlist+' '+self.rvrtd3
        if self.rw4:
            rvrlist = rvrlist+' | R'+self.rw4
        if self.rvr4:
            if self.rvr4=='P2000':
                rvrlist = rvrlist+' '+self.rvr4+'m' 
            else:
                rvrlist = rvrlist+' '+str(int(self.rvr4))+'m' 
        if self.rvr4v:
            if self.rvr4v=='P2000':
                rvrlist = rvrlist+'-'+self.rvr4v+'m'
            else:
                rvrlist = rvrlist+'-'+str(int(self.rvr4v))+'m'
        if self.rvrtd4:
            rvrlist = rvrlist+' '+self.rvrtd4
        if rvrlist:
            lines.append('RVR:%s' % rvrlist)

        wwlist = ''
        if self.ww1:
            wwlist = wwlist+' '+self.ww1
        if self.ww2:
            wwlist = wwlist+' '+self.ww2
        if self.ww3:
            wwlist = wwlist+' '+self.ww3
        if self.pww:
            wwlist = wwlist+' (RE'+self.pww+')'
        if self.ws:
            wwlist = wwlist+' (WS '+self.wsrw+')'
        if wwlist:
            lines.append('Weather:%s' % wwlist)

        cloudlist = ''
        if self.clcover1:
            cloudlist = cloudlist+' '+self.clcover1
        if self.clh1:
            cloudlist = cloudlist+' '+str(int(self.clh1)*30)+'m'
        if self.clf1:
            cloudlist = cloudlist+' '+self.clf1
        if self.clcover2:
            cloudlist = cloudlist+' | '+self.clcover2
        if self.clh2:
            cloudlist = cloudlist+' '+str(int(self.clh2)*30)+'m'
        if self.clf2:
            cloudlist = cloudlist+' '+self.clf2
        if self.clcover3:
            cloudlist = cloudlist+' | '+self.clcover3
        if self.clh3:
            cloudlist = cloudlist+' '+str(int(self.clh3)*30)+'m'
        if self.clf3:
            cloudlist = cloudlist+' '+self.clf3
        if self.clcover4:
            cloudlist = cloudlist+' | '+self.clcover4
        if self.clh4:
            cloudlist = cloudlist+' '+str(int(self.clh4)*30)+'m'
        if self.clf4:
            cloudlist = cloudlist+' '+self.clf4
        if cloudlist:
            lines.append('Cloud:%s' % cloudlist)

        if self.tt or self.td:
            lines.append('T/Td: %d°C/%d°C' % (int(self.tt), int(self.td)))
        if self.slp:
            lines.append('SLP: %dhPa' % int(self.slp))

        lines.append('METAR: '+rawmetar)
        return '\n'.join(lines)
