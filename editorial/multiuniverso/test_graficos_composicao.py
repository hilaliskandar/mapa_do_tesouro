#!/usr/bin/env python3
from graficos_composicao import build
def v(value,year=2025,status="observado"):
 return {"latest":{"value":value,"year":year,"status":status}}
def main():
 d={"variables":{"dca_receita_tributaria_bruta":v(20),"dca_receita_corrente_bruta":v(100),
  "dca_investimentos_liquidada":v(15),"dca_despesa_total_liquidada":v(60),
  "dca_despesa_corrente_liquidada":v(42)}}
 page=build(d)
 assert page.count('class="chart-card"')==3
 assert "20,0%" in page and "25,0%" in page and "70,0%" in page
 d["variables"]["dca_receita_tributaria_bruta"]=v(20,2024)
 assert build(d).count('class="chart-card"')==2
 d["variables"]["dca_investimentos_liquidada"]=v(65)
 assert build(d).count('class="chart-card"')==1
 d["variables"]["dca_despesa_corrente_liquidada"]=v(None,status="ausente")
 assert "Nenhum valor foi estimado" in build(d)
 print("QA composicao: anos, positivos, limites e ausencias aprovados")
if __name__=="__main__":main()
