"""Transcribe with OpenAI whisper-1 (word timestamps). usage: wx.py in.(mp4|mp3) out.json [lang]"""
import os,sys,json,subprocess,tempfile,requests
src,out=sys.argv[1],sys.argv[2]; lang=sys.argv[3] if len(sys.argv)>3 else None
tmp=tempfile.mktemp(suffix='.mp3')
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vn','-ac','1','-ar','16000','-b:a','48k',tmp],check=True)
data={'model':'whisper-1','response_format':'verbose_json','timestamp_granularities[]':['word','segment']}
if lang: data['language']=lang
r=requests.post('https://api.openai.com/v1/audio/transcriptions',headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY']},data=data,files={'file':open(tmp,'rb')},timeout=300)
r.raise_for_status(); j=r.json(); json.dump(j,open(out,'w'),ensure_ascii=False,indent=1)
for s in j.get('segments',[]): print(f"{s['start']:6.2f}-{s['end']:6.2f} {s['text']}")
