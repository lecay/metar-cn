
import pandas as pd
import cnmatar

# file = r'ZWWW.xls'
# df = pd.DataFrame(pd.read_excel(file, header=None, names=['id','time','raw']))
# for ri,r in enumerate(df['raw']):
# 	data = cnmatar.metar(r)
# 	if int(data.rvr1)<=550 or int(data.rvr2)<=550:
# 		print(ri,df['time'][ri],r)


a = 'SPECI ZSNB 030614Z 06004MPS 010V090 9999 -TS BKN023 SCT026CB 31/25 Q1006 RESHRA BECMG TL0640 TSRA='
data = cnmatar.metar(a)
#aa = data.info
print(data.ww2)