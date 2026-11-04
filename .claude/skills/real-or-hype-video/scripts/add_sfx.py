# usage: add_sfx.py <workdir> <in.mp4> <starts.txt> <out.mp4>  — whoosh into section cuts, pop on panel, ding on price, clicks on ticks
import sys,os,subprocess,ast
os.chdir(sys.argv[1]); inp_v,stf,out=sys.argv[2:5]; st=ast.literal_eval(open(stf).read()); W=0.305
ev=[('whoosh',st['O1']-W,0.5,None),('whoosh',st['A1']-W,0.5,None),('whoosh',st['R1']-W,0.5,None),
    ('pop',st['O5']+0.03,0.5,None),('ding',st['I4']+0.08,0.4,(0,0.45)),
    ('click',st['V1']+1.1-0.06,0.7,(1.02,1.16)),('buzz',st['V1']+2.0,0.35,None)]
inp=['-i',inp_v]; fc=''
for i,(n,t,v,tr) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.wav']; ms=int(t*1000)
    trim=f'atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS,afade=t=out:st={tr[1]-tr[0]-0.08:.2f}:d=0.08,' if tr else ''
    fc+=f'[{i+1}:a]{trim}aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}];'
fc+='[0:a]'+''.join(f'[s{i}]' for i in range(len(ev)))+f'amix=inputs={len(ev)+1}:normalize=0:duration=first,alimiter=limit=0.95[a]'
subprocess.run(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
print('sfx ok')
