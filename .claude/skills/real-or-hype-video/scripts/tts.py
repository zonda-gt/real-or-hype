import sys,asyncio,certifi
certifi.where=lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
async def main(voice,rate,pitch,text,out):
    await edge_tts.Communicate(text,voice,rate=rate,pitch=pitch).save(out)
asyncio.run(main(*sys.argv[1:6]))
