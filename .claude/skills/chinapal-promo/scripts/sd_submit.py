import base64,json,requests,sys
img,text,out=sys.argv[1],sys.argv[2],sys.argv[3]; res=sys.argv[4] if len(sys.argv)>4 else '480p'; dur=int(sys.argv[5]) if len(sys.argv)>5 else 5
u='data:image/jpeg;base64,'+base64.b64encode(open(img,'rb').read()).decode()
body={"model":"doubao-seedance-2-0-mini-260615","content":[{"type":"text","text":text},{"type":"image_url","image_url":{"url":u},"role":"first_frame"}],
 "ratio":"9:16","resolution":res,"duration":dur,"generate_audio":True,"watermark":False}
r=requests.post('https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks',headers={'Authorization':'Bearer proxy-injected'},json=body,timeout=60)
print(r.status_code,r.text[:600]); open(out,'w').write(r.text)
