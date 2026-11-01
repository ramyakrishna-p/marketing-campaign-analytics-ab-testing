import numpy as np, pandas as pd, json, pathlib
from scipy import stats
np.random.seed(7)
root=pathlib.Path(__file__).parent; (root/"data").mkdir(exist_ok=True); (root/"results").mkdir(exist_ok=True)
channels=["Email","Social","Search","Display"]; rows=[]
for i in range(4000):
    ch=np.random.choice(channels,p=[.3,.3,.25,.15]); imp=1
    ctr={"Email":.22,"Social":.14,"Search":.18,"Display":.08}[ch]
    clicked=int(np.random.random()<ctr); conv=0; rev=0.0; cost=float(np.random.uniform(0.5,3.0))
    variant=np.random.choice(["A","B"],p=[.5,.5])
    # B lifts conversion
    base={"Email":.18,"Social":.12,"Search":.20,"Display":.07}[ch]; pconv=base*(1.25 if variant=="B" else 1.0)
    if clicked: conv=int(np.random.random()<pconv); rev=float(conv*np.random.uniform(30,120))
    rows.append([i,ch,variant,imp,clicked,conv,round(cost,2),round(rev,2)])
df=pd.DataFrame(rows,columns=["user_id","channel","variant","impressions","clicks","conversions","cost","revenue"])
df.to_csv(root/"data/campaign.csv",index=False)
chan=df.groupby("channel").agg(impressions=("impressions","sum"),clicks=("clicks","sum"),conversions=("conversions","sum"),cost=("cost","sum"),revenue=("revenue","sum"))
chan["ctr"]=chan.clicks/chan.impressions; chan["conversion_rate"]=chan.conversions/chan.clicks.replace(0,np.nan); chan["roi"]=(chan.revenue-chan.cost)/chan.cost
a=df[df.variant=="A"]; b=df[df.variant=="B"]
# conversion among clickers, chi-square
table=np.array([[a.conversions.sum(), a.clicks.sum()-a.conversions.sum()],[b.conversions.sum(), b.clicks.sum()-b.conversions.sum()]])
chi2,p,_,_=stats.chi2_contingency(table)
summary={"rows":len(df),"overall_ctr":round(float(df.clicks.sum()/df.impressions.sum()),4),"overall_conversion_rate_clickers":round(float(df.conversions.sum()/max(df.clicks.sum(),1)),4),"total_cost":round(float(df.cost.sum()),2),"total_revenue":round(float(df.revenue.sum()),2),"overall_roi":round(float((df.revenue.sum()-df.cost.sum())/df.cost.sum()),4),"best_channel_by_roi":str(chan.roi.idxmax()),"best_channel_roi":round(float(chan.roi.max()),4),"variant_A_conv_rate":round(float(a.conversions.sum()/max(a.clicks.sum(),1)),4),"variant_B_conv_rate":round(float(b.conversions.sum()/max(b.clicks.sum(),1)),4),"ab_chi2":round(float(chi2),4),"ab_p_value":float(p),"ab_significant_0_05":bool(p<0.05),"channel_table":chan.round(4).to_dict(orient="index")}
(root/"results/summary.json").write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
