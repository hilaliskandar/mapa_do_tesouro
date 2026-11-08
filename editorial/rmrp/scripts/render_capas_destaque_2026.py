import csv, json, os, math, pathlib
from PIL import Image, ImageDraw, ImageFont
OUT=pathlib.Path('/mnt/data/rmrp_capas_20261108')
OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/lato/'
C={'navy':'#102943','dark':'#0B2136','white':'#FFFFFF','sub':'#9DB2C7','teal':'#23B7C5','blue':'#386D98','orange':'#DA995A','green':'#27896A','soft':'#EDF3F8','grey':'#DDE7F0','ink':'#183551','yellow':'#E5B96A'}
F=lambda size,bold=False:ImageFont.truetype(FONT+('Lato-Bold.ttf' if bold else 'Lato-Regular.ttf'),size)
def put(draw,x,y,text,size=24,color=None,bold=False):
    draw.text((x,y),str(text),font=F(size,bold),fill=color or C['ink'])
def box(draw,x1,y1,x2,y2,fill,r=16):draw.rounded_rectangle((x1,y1,x2,y2),radius=r,fill=fill)
def ellipsis(draw,text,sz,maxw):
    while draw.textbbox((0,0),text,font=F(sz,True))[2]>maxw: text=text[:-2]
    return text+'…' if len(text)<4 else text

def base(title,subtitle,kind):
    image=Image.new('RGB',(1200,630),C['soft']);d=ImageDraw.Draw(image)
    d.rectangle((0,0,1200,151),fill=C['navy']);d.rectangle((44,31,53,120),fill=C['teal']);
    size=57 if len(title)<22 else 46 if len(title)<28 else 39
    put(d,78,30,title,size,'white',True)
    put(d,80,104,subtitle,24,C['sub'])
    put(d,52,595,'FINANÇAS MUNICIPAIS DA RMRP  |  VOLUME II · G30 RC1  |  2025',17,'#5C748B',True)
    put(d,1025,595,kind,17,C['blue'],True)
    return image,d

def pct(x):return f'{x:.2f}'.replace('.',',')+'%'
entries=[]
with open('/mnt/data/rmrp_coverage_data.csv',encoding='utf-8') as f:
 for row in csv.DictReader(f,delimiter=';'):
    x={k:(float(v.replace(',','.')) if k in ('iss','icms','fpm') else v) for k,v in row.items()}
    entries.append(x)
assert len(entries)==33
for x in entries:
  im,d=base(x['nome'],'Composição selecionada da receita corrente  •  exercício de 2025','MUNICÍPIO')
  box(d,43,175,1157,560,C['white'])
  put(d,71,191,'Participação na receita corrente',35,C['ink'],True)
  put(d,71,242,'Indicadores contábeis anuais da DCA/FINBRA',22,'#647F98')
  for idx,(key,name,col) in enumerate([('iss','ISS principal',C['teal']),('icms','Cota-parte ICMS',C['blue']),('fpm','FPM · cota mensal ordinária',C['orange'])]):
     v=x[key];y=304+idx*78
     put(d,72,y-3,name,23,C['ink'],True)
     d.rounded_rectangle((480,y,1045,y+27),radius=12,fill='#E0E8EF')
     d.rounded_rectangle((480,y,480+565*v/55,y+27),radius=12,fill=col)
     put(d,1059,y-6,pct(v),25,C['ink'],True)
  put(d,72,538,'Rubricas selecionadas; não representam a totalidade das receitas.',17,'#75889A')
  fn=f'capa-municipio-{x["slug"]}-g30rc1.webp';p=OUT/fn;im.save(p,'WEBP',quality=91,method=6)
  x.update({'filename':fn,'path':str(p),'type':'municipal'})
sub=[('jaboticabal','Jaboticabal',6,55.29,19.24,20.31),('mococa','Mococa',6,24.31,17.27,24.06),('batatais','Batatais',7,56.50,16.33,20.17)]
for slug,name,n,fall,tax,fpm in sub:
 im,d=base('Sub-região de '+name,f'{n} municípios  •  investimentos e composição fiscal','SUB-REGIÃO')
 box(d,42,176,1158,559,C['white'])
 put(d,68,196,'Investimentos liquidados reais',34,C['ink'],True)
 put(d,68,245,'Índice dos valores agregados (2023 = 100)',22,'#617B91')
 for i,(ano,val,col) in enumerate([('2023',100,C['navy']),('2025',100-fall,C['teal'])]):
  y=304+i*67
  put(d,72,y-7,ano,25,C['ink'],True)
  d.rounded_rectangle((195,y,803,y+30),radius=14,fill='#E1EBF1')
  d.rounded_rectangle((195,y,195+608*val/100,y+30),radius=14,fill=col)
  put(d,821,y-5,f'{val:.2f}'.replace('.',','),25,C['ink'],True)
 box(d,69,456,623,536,'#E6F0F4')
 put(d,93,471,'Queda real 2023–2025:',20,C['ink'])
 put(d,384,465,'−'+pct(fall),32,'#A44F4D',True)
 box(d,643,453,1127,537,'#E8F0F9')
 put(d,667,464,'Tributação:',21,C['ink']);put(d,985,461,pct(tax),24,C['blue'],True)
 put(d,667,502,'FPM ordinário:',21,C['ink']);put(d,985,498,pct(fpm),24,C['blue'],True)
 fn=f'capa-subregiao-{slug}-g30rc1.webp';p=OUT/fn;im.save(p,'WEBP',quality=91,method=6)
 entries.append({'slug':slug,'nome':name,'filename':fn,'path':str(p),'type':'subregional','n':n,'fall':fall,'tax':tax,'fpm':fpm})
with open(OUT/'manifesto.json','w',encoding='utf-8') as f:json.dump(entries,f,ensure_ascii=False,indent=2)
print('created',len(entries),'outputs',OUT)
print('sizes',min(os.path.getsize(e['path']) for e in entries),max(os.path.getsize(e['path']) for e in entries))
