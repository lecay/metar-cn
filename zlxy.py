import pandas as pd
import cnmatar

def splitmetar(context):
	m = cnmatar.metar(context)
	return pd.Series({'wind_dir':m.wind_dir, 'wind_speed':m.wind_speed, 'vis':m.vis, 'rvr1':m.rvr1, 'rvr2':m.rvr2,
                    'ww1':m.ww1, 'ww2':m.ww2, 'tt':m.tt, 'td':m.td, 'slp':m.slp})

#filename = r'J:\影响天气\lecay\案例\20191107西安大雾\西安rvr低于550报文\ZLXY_METAR_SPECI 报文数据 (20190101-20191110).xls'
filename = r'F:\MF\案例\20191107西安大雾\西安rvr低于550报文\ZLXY_METAR_SPECI 报文数据 (20190101-20191110).xls'
df = pd.DataFrame(pd.read_excel(filename))
usedata = df['内容'].apply(splitmetar)
newdf = pd.concat([df['时间'], usedata], axis=1)
print(newdf)

'''
import os
import pandas as pd
# 将文件读取出来放一个列表里面
pwd = 'test'  # 获取文件目录
# 新建列表，存放文件名
file_list = []
# 新建列表存放每个文件数据(依次读取多个相同结构的Excel文件并创建DataFrame)
dfs = []
for root,dirs,files in os.walk(pwd):  # 第一个为起始路径，第二个为起始路径下的文件夹，第三个是起始路径下的文件。
    for file in files:
        file_path = os.path.join(root, file)
        file_list.append(file_path) # 使用os.path.join(dirpath, name)得到全路径
        df = pd.read_excel(file_path) # 将excel转换成DataFrame
        dfs.append(df)
# 将多个DataFrame合并为一个
df = pd.concat(dfs)
# 写入excel文件，不包含索引数据
df.to_excel('test\\result.xls', index=False)
'''