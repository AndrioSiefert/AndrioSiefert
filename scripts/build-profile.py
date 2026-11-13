"""Build the profile's self-contained SVG components (Python standard library only)."""
from pathlib import Path
from html import escape
import copy
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
COLORS = dict(text='#F5EAF1', muted='#C0AEBD', rose='#EBAAC7', lilac='#C5A0DB', peach='#EAC4A8', mint='#9BC6BD', surface='#1B1721', line='#49394E')
ICONS = {}
for filename in ['languages', 'frontend', 'ai', 'data', 'infra', 'integrations']:
    pending = None
    for node in ET.parse(ASSETS / f'stack-{filename}.svg').getroot():
        if node.tag.endswith('}g'):
            pending = node
        elif node.tag.endswith('}text') and pending is not None:
            ICONS[node.text] = copy.deepcopy(pending)
            pending = None


def text(x, y, label, size=20, color='text', weight=400, anchor='start'):
    color = COLORS.get(color, color)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>'


def icon(label, x, y, size=32, color='rose'):
    node = copy.deepcopy(ICONS[label])
    color = COLORS.get(color, color)
    node.set('transform', f'translate({x} {y}) scale({size / 24})')
    if node.get('fill') == 'none':
        node.set('stroke', color)
    else:
        node.set('fill', color)
    return ET.tostring(node, encoding='unicode')


def path(d, color='line', width=1, extra=''):
    return f'<path d="{d}" fill="none" stroke="{COLORS.get(color, color)}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def panel(x, y, w, h, accent='rose', fill=None):
    return (f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="16" fill="{fill or COLORS["surface"]}" stroke="{COLORS["line"]}"/>'
            + path(f'M{x+24} {y+1}h64', accent, 2))


def rule(x, y, w):
    return path(f'M{x} {y}h{w}')


def logo_label(label, cx, y, color='rose', size=34, font=19):
    return icon(label, cx-size/2, y, size, color) + text(cx, y+size+30, label, font, anchor='middle')


def save(name, w, h, title, content, description=''):
    # Paths and labels stay visible without animation or CSS support.
    # Motion is confined to two small diagrams; reduced-motion keeps a static alternative.
    defs = '''<defs>
      <linearGradient id="feature" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#211A2B"/><stop offset="1" stop-color="#382638"/></linearGradient>
      <linearGradient id="edge"><stop stop-color="#C5A0DB" stop-opacity="0"/><stop offset=".5" stop-color="#EBAAC7"/><stop offset="1" stop-color="#EAC4A8" stop-opacity="0"/></linearGradient>
    </defs>
    <style>
      text{font-family:DejaVu Sans,Arial,sans-serif}
      .packet{stroke-dasharray:5 95;stroke-dashoffset:100;animation:transmit 8s linear infinite}
      .packet.delay{animation-delay:1s}
      .orbital{transform-box:fill-box;transform-origin:center;animation:orbit 32s linear infinite}
      .breathe{animation:breathe 8s ease-in-out infinite}
      @keyframes transmit{to{stroke-dashoffset:-100}}
      @keyframes orbit{to{transform:rotate(360deg)}}
      @keyframes breathe{0%,100%{opacity:.45}50%{opacity:1}}
      @media(prefers-reduced-motion:reduce){.packet,.orbital,.breathe{animation:none!important}.packet{stroke-dasharray:none;opacity:.3}}
    </style>'''
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}</desc>{defs}{content}</svg>\n'
    (ASSETS / f'{name}.svg').write_text(svg)


def core(mobile=False):
    w = 480 if mobile else 960
    h = 1080 if mobile else 572
    left_w = 480 if mobile else 312
    lh = 400 if mobile else 572
    s = panel(0, 0, left_w, lh, 'peach', '#201A23')
    s += text(28, 48, 'Languages', 28, weight=700)
    s += text(28, 84, '& runtime', 28, 'peach', 700)
    s += path(f'M{left_w-69} 42l-10 10 10 10m20-20 10 10-10 10', 'peach', 2)
    s += rule(28, 110, left_w-56)
    for i, label in enumerate(['TypeScript', 'JavaScript', 'Python', 'Node.js']):
        x = 28 + (i % 2)*224 if mobile else 28
        y = 140 + (i//2)*90 if mobile else 142+i*76
        s += icon(label, x, y, 32, 'peach') + text(x+48, y+23, label, 24 if mobile else 21, weight=500)
    s += rule(28, lh-103, left_w-56)
    s += text(28, lh-64, 'Bash · Java', 23 if mobile else 19, 'muted')
    s += text(28, lh-29, 'PHP · pip', 23 if mobile else 19, 'muted')
    for j, (title, color, logos, lines) in enumerate([
        ('Frontend & interfaces', 'lilac', ['React','Vite','Tailwind CSS'], ['Next.js · TanStack Query', 'React Hook Form · Zod · Chart.js']),
        ('Backend & AI', 'rose', ['NestJS','FastAPI','OpenAI API'], ['Express · n8n · TypeORM', 'AI agents · Multimodal AI']),
    ]):
        x, y, pw, ph = (0, 428+j*340, 480, 312) if mobile else (336, j*300, 624, 272)
        s += panel(x,y,pw,ph,color, '#1C1927' if j==0 else '#231A25')
        s += text(x+28,y+48,title,27 if mobile else 26,weight=700)
        for i, label in enumerate(logos):
            cx=x+pw*(i+.5)/3
            s += logo_label(label,cx,y+83,color,36,23 if mobile else 19)
        s += rule(x+28,y+176,pw-56)
        for k, line in enumerate(lines):
            s += text(x+pw/2,y+214+k*33,line,23 if mobile else 18,'muted',anchor='middle')
    save('stack-core'+('-mobile' if mobile else ''),w,h,'Languages, frontend and backend',s,
         'TypeScript, JavaScript, Python, Node.js, Bash, Java, PHP, pip. React, Vite, Tailwind CSS, Next.js, TanStack Query, React Hook Form, Zod, Chart.js. NestJS, FastAPI, OpenAI API, Express, n8n, TypeORM, AI agents, Multimodal AI.')


def systems(mobile=False):
    w,h = (480,864) if mobile else (960,408)
    pw=480 if mobile else 468
    s=''
    for i,(title,color) in enumerate([('Data & messaging','mint'),('Linux & infrastructure','lilac')]):
        x,y=(0,i*444) if mobile else (i*492,0)
        s += panel(x,y,pw,408,color, '#182326' if i==0 else '#1D1927')
        s += text(x+pw/2,y+49,title,27 if mobile else 25,weight=700,anchor='middle')
        if i==0:
            s += icon('PostgreSQL',x+80,y+85,42,color)+text(x+140,y+116,'PostgreSQL',29,weight=600)
            s += rule(x+28,y+151,pw-56)
            for j,label in enumerate(['Redis','BullMQ','RabbitMQ']):
                s += logo_label(label,x+pw*(j+.5)/3,y+182,color,30,23 if mobile else 19)
            s += text(x+pw/2,y+313,'MinIO · Supabase · SQL · JSONB',23 if mobile else 18,'muted',anchor='middle')
            s += text(x+pw/2,y+355,'MySQL · MongoDB',23 if mobile else 18,'muted',anchor='middle')
        else:
            for j,label in enumerate(['Linux','Docker','Git']):
                s += logo_label(label,x+pw*(j+.5)/3,y+98,color,42,22 if mobile else 20)
            s += rule(x+28,y+215,pw-56)
            for j,line in enumerate(['Docker Compose · Docker Swarm','NGINX · Traefik','Terminal · GitHub Actions']):
                s += text(x+pw/2,y+264+j*46,line,23 if mobile else 19,'muted',anchor='middle')
    save('stack-systems'+('-mobile' if mobile else ''),w,h,'Data, messaging and infrastructure',s,
         'PostgreSQL, Redis, BullMQ, RabbitMQ, MinIO, Supabase, SQL, JSONB, MySQL, MongoDB. Linux, Docker, Git, Docker Compose, Docker Swarm, NGINX, Traefik, Terminal, GitHub Actions.')


def network(mobile=False):
    w,h=(480,520) if mobile else (960,288)
    s=panel(0,0,w,h,'peach','#231D24')
    s+=text(28,49,'APIs & integrations',28,weight=700)
    if mobile:
        s+=text(28,94,'REST APIs · Webhooks · SSE',22,'peach')
        s+=text(28,130,'JWT · OAuth 2.0',22,'muted')
        cx,cy=90,330
        nx=234
        ys=[218,310,402]
        nodew=218
    else:
        s+=text(28,103,'REST APIs · Webhooks',23,'peach')
        s+=text(28,143,'SSE · JWT · OAuth 2.0',20,'muted')
        s+=text(28,230,'Connecting systems. Automating work.',18,'muted')
        cx,cy=517,145
        nx=668
        ys=[41,121,201]
        nodew=264
    for i,y in enumerate(ys):
        route=f'M{cx+35} {cy}H{nx-46}V{y+24}H{nx}'
        s+=path(route,'#775E70',1.5)
        s+=path(route,'peach',2.5,f'class="packet {"delay" if i%2 else ""}" pathLength="100"')
    s+=f'<circle cx="{cx}" cy="{cy}" r="37" fill="#302631" stroke="#A48191"/>'
    s+=path(f'M{cx-13} {cy-9}l-9 9 9 9m26-18 9 9-9 9m-10-22-6 26','peach',2)
    for label,y in zip(['WhatsApp API','Google Calendar','Asaas'],ys):
        s+=f'<rect x="{nx}" y="{y}" width="{nodew}" height="48" rx="8" fill="#302631" stroke="#685261"/>'
        s+=text(nx+nodew/2,y+31,label,23 if mobile else 20,anchor='middle')
    if mobile:s+=text(w/2,484,'Connecting systems. Automating work.',19,'muted',anchor='middle')
    save('stack-network'+('-mobile' if mobile else ''),w,h,'APIs and integrations',s,
         'REST APIs, Webhooks, SSE, JWT and OAuth 2.0. Integrations with WhatsApp API, Google Calendar and Asaas. Animated signals follow the connection paths.')


def engineering(mobile=False):
    w,h=(480,606) if mobile else (960,274)
    s=''
    stages=[('Architecture','Clean · Hexagonal','Multi-tenant','lilac'),('Data integrity','Transactions · Concurrency','Queues · Idempotency','mint'),('Validation','Unit · Integration tests','Contracts · Race conditions','rose')]
    if mobile:
        s+=path('M51 50V484','#725772',1.5)
    else:
        s+=path('M160 67H800','#725772',1.5)
    for i,(title,line1,line2,color) in enumerate(stages):
        cx,cy=(51,53+i*199) if mobile else (160+i*320,67)
        s+=f'<circle cx="{cx}" cy="{cy}" r="27" fill="#211B29" stroke="{COLORS[color]}"/>'
        if i==0:
            s+=path(f'M{cx} {cy-12}l14 8-14 8-14-8 14-8m-14 17 14 8 14-8',color,1.7)
        elif i==1:
            s+=path(f'M{cx-13} {cy}h26m-8-8 8 8-8 8m-8-16-8 8 8 8',color,1.7)
        else:
            s+=path(f'M{cx-12} {cy}l8 8 17-18',color,2)
        if mobile:
            s+=text(103,cy+8,title,28,weight=700)
            s+=text(103,cy+53,line1,21,'muted')
            s+=text(103,cy+86,line2,21,'muted')
        else:
            s+=text(cx,139,title,26,weight=700,anchor='middle')
            s+=text(cx,181,line1,18,'muted',anchor='middle')
            s+=text(cx,214,line2,18,'muted',anchor='middle')
    # A fixed dark surface keeps SVG text readable in both GitHub themes.
    s=f'<rect width="{w}" height="{h}" rx="16" fill="#18151F"/>'+s
    save('engineering-flow'+('-mobile' if mobile else ''),w,h,'Architecture, data integrity and validation',s,
         'Clean, Hexagonal and multi-tenant architecture. Transactions, concurrency control, queues and idempotency. Automated unit, integration, contract and race-condition tests.')


def feature(mobile=False):
    w,h=(480,490) if mobile else (960,304)
    s=panel(0,0,w,h,'rose','url(#feature)')
    # The same wireframe geometry as the profile identity, composed as an orbital portal.
    cx,cy=(240,365) if mobile else (772,150)
    r=91 if mobile else 105
    s+=f'<circle cx="{cx}" cy="{cy}" r="{r+16}" fill="none" stroke="#644B69"/>'
    s+=f'<g class="orbital" stroke="#B38EC4" fill="none" stroke-width="1.1" opacity=".65">'
    s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*.35}" transform="rotate(-32 {cx} {cy})"/>'
    s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*.35}" transform="rotate(52 {cx} {cy})"/>'
    s+=path(f'M{cx} {cy-r} {cx+r*.64} {cy} {cx} {cy+r} {cx-r*.64} {cy}Z M{cx} {cy-r}V{cy+r}M{cx-r*.64} {cy}H{cx+r*.64}','lilac',1.1)
    s+='</g>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="5" fill="#EBAAC7" class="breathe"/>'
    tx=240 if mobile else 40
    anchor='middle' if mobile else 'start'
    s+=text(tx,76 if mobile else 95,'brechó.dev',52 if mobile else 65,'text',700,anchor)
    s+=text(tx,117 if mobile else 145,'My corner of the internet.',23,'rose',anchor=anchor)
    s+=text(tx,155 if mobile else 181,'Storefront, portfolio & experiments.',20,'muted',anchor=anchor)
    bx,by=(94,191) if mobile else (40,220)
    s+=f'<rect x="{bx}" y="{by}" width="292" height="48" rx="8" fill="#EBAAC7"/>'
    s+=text(bx+22,by+31,'Explore BrechoDev',20,'#241A26',600)
    s+=path(f'M{bx+255} {by+31}l14-14m-14 0h14v14','#241A26',2)
    save('brechodev-feature'+('-mobile' if mobile else ''),w,h,'Explore BrechoDev — my storefront and portfolio',s)


def signoff(mobile=False):
    w,h=(480,140) if mobile else (960,130)
    s=f'<path d="M20 10H{w-20}" stroke="url(#edge)"/>'
    # This signature is decorative; its readable copy is native HTML in the README.
    s+=f'<path d="m{w/2} 0 10 10-10 10-10-10Z" fill="#211B29" stroke="#C5A0DB"/>'
    save('profile-divider'+('-mobile' if mobile else ''),w,30,'Section divider',s)


for mobile in [False,True]:
    core(mobile)
    systems(mobile)
    network(mobile)
    engineering(mobile)
    feature(mobile)
    signoff(mobile)
print('Built 12 responsive SVG assets.')
