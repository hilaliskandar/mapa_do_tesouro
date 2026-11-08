#!/usr/bin/env python3
"""Render deterministic and auditable WebP SWOT plates for RMRP G30 RC1.
Values and prose transcribed from the subregional Q4-Q7 analyses, no outside estimates.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, re, math

W,H=2100,1580
OUT=Path('/mnt/data')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
COLORS={"navy":"#172F48","ink":"#22334A","muted":"#536B80","line":"#D2DDE7","teal":"#1F6182","light":"#F5F8FC","green":"#2F754E","red":"#AA4C46","blue":"#276993","gold":"#956E1C"}
REGIONS=[
{"q":4,"name":"Ribeirão Preto","slug":"ribeirao-preto","count":15,"reduction":38.82,"swot":{
"Forças":"A sub-região reúne a maior concentração identificada de investimentos no município-polo e a exceção de Cravinhos, único município com expansão nominal nos dois intervalos do triênio. A diversidade de escala e de intensidade oferece base para estratégias territoriais diferenciadas.",
"Fraquezas":"A concentração dos montantes no polo expõe o agregado à sua oscilação anual. Em diversos municípios, a execução de capital recuou muito mais que a receita corrente, com participação inferior a 1% em 2025; a situação de Jardinópolis, Pontal e São Simão é especialmente relevante para uma análise de continuidade de obras e equipamentos.",
"Oportunidades":"Cooperação entre municípios próximos para estruturar projetos compartilhados, quando demonstrada sua viabilidade técnica e institucional, pode diminuir custos de preparação e ampliar escala de serviços. A existência dessa alternativa não constitui evidência de carteira contratada.",
"Ameaças":"A eventual redução ou atraso de recursos externos vinculados a projetos específicos pode afetar municípios com baixa intensidade de investimento e execução volátil. Alterações na agenda de obras do polo também podem modificar a leitura regional sem se reproduzir em cada município.",
"Síntese estratégica":"O planejamento sub-regional precisa monitorar separadamente o volume de Ribeirão Preto e a evolução dos municípios menores, evitando que a escala do polo oculte situações de investimento residual. A participação contábil observada de ISS e ICMS não constitui projeção da receita futura do IBS."}},
{"q":5,"name":"Jaboticabal","slug":"jaboticabal","count":6,"reduction":55.29,"swot":{
"Forças":"A execução de capital não está restrita a um único município; Guariba e Jaboticabal têm peso relevante na série, ainda que com retrações. A diversidade de padrões municipais permite avaliar continuidade e recuperação com maior granularidade.",
"Fraquezas":"A forte contração real da sub-região combina queda persistente em alguns municípios com reversões abruptas após 2024. A intensidade de 0,82% registrada em Taquaral em 2025, inferior aos 2,08% sub-regionais, ilustra a fragilidade de utilizar picos isolados como sinal de capacidade permanente.",
"Oportunidades":"A organização compartilhada de projetos de infraestrutura e a melhor sincronização de etapas de licitação, contratação e liquidação podem contribuir para reduzir descontinuidades, desde que respaldadas em carteiras municipais concretas.",
"Ameaças":"Projetos que dependam de etapas de formalização e de desembolso de outros entes podem apresentar diferença entre valor previsto, contratado e efetivamente pago. O caso documentado da escola integral de Guariba exemplifica a necessidade de manter essa distinção, sem pressupor inadimplemento.",
"Síntese estratégica":"A prioridade analítica é identificar se a redução da liquidação representa conclusão de obras, adiamento de execução ou menor incorporação de novos investimentos; os agregados disponíveis não distinguem essas causas e não autorizam imputar uma delas. A participação contábil observada de ISS e ICMS não constitui projeção da receita futura do IBS."}},
{"q":6,"name":"Mococa","slug":"mococa","count":6,"reduction":24.31,"swot":{
"Forças":"A sub-região apresentou a menor retração agregada entre os quatro agrupamentos e contém municípios com expansão real do investimento entre os extremos do triênio. Sua heterogeneidade oferece maior amplitude para examinar diferentes padrões de execução.",
"Fraquezas":"A média sub-regional esconde retrações extremas: Santa Cruz da Esperança viu a intensidade dos investimentos cair de 11,07% para 1,23%; Cássia dos Coqueiros, de 9,77% para 1,93%. O agregado relativamente favorável não representa preservação generalizada dos investimentos municipais.",
"Oportunidades":"Projetos cuja escala ultrapasse a capacidade de preparação individual de municípios pequenos podem ser considerados em arranjos intermunicipais, sujeitos à comprovação de demanda, competência e fonte de recursos.",
"Ameaças":"A combinação de investimentos voláteis e receitas de transferências condicionadas à conjuntura pode comprometer previsibilidade de projetos, sem permitir inferência automática sobre a situação de caixa ou sobre limites da LRF.",
"Síntese estratégica":"A menor retração regional não deve reduzir a atenção às cidades com quedas mais pronunciadas; indicadores agregados precisam ser lidos em conjunto com a dispersão municipal. A participação contábil observada de ISS e ICMS não constitui projeção da receita futura do IBS."}},
{"q":7,"name":"Batatais","slug":"batatais","count":7,"reduction":56.50,"swot":{
"Forças":"A intensidade relativa dos investimentos em Nuporanga, superior à média sub-regional em 2025, demonstra que o conjunto não é homogêneo. Em alguns municípios, as receitas correntes apresentaram crescimento real, o que diferencia restrição de receita agregada de redução da aplicação em capital.",
"Fraquezas":"A retração real agregada foi a mais profunda da RMRP. Altinópolis e Sales Oliveira encerraram 2025 com investimentos inferiores a 1% da receita corrente; Morro Agudo apresentou queda nominal contínua e perda significativa de intensidade.",
"Oportunidades":"O ordenamento de prioridades e a preparação de projetos de execução plurianual podem contribuir para reduzir a dependência de picos orçamentários, desde que amparados em diagnósticos setoriais e fontes viáveis de financiamento.",
"Ameaças":"Atrasos em transferências discricionárias ou aumentos de custos de projetos poderiam aprofundar a descontinuidade da execução, sobretudo onde a intensidade de investimentos já terminou o triênio em patamar muito baixo.",
"Síntese estratégica":"A comparação entre Nuporanga e os municípios de execução residual mostra que a trajetória temporal e a posição relativa em 2025 devem ser acompanhadas simultaneamente, sob pena de se ocultar a heterogeneidade do grupo. A participação contábil observada de ISS e ICMS não constitui projeção da receita futura do IBS."}}]

def wrap(draw, txt, font, width):
    words=txt.split(' ');lines=[];line=''
    for word in words:
        candidate=(line+' '+word).strip()
        if line and draw.textbbox((0,0),candidate,font=font)[2]>width:
            lines.append(line);line=word
        else: line=candidate
    if line:lines.append(line)
    return lines

def paragraph(draw, text, x,y,width,height,color,fontsize=27,spacing=9):
    ff=f(fontsize)
    lines=wrap(draw,text,ff,width)
    lineheight=fontsize+spacing
    if len(lines)*lineheight>height:
        ff=f(fontsize-2);lines=wrap(draw,text,ff,width);lineheight=fontsize+spacing-3
    assert len(lines)*lineheight<=height,(text[:40],len(lines),height)
    for i,s in enumerate(lines):draw.text((x,y+i*lineheight),s,font=ff,fill=color)
    return len(lines)

def rectangle(draw, xy, fill, outline=None, radius=12,width=2):draw.rounded_rectangle(xy,fill=fill,outline=outline,radius=radius,width=width)

def card(draw,x,y,w,h,label,body,color,head_color):
    rectangle(draw,(x,y,x+w,y+h),'#FFFFFF',outline=color,radius=15,width=3)
    rectangle(draw,(x+1,y+1,x+w-1,y+64),head_color,radius=14)
    draw.rectangle((x+1,y+47,x+w-1,y+64),fill=head_color)
    draw.text((x+27,y+11),label,font=f(33,True),fill=color)
    paragraph(draw,body,x+27,y+88,w-54,h-101,COLORS['ink'],27,10)

def two_bars(draw,x,y,left,baseline,index):
    plot_x=x+140;plot_w=760;bar_h=39
    draw.text((x,y),"INVESTIMENTO LIQUIDADO · ÍNDICE REAL (2023 = 100)",font=f(29,True),fill=COLORS['navy'])
    for row,(yr,v,color) in enumerate([(2023,100.0,COLORS['navy']),(2025,index,'#448DB9')]):
        yy=y+64+row*86
        draw.text((x,yy+2),str(yr),font=f(31,True),fill=COLORS['ink'])
        rectangle(draw,(plot_x,yy,plot_x+plot_w,yy+bar_h),'#DFE9F2',radius=7)
        rectangle(draw,(plot_x,yy,plot_x+round(plot_w*v/100),yy+bar_h),color,radius=7)
        draw.text((plot_x+plot_w+22,yy+1),f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.'),font=f(30,True),fill=COLORS['ink'])
    return plot_x,plot_w

def render(r):
    im=Image.new('RGB',(W,H),'#FFFFFF');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,12),fill=COLORS['navy'])
    d.rectangle((70,65,85,207),fill=COLORS['teal'])
    d.text((113,68),f"Quadro Q{r['q']} — Matriz SWOT",font=f(56,True),fill=COLORS['navy'])
    d.text((113,143),f"Sub-região de {r['name']}",font=f(43),fill=COLORS['navy'])
    d.text((115,213),"FINANÇAS MUNICIPAIS • INVESTIMENTOS • DIFERENCIAÇÃO TERRITORIAL",font=f(23),fill=COLORS['muted'])
    rectangle(d,(1434,58,2020,211),'#EAF0F7',outline='#B9C9DA',radius=14)
    d.text((1470,83),f"{r['count']} municípios",font=f(38,True),fill=COLORS['navy'])
    d.text((1470,143),f"Investimentos: −{r['reduction']:.2f}%".replace('.',','),font=f(34,True),fill=COLORS['red'])
    x1,x2=65,1062; cw=970
    card(d,x1,275,cw,307,'Forças',r['swot']['Forças'],COLORS['green'],'#DDF1E2')
    card(d,x2,275,cw,307,'Fraquezas',r['swot']['Fraquezas'],COLORS['red'],'#F9E2DE')
    card(d,x1,608,cw,275,'Oportunidades',r['swot']['Oportunidades'],COLORS['blue'],'#DFEEF9')
    card(d,x2,608,cw,275,'Ameaças',r['swot']['Ameaças'],COLORS['gold'],'#FAEDD5')
    rectangle(d,(65,908,2032,1199),'#F4F7FB',outline='#C7D6E4',radius=16)
    plot_x,plot_w=two_bars(d,99,928,0,0,100-r['reduction'])
    d.line((1206,950,1206,1167),fill='#B5C7D7',width=3)
    d.text((1255,934),'VARIAÇÃO REAL AGREGADA',font=f(28,True),fill=COLORS['navy'])
    d.text((1254,1007),f"−{r['reduction']:.2f}%".replace('.',','),font=f(62,True),fill=COLORS['red'])
    d.text((1255,1087),f"{r['count']} municípios na sub-região",font=f(28),fill=COLORS['ink'])
    d.text((1255,1138),'2023–2025 · não é variação per capita',font=f(21),fill=COLORS['muted'])
    rectangle(d,(65,1228,2032,1449),'#E8F0F7',outline='#CAD6E3',radius=14)
    d.text((98,1252),'SÍNTESE ESTRATÉGICA',font=f(32,True),fill=COLORS['navy'])
    paragraph(d,r['swot']['Síntese estratégica'],98,1312,1900,126,COLORS['ink'],27,10)
    d.line((65,1470,2032,1470),fill='#9FADBB',width=2)
    d.text((70,1492),'Fonte: Volume II — Finanças municipais da Região Metropolitana de Ribeirão Preto (G30 RC1, 2026).',font=f(22),fill=COLORS['ink'])
    d.text((70,1527),'Nota: barras proporcionais ao índice real agregado de investimento liquidado; base 2023=100.',font=f(19),fill=COLORS['muted'])
    fp=OUT/f"q{r['q']}_swot_subregional_qa_v2.webp";im.save(fp,'WEBP',quality=95,method=6)
    im.save(OUT/f"q{r['q']}_swot_subregional_qa_v2.png",'PNG')
    return {"q":r['q'],"file":str(fp),"size":fp.stat().st_size,"width":W,"height":H,"reduction":r['reduction'],"index2025":round(100-r['reduction'],2),"count":r['count']}

if __name__=='__main__':
    out=[render(r) for r in REGIONS]
    (OUT/'rmrp_swot_render_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(out,ensure_ascii=False,indent=2))
