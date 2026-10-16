# 更新角色圖鑑與頭像：python tools/update_characters.py
# 資料來源：Project Amber (gi.yatta.moe) 繁中角色 API；新角色上線後重跑即可
import json, os, sys, urllib.request, concurrent.futures as cf
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
req = urllib.request.Request('https://gi.yatta.moe/api/v2/cht/avatar', headers={'User-Agent':'theatar-planner'})
os.makedirs(os.path.join(root,'data'),exist_ok=True)
open(os.path.join(root,'data/yatta-cht.json'),'wb').write(urllib.request.urlopen(req,timeout=30).read())
d = json.load(open(os.path.join(root,'data/yatta-cht.json'),encoding='utf-8'))['data']['items']
E = {'Fire':'pyro','Water':'hydro','Electric':'electro','Ice':'cryo','Wind':'anemo','Rock':'geo','Grass':'dendro'}
out = []
for k,v in d.items():
    if v.get('element') not in E: print('skip',v['id']); continue
    if isinstance(v['id'],str):  # traveler variants: keep boy only
        if 'PlayerGirl' in v['icon']: continue
        name = '旅行者(%s)' % {'pyro':'火','hydro':'水','electro':'雷','cryo':'冰','anemo':'風','geo':'岩','dendro':'草'}[E[v['element']]]
    else: name = v['name']
    out.append({'id':v['id'],'name':name,'el':E[v['element']],'r':v['rank'] if v['rank']<=5 else 5,'icon':v['icon'],'rel':v.get('release',0)})
out.sort(key=lambda c:(c['el'],-c['r'],c['rel']))
os.makedirs(os.path.join(root,'assets/avatars'),exist_ok=True)
def dl(icon):
    p = os.path.join(root,'assets/avatars',icon+'.png')
    if os.path.exists(p): return
    req = urllib.request.Request('https://gi.yatta.moe/assets/UI/%s.png'%icon, headers={'User-Agent':'theatar-planner'})
    open(p,'wb').write(urllib.request.urlopen(req,timeout=30).read())
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(dl,{c['icon'] for c in out}))
with open(os.path.join(root,'data/characters.js'),'w',encoding='utf-8') as f:
    f.write('// 由 yatta.moe (Project Amber) API 產生：gi.yatta.moe/api/v2/cht/avatar\n')
    f.write('window.CHAR_DATA=' + json.dumps(out,ensure_ascii=False) + ';\n')
print(len(out), len(os.listdir(os.path.join(root,'assets/avatars'))))
