#!/usr/bin/env python3
from graficos_agregados import reconcile,build
def v(x,y=2025,status="observado"):
 return {"latest":{"year":y,"value":x,"status":status}}
def main():
 d={"variables":{"tributos_imobiliarios":v(100),"dca_iptu_principal":v(60),"dca_itbi_principal":v(40)}}
 ok,bad=reconcile(d)
 assert len(ok)==1 and ok[0][0]=="tributos_imobiliarios"
 assert "60,0%" in build(d) and "40,0%" in build(d)
 d["variables"]["dca_itbi_principal"]=v(41)
 assert not reconcile(d)[0] and "reconciliação" in build(d)
 d["variables"]["dca_itbi_principal"]=v(40,2024)
 assert not reconcile(d)[0]
 d["variables"]["dca_itbi_principal"]=v(40,status="ausente")
 assert not reconcile(d)[0]
 d["variables"]["dca_itbi_principal"]=v(40)
 d["variables"]["dca_iptu_principal"]=v(-1)
 assert not reconcile(d)[0]
 print("QA agregados: igualdade, ano, ausencia e invalidez OK")
if __name__=="__main__":main()
