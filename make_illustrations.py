from pathlib import Path
from PIL import Image
from xml.sax.saxutils import escape
import math, json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'/'illustrations';OUT.mkdir(parents=True,exist_ok=True)
C={'bg':'#10222b','grid':'#2d4350','stroke':'#627c88','light':'#ebf8f4','muted':'#a8c0c9','mint':'#9ceac2','cyan':'#61c7d3','gold':'#ffcb81','red':'#ff8f82','soft':'#172d35'}
def tag(t,**a):
 return '<'+t+' '+' '.join(f'{k.replace("_","-")}="{escape(str(v))}"' for k,v in a.items())+'/>'
def text(x,y,s,size=22,color=None,anchor=None,weight='500',rotate=None):
 attrs=f'x="{x}" y="{y}" fill="{color or C["light"]}" font-size="{size}" font-weight="{weight}"'
 if anchor:attrs+=f' text-anchor="{anchor}"'
 if rotate:attrs+=f' transform="rotate({rotate} {x} {y})"'
 return f'<text {attrs}>{escape(str(s))}</text>'
def line(x1,y1,x2,y2,color=None,width=4,dash=None,arrow=False):
 return tag('line',x1=x1,y1=y1,x2=x2,y2=y2,stroke=color or C['mint'],stroke_width=width,stroke_dasharray=dash or '',marker_end='url(#arrow)' if arrow else '')
def path(d,stroke=None,width=4,fill='none',dash=None,arrow=False):
 return tag('path',d=d,stroke=stroke or C['mint'],stroke_width=width,fill=fill,stroke_linejoin='round',stroke_linecap='round',stroke_dasharray=dash or '',marker_end='url(#arrow)' if arrow else '')
def circ(cx,cy,r,fill=None,stroke=None,width=3):return tag('circle',cx=cx,cy=cy,r=r,fill=fill or C['soft'],stroke=stroke or C['stroke'],stroke_width=width)
def rect(x,y,w,h,fill=None,stroke=None,rx=14,sw=2):return tag('rect',x=x,y=y,width=w,height=h,rx=rx,fill=fill or C['soft'],stroke=stroke or C['grid'],stroke_width=sw)
def ellipse(cx,cy,rx,ry,fill=None,stroke=None,width=3):return tag('ellipse',cx=cx,cy=cy,rx=rx,ry=ry,fill=fill or C['soft'],stroke=stroke or C['stroke'],stroke_width=width)
def poly(points,fill=None,stroke=None,width=3):return tag('polygon',points=' '.join(f'{x},{y}' for x,y in points),fill=fill or 'none',stroke=stroke or C['stroke'],stroke_width=width)
def blob(filename,title,subtitle,body,foot='',height=480):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-label="{escape(title)}">
 <defs><pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 30 0 L 0 0 0 30" fill="none" stroke="{C['grid']}" stroke-width=".75" opacity=".42"/></pattern><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="{C['mint']}" /></marker></defs>
 <rect width="960" height="{height}" rx="27" fill="{C['bg']}"/><rect width="960" height="{height}" rx="27" fill="url(#grid)"/>
 {text(40,50,title,27,C['light'],weight='750')}{text(40,80,subtitle,16,C['muted'])}
 {body}<text x="40" y="{height-22}" font-size="14" fill="{C['muted']}">{escape(foot)}</text></svg>'''
 (OUT/(filename+'.svg')).write_text(svg,encoding='utf8')

# Study strategy
b=''
for i,(name,sub) in enumerate([('01', 'ДАНО'),('02','МОДЕЛЬ'),('03','ФОРМУЛА'),('04','ОТВЕТ')]):
 x=42+i*232;b+=rect(x,165,195,138,C['soft'],C['grid'])+text(x+24,200,name,18,C['cyan'])+text(x+98,253,sub,23,C['light'],'middle','750')
 if i<3:b+=line(x+197,234,x+229,234,C['mint'],3,arrow=True)
b+=rect(245,338,470,74,'#1b3b35','#426b60')+text(480,381,'ПРОВЕРЬ ЕДИНИЦЫ И ЗНАК',23,C['mint'],'middle','700')
blob('strategy','Стратегия решения','Применяй один и тот же алгоритм к каждой задаче.',b,'Сначала модель и формула, потом числа.')

# units
b=circ(286,274,146,'#172c34','#4e7180',3)+line(99,274,480,274,C['stroke'],2)+line(286,441,286,101,C['stroke'],2)+path('M286 274 L390 171',C['mint'],6,arrow=True)+path('M340 274 A54 54 0 0 0 324 236',C['gold'],4)+text(353,252,'45°',21,C['gold'])+text(406,165,'(cos θ, sin θ)',18,C['mint'])+text(466,270,'x',18,C['muted'])+text(295,126,'y',18,C['muted'])
for i,(name,num) in enumerate([('90°','π / 2'),('180°','π'),('360°','2π')]):
 y=155+i*85;b+=rect(572,y,330,66)+text(610,y+43,name,24,C['light'])+text(842,y+43,num,25,C['mint'],'end')
blob('units','Углы и радианы','Длина дуги s = R · θ при θ в радианах.',b,'1 оборот = 360° = 2π рад; для векторов используй компоненты.')

# gears
b=''
def gear(cx,cy,r,teeth,fill,stroke):
 pts=[]
 for i in range(teeth*4):
  a=2*math.pi*i/(teeth*4); rr=r+(9 if i%4 in (1,2) else 0)
  pts.append((round(cx+rr*math.cos(a),2),round(cy+rr*math.sin(a),2)))
 return poly(pts,fill,stroke,3)+circ(cx,cy,r*.18,C['bg'],stroke,2)
b+=gear(179,252,56,8,'#2d5555',C['cyan'])+gear(405,252,161,24,'#375043',C['mint'])
b+=text(179,344,'z₁ = 8',25,C['cyan'],'middle')+text(405,434,'z₂ = 24',25,C['mint'],'middle')
b+=rect(615,153,290,210,'#1a3137','#44636a')+text(643,200,'ОБОРОТЫ',20,C['muted'])+text(643,260,'n₂ = n₁ · 8/24',29,C['mint'],weight='750')+text(643,316,'В 3 раза медленнее',19,C['light'])
blob('gears','Две сцепленные шестерни','Больше зубьев → меньше оборотов ведомого вала.',b,'На общей оси частоты равны. В паре зацепления — отношение зубьев.')

# wheels
b=''
for x,label in [(48,'Танковый поворот'),(495,'Один мотор стоит')]:
 b+=rect(x,116,416,307,'#142932','#344a54')+text(x+208,155,label,22,C['light'],'middle','700')
 c=x+208
 b+=rect(c-82,209,164,143,'#245045','#73b8a7',18)+rect(c-108,232,23,98,'#314452','#72c8d3',5)+rect(c+85,232,23,98,'#314452','#72c8d3',5)+circ(c,282,10,'#0b191e',C['mint'])
 b+=text(c-99,376,'L',19,C['cyan'],'middle')+text(c+99,376,'R',19,C['cyan'],'middle')
 if x<100:
  b+=path(f'M{c-138} 219 Q{c-163} 282 {c-138} 347',C['gold'],4,arrow=True)+path(f'M{c+137} 344 Q{c+161} 281 {c+137} 220',C['gold'],4,arrow=True)
 else:
  b+=circ(c-97,281,6,C['gold'],C['gold'])+text(c-80,199,'ось поворота',15,C['gold'])+path(f'M{c+137} 346 Q{c+193} 267 {c+138} 209',C['mint'],4,arrow=True)
b+=text(480,450,'Танковый: α колеса = θ·B/D    ·    Стоит колесо: α = 2θ·B/D',20,C['mint'],'middle')
blob('wheels','Дифференциальный привод','Почему формула зависит от центра поворота.',b,'B — колея, D — диаметр колеса, θ — поворот корпуса.',500)

# motion
b=rect(64,132,832,294,'#132832','#314652')
# axes
b+=line(125,290,863,290,C['muted'],2,arrow=True)+line(125,410,125,159,C['muted'],2,arrow=True)
pts=[(125,290),(255,198),(368,198),(508,363),(637,363),(752,225),(850,225)]
b+=poly([pts[0],pts[1],pts[2],(368,290)],'#214b42','none',0)+poly([(368,290),(508,363),(637,363),(637,290)],'#493536','none',0)
b+=path('M'+' L'.join(f'{x} {y}' for x,y in pts),C['mint'],5)
b+=text(871,285,'t',18,C['muted'])+text(102,170,'v',18,C['muted'])+text(250,188,'v > 0',18,C['mint'])+text(521,387,'v < 0',18,C['red'])+text(525,170,'Путь: ∫|v|dt',23,C['light'])
blob('motion','Путь по графику скорости','Положительная и отрицательная скорость дают положительный путь.',b,'Путь — суммы модулей площадей, перемещение — площади со знаками.')

# forces
b=poly([(160,381),(570,381),(570,166)],'#203d42','#466a75',3)+line(160,381,570,166,C['cyan'],6)
# box rotated at hill center
b+=f'<g transform="translate(390,260) rotate(-28)">{rect(-53,-50,106,82,"#31584d",C["mint"],9,3)}</g>'
# vectors center (390,260)
b+=line(390,260,390,413,C['gold'],4,arrow=True)+line(390,260,535,179,C['mint'],4,arrow=True)+line(390,260,340,169,C['cyan'],4,arrow=True)
b+=text(408,411,'mg',22,C['gold'])+text(526,168,'тяга F',20,C['mint'])+text(287,160,'N',23,C['cyan'])+text(585,283,'mg · sin α вдоль склона',20,C['light'])+text(585,320,'μmg · cos α — трение',20,C['light'])
blob('forces','Силы на наклонной плоскости','Разложи силу тяжести относительно наклонной поверхности.',b,'Для подъёма с постоянной скоростью F = mg·sinα + μmg·cosα.')

# torque
b=line(110,254,846,254,C['light'],14)+poly([(477,264),(439,331),(515,331)],'#4d6472','#a5c5cc',3)+line(260,254,260,367,C['gold'],5,arrow=True)+line(715,254,715,369,C['cyan'],5,arrow=True)+line(260,208,475,208,C['gold'],2)+line(475,208,715,208,C['cyan'],2)+text(368,195,'L₁',21,C['gold'],'middle')+text(596,195,'L₂',21,C['cyan'],'middle')+text(254,396,'m₁g',21,C['gold'])+text(711,396,'m₂g',21,C['cyan'])+text(476,369,'опора',18,C['muted'],'middle')+text(480,133,'m₁g · L₁ = m₂g · L₂',27,C['mint'],'middle','700')
blob('torque','Рычаг и моменты','Сравнивай не массы, а силы с плечами от точки опоры.',b,'Сила на длинном плече создаёт больший момент.')

# electric
b=text(85,220,'+9 В',23,C['gold'])+line(160,213,238,213,C['gold'],4)+rect(238,188,125,50,'#264d47',C['mint'],7,3)+text(300,219,'R₁',22,C['light'],'middle')+line(363,213,495,213,C['mint'],4)+circ(495,213,8,C['mint'],C['mint'])+line(495,213,594,213,C['mint'],4)+rect(594,188,125,50,'#264d47',C['mint'],7,3)+text(656,219,'R₂',22,C['light'],'middle')+line(719,213,786,213,C['mint'],4)+line(786,213,786,265,C['mint'],4)+line(764,265,809,265,C['muted'],3)+line(770,274,802,274,C['muted'],3)+line(778,282,795,282,C['muted'],3)+line(495,221,495,335,C['cyan'],4)+circ(495,335,9,C['cyan'],C['cyan'])+text(498,366,'ПИН / Vout',20,C['cyan'],'middle')+text(478,160,'Uout = U · R₂/(R₁ + R₂)',24,C['light'],'middle','700')+text(478,430,'Чем больше нижний R₂, тем выше напряжение на пине.',18,C['muted'],'middle')
blob('electric','Делитель напряжения','Упрощённая электрическая схема без нагрузки на выходе.',b,'Важный шаг: проверь, между какими узлами измеряется Vout.')

# code
b=''
for x,y,w,h,name in [(347,117,265,55,'СТАРТ'),(347,209,265,68,'ПРОВЕРИТЬ УСЛОВИЕ'),(347,314,265,62,'ИЗМЕНИТЬ ПЕРЕМЕННЫЕ')]:
 b+=rect(x,y,w,h,'#23433e','#579b85')+text(x+w/2,y+h/2+8,name,20,C['light'],'middle','650')
b+=line(480,172,480,207,C['mint'],4,arrow=True)+line(480,277,480,312,C['mint'],4,arrow=True)+path('M480 377 L480 405 L695 405 L695 243 L615 243',C['gold'],4,arrow=True)+text(617,390,'повтор',17,C['gold'])+path('M348 243 L204 243 L204 370',C['cyan'],4,arrow=True)+text(223,225,'нет',18,C['cyan'])+text(484,291,'да',17,C['mint'])+text(207,390,'КОНЕЦ',20,C['cyan'],'middle')
blob('code','Алгоритмы и циклы','Обновляй все переменные именно в том порядке, что задан.',b,'Проверяй, входит ли изменение переменной внутрь цикла.')

# geometry
b=''
for cx,rad,mark in [(222,74,'r'),(493,148,'2r')]:
 b+=circ(cx,275,rad,'#235348','#8ddfbb',4)+line(cx,275,cx+rad,275,C['gold'],4)+text(cx+rad*.55,263,mark,23,C['gold'],'middle')
b+=rect(700,152,193,217,'#193a3a','#44736d')+text(796,202,'ДЛИНА',19,C['muted'],'middle')+text(796,243,'× 2',29,C['mint'],'middle','800')+text(796,293,'ПЛОЩАДЬ',18,C['muted'],'middle')+text(796,337,'× 4',29,C['gold'],'middle','800')
blob('geometry','Масштаб и площадь','Если радиус вырос вдвое, площадь выросла в 4 раза.',b,'Масса объёмного тела при одинаковой плотности растёт как r³.')

# vision
b=line(450,134,450,411,C['cyan'],4)+circ(450,280,8,C['gold'],C['gold'])+line(175,157,175,387,C['mint'],7)+line(761,195,761,365,C['red'],7)+path('M175 157 L450 280 L761 365',C['mint'],2,dash='9 8')+path('M175 387 L450 280 L761 195',C['mint'],2,dash='9 8')+text(174,140,'Объект H',22,C['mint'],'middle')+text(451,123,'Камера',20,C['cyan'],'middle')+text(761,183,'Изображение h',20,C['red'],'middle')+text(306,439,'Z — расстояние до объекта',18,C['muted'],'middle')+text(611,439,'f — фокусный параметр',18,C['muted'],'middle')+text(480,104,'h = f·H/Z',25,C['gold'],'middle','750')
blob('vision','Проекция камеры','Модель тонкой камеры: изображение уменьшается с расстоянием.',b,'Размер в пикселях пропорционален размеру объекта и 1/Z.')

# nav
b=rect(62,125,830,313,'#172b34','#354b58')+line(140,372,796,372,C['stroke'],2,arrow=True)+line(140,372,140,163,C['stroke'],2,arrow=True)+text(808,379,'Восток (x)',19,C['muted'])+text(155,161,'Север (y)',19,C['muted'])+line(172,348,495,348,C['mint'],5,arrow=True)+path('M495 348 L690 151',C['cyan'],5,arrow=True)+text(350,340,'4 км на восток',18,C['mint'],'middle')+text(638,223,'5 км, СВ',18,C['cyan'])+path('M172 348 L690 151',C['gold'],3,dash='10 8')+text(380,213,'Перемещение',19,C['gold'])+text(385,424,'Сначала складывай x и y, затем применяй Пифагора.',17,C['muted'],'middle')
blob('nav','Маршрут дрона и векторы','Сумма длины маршрута не равна расстоянию от старта.',b,'Северо-восток: по x и y добавляется 5/√2.')

# control
b=''
for x,name in [(53,'ЗАДАНИЕ'),(296,'РЕГУЛЯТОР'),(543,'МОТОР И РОБОТ')]:
 b+=rect(x,185,205,106,'#1c3d38','#5a9582')+text(x+102,240,name,18,C['light'],'middle','750')
b+=line(258,240,294,240,C['mint'],4,arrow=True)+line(501,240,541,240,C['mint'],4,arrow=True)+line(748,240,889,240,C['mint'],4,arrow=True)+text(843,217,'y(t)',18,C['cyan'])+path('M805 241 L805 360 L154 360 L154 290',C['gold'],4,arrow=True)+rect(582,327,180,60,'#354134','#727d56')+text(672,366,'ДАТЧИК',20,C['gold'],'middle','700')+text(385,150,'e(t) = задание − измерение',22,C['muted'],'middle')
blob('control','Замкнутая система управления','Регулятор исправляет ошибку по измерениям датчика.',b,'PID: пропорциональная, интегральная и дифференциальная составляющие.')

# stats
values=[8,9,9,10,13,13,15];b=rect(65,120,825,308,'#182d36','#3c515d')+line(115,345,843,345,C['stroke'],2,arrow=True)
for j,x in enumerate(values):
 px=135+(x-7)*70;b+=circ(px,340-(j%2)*46,11,C['cyan'] if 8.55<=x<=13.45 else C['red'],C['light'],1)
for v in range(8,16):b+=text(135+(v-7)*70,375,v,15,C['muted'],'middle')
x1=135+(8.55-7)*70;x2=135+(13.45-7)*70;b+=rect(x1,192,x2-x1,100,'#214c3e','#397865',8,2)+line(135+(11-7)*70,145,135+(11-7)*70,345,C['gold'],3,dash='6 6')+text(480,157,'Среднее x̄ = 11',21,C['gold'],'middle')+text(480,216,'В пределах ±σ',19,C['mint'],'middle')+text(480,258,'σ ≈ 2,45',21,C['mint'],'middle')
blob('stats','Среднее и стандартное отклонение','Выборка: 8, 9, 9, 10, 13, 13, 15.',b,'Отклонения считают от среднего исходного набора; n=7.')

# manip
b=line(210,376,815,376,C['stroke'],3)+circ(271,350,35,'#274742','#5d9789',4)+line(271,350,465,228,C['mint'],15)+circ(465,228,19,'#163236',C['cyan'],5)+line(465,228,677,177,C['cyan'],13)+circ(677,177,13,C['gold'],C['gold'],2)+line(677,177,700,200,C['gold'],5)+text(344,259,'L₁',23,C['mint'])+text(572,186,'L₂',23,C['cyan'])+path('M331 350 A64 64 0 0 0 316 316',C['gold'],3)+text(338,332,'θ₁',20,C['gold'])+path('M508 210 A48 48 0 0 1 504 254',C['gold'],3)+text(533,267,'θ₂',20,C['gold'])+text(728,156,'(x, y)',22,C['gold'])+text(625,339,'x = L₁cosθ₁ + L₂cos(θ₁+θ₂)',20,C['light'],'middle')
blob('manip','Двухзвенный манипулятор','Конец руки зависит от суммы углов звеньев.',b,'Вычисление положения рабочего органа — прямая кинематика.')

# sensors
b=rect(58,270,844,134,'#cfd6d9','#8d9ca6',11,3)+rect(406,270,156,134,'#17202a','#35404c',0,0)
for x,name,col in [(298,'Белая зона',C['cyan']),(646,'Чёрная линия',C['gold'])]:
 b+=rect(x-42,145,84,46,'#244846','#6fafa0')+ellipse(x,215,18,14,'#75d4cc','#aed9d3',3)+line(x,225,x,275,col,3,dash='8 7')+text(x,130,name,20,C['light'],'middle')
b+=text(480,452,'Разница отражённого ИК-света → ошибка положения → коррекция скорости колёс',19,C['mint'],'middle')
blob('sensors','Датчики линии','Пара отражательных датчиков помогает удерживать чёрную линию.',b,'Порог устанавливай по калибровке на реальном покрытии.',500)

# Arduino
b=rect(44,160,220,180,'#1c4555','#4caec3')+text(154,231,'Arduino',26,C['light'],'middle','800')+text(154,268,'UNO',25,C['mint'],'middle','750')
for x,y,name,col in [(362,160,'ДРАЙВЕР',C['mint']),(680,160,'МОТОРЫ',C['gold']),(362,328,'ДАТЧИКИ',C['cyan']),(680,328,'LED / СЕРВО',C['mint'])]:
 b+=rect(x,y,235,80,'#1e383b','#52726a')+text(x+118,y+49,name,20,col,'middle','750')
b+=line(266,196,360,196,C['mint'],4,arrow=True)+line(597,196,678,196,C['mint'],4,arrow=True)+path('M362 368 L297 368 L297 275 L265 275',C['cyan'],4,arrow=True)+path('M264 296 L625 296 L625 368 L679 368',C['mint'],3,arrow=True)
blob('arduino','Блоки электроники робота','Это функциональная схема, не схема подключения конкретных пинов.',b,'Моторы управляются через драйвер; объединяй GND компонентов.')

# practical
b=''
for i,(n,name) in enumerate([('1','СТАРТ'),('2','ОБЪЕЗД 0–9'),('3','ОСМОТР'),('4','ФИНИШ')]):
 x=44+i*234;b+=rect(x,150,197,110,'#20423a','#447d6b')+text(x+97,185,n,18,C['cyan'],'middle')+text(x+97,226,name,19,C['light'],'middle','700')
 if i<3:b+=line(x+199,204,x+231,204,C['mint'],3,arrow=True)
b+=rect(145,309,670,91,'#2b3830','#5b7554')+text(480,342,'1 кубик → вытолкнуть    ·    2–3 кубика → не трогать',20,C['gold'],'middle')+text(480,373,'LED 1 / 2 / 3 = чётность сумм исходных номеров зон',18,C['mint'],'middle')
blob('practice','Робот-инспектор склада','Схема логики выполнения, не геометрия оригинального полигона.',b,'Для практики обязательны остановки ≥1 секунды на каждой зоне.')

# exam
b=''
items=[('КОЛЁСА','s = πD · n'),('ШЕСТЕРНИ','z₁/z₂'),('РЫЧАГ','ΣM = 0'),('ГРАФИК','площадь / наклон'),('КАМЕРА','h = fH/Z'),('ЦЕПЬ','U = IR')]
for i,(t,formula) in enumerate(items):
 x=50+(i%3)*298;y=148+(i//3)*134
 b+=rect(x,y,267,100,'#1b3a38','#476c65')+text(x+17,y+40,t,19,C['light'],weight='730')+text(x+17,y+78,formula,21,C['mint'])
blob('exam','Как выбрать формулу по условию','Определи тип задачи прежде, чем начинать вычисления.',b,'Строить рисунок полезно даже к заданию, где нужно вписать одно число.')

print('Generated SVG illustrations:',len(list(OUT.glob('*.svg'))))

# Source task figure extractions, source PDF exact locations (relative to page dimensions).
try:
 import fitz
 pdf_paths={
 'M': ROOT/'sources'/'tasks-robo-10-11-teor-mun-msk-25-26.pdf',
 'S': ROOT/'sources'/'tasks-robo-10-11-teor-sch-msk-26-27.pdf',
 'R': ROOT/'sources'/'tasks-robo-10-11-teor-25-26.pdf',
 'P': ROOT/'sources'/'tasks-robo-10-11-prak-25-26.pdf'}
 # bbox in 0..1 x/y of original PDF pages; crop the original artwork + labels, not the entire page.
 clips={
 'M01':(1,.41,.36,.66,.54),
 'M06':(2,.35,.62,.73,.80),
 'M08':(3,.12,.36,.90,.47),
 'M09':(3,.13,.69,.90,.90),
 'M10':(4,.07,.14,.93,.40),
 'M12':(5,.11,.11,.88,.39),
 'M13':(5,.26,.55,.78,.76),
 'M14a':(6,.09,.07,.77,.40),
 'M14b':(6,.09,.49,.78,.87),
 'S01':(1,.11,.15,.95,.37),
 'S02':(1,.29,.56,.79,.77),
 'S03':(2,.35,.395,.76,.525),
 'S05':(3,.34,.29,.75,.50),
 'S07':(4,.10,.40,.94,.87),
 'R02':(3,.13,.06,.60,.4),
 'R11':(7,.18,.19,.62,.53),
 'P_MAP':(7,.16,.055,.87,.385),
 }
 crop_dir=ROOT/'assets'/'figures';crop_dir.mkdir(parents=True,exist_ok=True)
 for key,(page,x0,y0,x1,y1) in clips.items():
  doc=fitz.open(pdf_paths[key[0]])
  pg=doc[page-1];r=pg.rect;clip=fitz.Rect(r.x0+x0*r.width,r.y0+y0*r.height,r.x0+x1*r.width,r.y0+y1*r.height)
  pix=pg.get_pixmap(matrix=fitz.Matrix(2.0,2.0),clip=clip,alpha=False)
  im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  im.save(crop_dir/(key+'.webp'),format='WEBP',quality=89,method=5)
  doc.close()
 print('PDF crops:',len(list(crop_dir.glob('*.webp'))))
except Exception as exc:print('PDF crop generation failed',exc)

lesson_map={
 'strategy':[('strategy','Пять шагов к правильному ответу',1)],
 'units':[('units','Единичная окружность и связь градусов с радианами',2)],
 'gears':[('gears','Передаточное отношение зависит от зубьев',1)],
 'wheels':[('wheels','Два типа поворота: вокруг центра и вокруг колеса',2)],
 'motion':[('motion','Путь по графику v(t): учитывай площадь по модулю',2)],
 'forces':[('forces','Силы на наклонной плоскости',1)],
 'torque':[('torque','Плечи сил относительно опоры',1)],
 'electric':[('electric','Делитель напряжения: как найти потенциал пина',1)],
 'code':[('code','Цикл и условие в блок-схеме',1)],
 'geometry':[('geometry','Зависимость площади от масштаба',1)],
 'vision':[('vision','Проекция: размер объекта, расстояние и пиксели',1)],
 'nav':[('nav','Разложение движения дрона на компоненты',1)],
 'control':[('control','Обратная связь в замкнутом контуре',2)],
 'stats':[('stats','Среднее и стандартное отклонение на реальной выборке',2)],
 'manip':[('manip','Положение конца двухзвенного манипулятора',1)],
 'sensors':[('sensors','Два датчика отражения и чёрная линия',1)],
 'arduino':[('arduino','Функциональные блоки электроники робота',2)],
 'practice':[('practice','Схема действий в практическом задании',1)],
 'exam':[('exam','Шесть основных типов олимпиадных задач',1)],
}
source_map={
 'R01':('units',None),'R02':('geometry','R02'),'R03':('forces',None),'R04':('torque',None),'R05':('code',None),'R06':('geometry',None),'R07':('control',None),'R08':('control',None),'R09':('nav',None),'R10':('nav',None),'R11':('vision','R11'),'R12':('manip',None),'R13':('forces',None),
 'M01':('code','M01'),'M02':('wheels',None),'M03':('wheels',None),'M04':('code',None),'M05':('gears',None),'M06':('geometry','M06'),'M07':('wheels',None),'M08':('electric','M08'),'M09':('motion','M09'),'M10':('motion','M10'),'M11':('nav',None),'M12':('electric','M12'),'M13':('torque','M13'),'M14a':('manip','M14a'),'M14b':('manip','M14b'),
 'S01':('gears','S01'),'S02':('wheels','S02'),'S03':('torque','S03'),'S04':('nav',None),'S05':('torque','S05'),'S06':('vision',None),'S07':('motion','S07'),'S08a':('stats',None),'S08b':('stats',None)
}
config={'lessons':{lid:[{'file':'assets/illustrations/'+stem+'.svg','caption':caption,'after':num} for stem,caption,num in rows] for lid,rows in lesson_map.items()},'sources':{sid:{'file':'assets/'+('figures/'+crop+'.webp' if crop else 'illustrations/'+stem+'.svg'),'original':bool(crop),'caption':'Фрагмент оригинального условия из PDF' if crop else 'Объясняющая схема по теме (не изображение из условия)'} for sid,(stem,crop) in source_map.items()},'practice':{'file':'assets/figures/P_MAP.webp','caption':'Оригинальный полигон из практического задания (PDF, стр. 7)'}}
(ROOT/'illustrations.js').write_text('window.ROBO_ILLUSTRATIONS = '+json.dumps(config,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
print('Configuration: lessons',len(config['lessons']),'sources',len(config['sources']))
