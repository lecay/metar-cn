import pandas as pd
import cnmatar

def splitmetar(context):
	m = cnmatar.metar(context)
	return m.wind_dir,m.wind_speed,m.vis,m.rvr1,m.rvr2,m.ww1,m.ww2,m.tt,m.td,m.slp

filename = r'J:\影响天气\lecay\案例\20191107西安大雾\西安rvr低于550报文\ZLXY_METAR_SPECI 报文数据 (20190101-20191110).xls'
df = pd.DataFrame(pd.read_excel(filename))
usedata = df['内容'].apply(splitmetar, axis=1, result_type='expand')
print(usedata)

