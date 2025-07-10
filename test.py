
cdate="16-03-2024"
cd1=cdate.split("-")

#between date
sdate="25-02-2024"
edate="15-03-2024"
sd1=sdate.split('-')
ed1=sdate.split('-')
import datetime
sdd = datetime.datetime(int(sd1[2]), int(sd1[1]),int(sd1[0]))
cdd = datetime.datetime(int(cd1[2]), int(cd1[1]),int(cd1[0]))
edd = datetime.datetime(int(ed1[2]), int(ed1[1]),int(ed1[0]))
#print(d1<d2<d3)
#print(d2<d1<d3)   

if sdd<cdd<edd:
    date_st='1'
else:
    date_st='2'


print(date_st)
