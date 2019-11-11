import pandas as pd
import cnmatar

filename = r'J:\影响天气\lecay\案例\20191107西安大雾\西安rvr低于550报文\ZLXY_METAR_SPECI 报文数据 (20190101-20191110).xls'
df = pd.DataFrame(pd.read_excel(filename))
print(df['内容'])