
import pandas as pd
import cnmatar

# file = r'ZWWW.xls'
# df = pd.DataFrame(pd.read_excel(file, header=None, names=['id','time','raw']))
# for ri,r in enumerate(df['raw']):
# 	data = cnmatar.metar(r)
# 	if int(data.rvr1)<=550 or int(data.rvr2)<=550:
# 		print(ri,df['time'][ri],r)


a = 'SPECI ZLXY 201907Z 35001MPS 1400 R05L/0500D R05R/P2000 BR PRFG NSC 13/13 Q1012 NOSIG='
data = cnmatar.metar(a)
#aa = data.info
print(data.info())