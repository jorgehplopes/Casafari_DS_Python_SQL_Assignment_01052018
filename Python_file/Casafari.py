##################################### PART 1  #####################################

import pandas as pd
import matplotlib.pyplot as plt


#import data from CSV
df=pd.read_csv('D:/Casafari/assignment_data.csv',sep=',')


#Number of NAN registers
print("Number of NAN registers in features = "+str(sum(pd.isnull(df['features']))))
print("Number of NAN registers in title = "+str(sum(pd.isnull(df['title']))))


#lower case and remove special characters to "title" columns to best filter cases
title_low=[]
for n in list(df.index):
    title_low.append(df.loc[n,"title"].lower())

df.loc[:,"title_low"]=title_low
   

df["title_low"]=df.loc[:,"title_low"].str.replace("nagüeles","nagueles")


#create location column
location=[]   
for n in list(df.index):
    if "alenquer" in df.loc[n,"title_low"]:
         location.append("Alenquer")
    elif "quinta da marinha" in df.loc[n,"title_low"]:
         location.append("Quinta da Marinha")
    elif "nagueles" in df.loc[n,"title_low"]:
         location.append("Nagüeles") 
    elif "golden mile" in df.loc[n,"title_low"]:
         location.append("Golden Mile")

df.loc[:,"location"]=location


#create type column
type=[]   
for n in list(df.index):
    if ("apartment") in df.loc[n,"title_low"]:
         type.append("apartments")
    elif ("penthouse") in df.loc[n,"title_low"]:
         type.append("apartments")
    elif ("duplex") in df.loc[n,"title_low"]:
         type.append("apartments")    
    elif ("house") in df.loc[n,"title_low"]:
         type.append("houses")  
    elif ("villa") in df.loc[n,"title_low"]:
         type.append("houses")  
    elif ("country estate") in df.loc[n,"title_low"]:
         type.append("houses")           
    elif ("moradia") in df.loc[n,"title_low"]:
         type.append("houses")           
    elif ("quinta") in df.loc[n,"title_low"]:
         type.append("houses")           
    elif ("plot") in df.loc[n,"title_low"]:
         type.append("plots")           
    elif ("land") in df.loc[n,"title_low"]:
         type.append("plots")
    else:
        type.append("other")

df.loc[:,"type"]=type


#delete "other" type registers
df = df[df.type != "other"]


#create a checkpoint
df_aux=df


#drop lines with NAN in features column
df=df.dropna(axis=0, subset=['features'])


#lower case to feature columns to best filter
features_low=[]
for n in list(df.index):
    features_low.append(df.loc[n,"features"].lower())

df.loc[:,"features_low"]=features_low
 
        
#create pool dummy column
df.loc[:,"pool"] = df.features_low.str.contains("pool")
df.pool=df.pool.astype(int)


#create sea_view dummy column
df.loc[:,"sea_view"] = df.features_low.str.contains("sea view")
df.sea_view=df.sea_view.astype(int)


#create garage dummy column
df.loc[:,"garage"] = df.features_low.str.contains("garage")
df.garage=df.garage.astype(int)


#create table to export
deliverable1=df.loc[:,["id","location","type","title","features","pool","sea_view","garage"]]


#change columns names
deliverable1.columns=["id", "location name", "type", "title", "features", "pool (0/1)", "sea view (0/1)", "garage (0/1)"]


#export table to CSV
deliverable1.to_csv('D:/Casafari/deliverable1.csv',sep=',', encoding='utf-8', index=False)


#deliverable1.columns
#deliverable1.head(20)



##################################### PART 2  #####################################


#recover dataset before drop lines with NAN in features column
df=df_aux


#add area column
area=[]   
for n in list(df.index):
    if (df.loc[n,"type"]=="apartments") | (df.loc[n,"type"]=="houses"):
        area.append(max(df.loc[n,"total_area"],df.loc[n,"living_area"])) 
    elif(df.loc[n,"type"]=="plots"):
        area.append(df.loc[n,"plot_area"])

df.loc[:,"area"]=area


#drop lines with NAN in area and price column
df=df.dropna(axis=0, subset=['area'])
df=df.dropna(axis=0, subset=['price'])


#delete all lines with price = 0 and area = 0... it is not usefull for price calculations
df = df[df.price != 0]
df = df[df.area != 0]


#add price_area column
price_area=[]   
for n in list(df.index):
    price_area.append(df.loc[n,"price"]/df.loc[n,"area"])

df.loc[:,"price_area"]=price_area   
    
    
#add loc_type_mean_price column... is the mean price_area for a specific type in a specific location
loc_type_mean_price=[] 
for n in list(df.index):
    if (df.loc[n,"location"]=="Alenquer") & (df.loc[n,"type"]=="houses"):
        loc_type_mean_price.append(df[(df.location=="Alenquer")&(df.type=="houses")].price_area.mean())
    elif (df.loc[n,"location"]=="Alenquer") & (df.loc[n,"type"]=="apartments"):
        loc_type_mean_price.append(df[(df.location=="Alenquer")&(df.type=="apartments")].price_area.mean())  
    elif (df.loc[n,"location"]=="Alenquer") & (df.loc[n,"type"]=="plots"):
        loc_type_mean_price.append(df[(df.location=="Alenquer")&(df.type=="plots")].price_area.mean())      
    elif (df.loc[n,"location"]=="Quinta da Marinha") & (df.loc[n,"type"]=="houses"):
        loc_type_mean_price.append(df[(df.location=="Quinta da Marinha")&(df.type=="houses")].price_area.mean())
    elif (df.loc[n,"location"]=="Quinta da Marinha") & (df.loc[n,"type"]=="apartments"):
        loc_type_mean_price.append(df[(df.location=="Quinta da Marinha")&(df.type=="apartments")].price_area.mean())  
    elif (df.loc[n,"location"]=="Quinta da Marinha") & (df.loc[n,"type"]=="plots"):
        loc_type_mean_price.append(df[(df.location=="Quinta da Marinha")&(df.type=="plots")].price_area.mean())  
    elif (df.loc[n,"location"]=="Golden Mile") & (df.loc[n,"type"]=="houses"):
        loc_type_mean_price.append(df[(df.location=="Golden Mile")&(df.type=="houses")].price_area.mean())
    elif (df.loc[n,"location"]=="Golden Mile") & (df.loc[n,"type"]=="apartments"):
        loc_type_mean_price.append(df[(df.location=="Golden Mile")&(df.type=="apartments")].price_area.mean())  
    elif (df.loc[n,"location"]=="Golden Mile") & (df.loc[n,"type"]=="plots"):
        loc_type_mean_price.append(df[(df.location=="Golden Mile")&(df.type=="plots")].price_area.mean())         
    elif (df.loc[n,"location"]=="Nagüeles") & (df.loc[n,"type"]=="houses"):
        loc_type_mean_price.append(df[(df.location=="Nagüeles")&(df.type=="houses")].price_area.mean())
    elif (df.loc[n,"location"]=="Nagüeles") & (df.loc[n,"type"]=="apartments"):
        loc_type_mean_price.append(df[(df.location=="Nagüeles")&(df.type=="apartments")].price_area.mean())  
    elif (df.loc[n,"location"]=="Nagüeles") & (df.loc[n,"type"]=="plots"):
        loc_type_mean_price.append(df[(df.location=="Nagüeles")&(df.type=="plots")].price_area.mean())           
    else:
        loc_type_mean_price.append(0)

df.loc[:,"loc_type_mean_price"]=loc_type_mean_price


#add over_valued,under_valued, normal columns
over_valued=[]
under_valued=[]
normal=[]
valued_factor=0.15

for n in list(df.index):
    if (df.loc[n,"price_area"]>(1+valued_factor)*df.loc[n,"loc_type_mean_price"]):
        over_valued.append(1)
        under_valued.append(0)
        normal.append(0)
    elif (df.loc[n,"price_area"]<(1-valued_factor)*df.loc[n,"loc_type_mean_price"]):        
        over_valued.append(0)
        under_valued.append(1)
        normal.append(0)        
    else:
        over_valued.append(0)
        under_valued.append(0)
        normal.append(1)

df.loc[:,"over_valued"]=over_valued
df.loc[:,"under_valued"]=under_valued
df.loc[:,"normal"]=normal


#create table to export
deliverable2=df.loc[:,["id","location","type","area","price","over_valued","under_valued","normal"]]


#change columns names
deliverable2.columns=["id","location","type","area","price","over-valued (0/1)","under-valued (0/1)","normal (0/1)"]


#deliverable2.columns
#deliverable2.head(20)


#export table to CSV
deliverable2.to_csv('D:/Casafari/deliverable2.csv',sep=',', encoding='utf-8', index=False)


#add AUX columns       
conta_under=df.loc_type_mean_price*(1-valued_factor)
conta_over=df.loc_type_mean_price*(1+valued_factor)
df.loc[:,"conta_under"]=conta_under
df.loc[:,"conta_over"]=conta_over


#graphic AUX columns
df.loc[:,"aux1"]=1
df.loc[:,"aux2"]=2
df.loc[:,"aux3"]=3
df.loc[:,"aux4"]=4


#graphic by location without rating
fig, ax = plt.subplots()
s = 80
x1=df[df.location=="Alenquer"].price_area
y1=df[df.location=="Alenquer"].aux1
x2=df[df.location=="Quinta da Marinha"].price_area
y2=df[df.location=="Quinta da Marinha"].aux2
x3=df[df.location=="Golden Mile"].price_area
y3=df[df.location=="Golden Mile"].aux3
x4=df[df.location=="Nagüeles"].price_area
y4=df[df.location=="Nagüeles"].aux4
ax.scatter(x1, y1, color='r', s=s, marker='^', alpha=.4)
ax.scatter(x2, y2, color='b', s=s, marker='x', alpha=.4)
ax.scatter(x3, y3, color='g', s=s, marker='s', alpha=.4)
ax.scatter(x4, y4, color='k', s=s, marker='*', alpha=.4)
ax.set_yticklabels([])
ax.set_xlim(0, max(df.price_area)*1.2)

ax.text(5000, 1.25, 'Alenquer', fontsize=15)
ax.text(5000, 2.25, 'Quinta da Marinha', fontsize=15)
ax.text(5000, 3.25, 'Golden Mile', fontsize=15)
ax.text(5000, 4.25, 'Nagüeles', fontsize=15)

plt.xlabel("Price per area", fontsize=14)
plt.ylabel("Locations", fontsize=14)
plt.suptitle("Price per Area by Locations", fontsize=18)


#graphic by location with rating
fig, ax = plt.subplots()
x1=df[(df.location=="Alenquer")&(df.over_valued==1)].price_area
y1=df[(df.location=="Alenquer")&(df.over_valued==1)].aux1
x2=df[(df.location=="Alenquer")&(df.under_valued==1)].price_area
y2=df[(df.location=="Alenquer")&(df.under_valued==1)].aux1
x3=df[(df.location=="Alenquer")&(df.normal==1)].price_area
y3=df[(df.location=="Alenquer")&(df.normal==1)].aux1
x4=df[(df.location=="Quinta da Marinha")&(df.over_valued==1)].price_area
y4=df[(df.location=="Quinta da Marinha")&(df.over_valued==1)].aux2
x5=df[(df.location=="Quinta da Marinha")&(df.under_valued==1)].price_area
y5=df[(df.location=="Quinta da Marinha")&(df.under_valued==1)].aux2
x6=df[(df.location=="Quinta da Marinha")&(df.normal==1)].price_area
y6=df[(df.location=="Quinta da Marinha")&(df.normal==1)].aux2
x7=df[(df.location=="Golden Mile")&(df.over_valued==1)].price_area
y7=df[(df.location=="Golden Mile")&(df.over_valued==1)].aux3
x8=df[(df.location=="Golden Mile")&(df.under_valued==1)].price_area
y8=df[(df.location=="Golden Mile")&(df.under_valued==1)].aux3
x9=df[(df.location=="Golden Mile")&(df.normal==1)].price_area
y9=df[(df.location=="Golden Mile")&(df.normal==1)].aux3
x10=df[(df.location=="Nagüeles")&(df.over_valued==1)].price_area
y10=df[(df.location=="Nagüeles")&(df.over_valued==1)].aux4
x11=df[(df.location=="Nagüeles")&(df.under_valued==1)].price_area
y11=df[(df.location=="Nagüeles")&(df.under_valued==1)].aux4
x12=df[(df.location=="Nagüeles")&(df.normal==1)].price_area
y12=df[(df.location=="Nagüeles")&(df.normal==1)].aux4

ax.scatter(x1, y1, color='r', s=s, marker='^', alpha=.4, label="Over Valued")
ax.scatter(x2, y2, color='g', s=s, marker='^', alpha=.4, label="Under Valued")
ax.scatter(x3, y3, color='b', s=s, marker='^', alpha=.4, label="Normal")
ax.scatter(x4, y4, color='r', s=s, marker='x', alpha=.4, label="Over Valued")
ax.scatter(x5, y5, color='g', s=s, marker='x', alpha=.4, label="Under Valued")
ax.scatter(x6, y6, color='b', s=s, marker='x', alpha=.4, label="Normal")
ax.scatter(x7, y7, color='r', s=s, marker='s', alpha=.4, label="Over Valued")
ax.scatter(x8, y8, color='g', s=s, marker='s', alpha=.4, label="Under Valued")
ax.scatter(x9, y9, color='b', s=s, marker='s', alpha=.4, label="Normal")
ax.scatter(x10, y10, color='r', s=s, marker='*', alpha=.4, label="Over Valued")
ax.scatter(x11, y11, color='g', s=s, marker='*', alpha=.4, label="Under Valued")
ax.scatter(x12, y12, color='b', s=s, marker='*', alpha=.4, label="Normal")

ax.set_yticklabels([])
ax.set_xlim(0, max(df.price_area)*1.2)
legend = ax.legend(loc='upper right', fontsize=10)

ax.text(5000, 1.25, 'Alenquer', fontsize=15)
ax.text(5000, 2.25, 'Quinta da Marinha', fontsize=15)
ax.text(5000, 3.25, 'Golden Mile', fontsize=15)
ax.text(5000, 4.25, 'Nagüeles', fontsize=15)

plt.xlabel("Price per area", fontsize=14)
plt.ylabel("Locations", fontsize=14)
plt.suptitle("Price per Area by Locations", fontsize=18)


#graphic by type without rating
fig, ax = plt.subplots()
x1=df[df.type=="apartments"].price_area
y1=df[df.type=="apartments"].aux1
x2=df[df.type=="houses"].price_area
y2=df[df.type=="houses"].aux2
x3=df[df.type=="plots"].price_area
y3=df[df.type=="plots"].aux3

ax.scatter(x1, y1, color='r', s=s, marker='^', alpha=.4)
ax.scatter(x2, y2, color='b', s=s, marker='x', alpha=.4)
ax.scatter(x3, y3, color='g', s=s, marker='s', alpha=.4)

ax.set_yticklabels([])
ax.set_xlim(0, max(df.price_area)*1.2)

ax.text(5000, 1.25, 'Apartments', fontsize=15)
ax.text(5000, 2.25, 'Houses', fontsize=15)
ax.text(5000, 3.25, 'Plots', fontsize=15)

plt.xlabel("Price per area", fontsize=14)
plt.ylabel("Types", fontsize=14)
plt.suptitle("Price per Area by Types", fontsize=18)


#graphic by Types with rating
fig, ax = plt.subplots()
x1=df[(df.type=="apartments")&(df.over_valued==1)].price_area
y1=df[(df.type=="apartments")&(df.over_valued==1)].aux1
x2=df[(df.type=="apartments")&(df.under_valued==1)].price_area
y2=df[(df.type=="apartments")&(df.under_valued==1)].aux1
x3=df[(df.type=="apartments")&(df.normal==1)].price_area
y3=df[(df.type=="apartments")&(df.normal==1)].aux1
x4=df[(df.type=="houses")&(df.over_valued==1)].price_area
y4=df[(df.type=="houses")&(df.over_valued==1)].aux2
x5=df[(df.type=="houses")&(df.under_valued==1)].price_area
y5=df[(df.type=="houses")&(df.under_valued==1)].aux2
x6=df[(df.type=="houses")&(df.normal==1)].price_area
y6=df[(df.type=="houses")&(df.normal==1)].aux2
x7=df[(df.type=="plots")&(df.over_valued==1)].price_area
y7=df[(df.type=="plots")&(df.over_valued==1)].aux3
x8=df[(df.type=="plots")&(df.under_valued==1)].price_area
y8=df[(df.type=="plots")&(df.under_valued==1)].aux3
x9=df[(df.type=="plots")&(df.normal==1)].price_area
y9=df[(df.type=="plots")&(df.normal==1)].aux3

ax.scatter(x1, y1, color='r', s=s, marker='^', alpha=.4, label="Over Valued")
ax.scatter(x2, y2, color='g', s=s, marker='^', alpha=.4, label="Under Valued")
ax.scatter(x3, y3, color='b', s=s, marker='^', alpha=.4, label="Normal")
ax.scatter(x4, y4, color='r', s=s, marker='x', alpha=.4, label="Over Valued")
ax.scatter(x5, y5, color='g', s=s, marker='x', alpha=.4, label="Under Valued")
ax.scatter(x6, y6, color='b', s=s, marker='x', alpha=.4, label="Normal")
ax.scatter(x7, y7, color='r', s=s, marker='s', alpha=.4, label="Over Valued")
ax.scatter(x8, y8, color='g', s=s, marker='s', alpha=.4, label="Under Valued")
ax.scatter(x9, y9, color='b', s=s, marker='s', alpha=.4, label="Normal")

legend = ax.legend(loc='upper right', fontsize=10)
ax.set_yticklabels([])
ax.set_xlim(0, max(df.price_area)*1.2)

ax.text(5000, 1.25, 'Apartments', fontsize=15)
ax.text(5000, 2.25, 'Houses', fontsize=15)
ax.text(5000, 3.25, 'Plots', fontsize=15)

plt.xlabel("Price per area", fontsize=14)
plt.ylabel("Types", fontsize=14)
plt.suptitle("Price per Area by Types", fontsize=18)


