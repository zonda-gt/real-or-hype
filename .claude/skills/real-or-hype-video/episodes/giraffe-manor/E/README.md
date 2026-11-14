# Giraffe Manor, version E: clips-first, reference style (@wynnejael study)

New series style, not Real or Hype?. Built in this order:
1. **Shot inventory first**, then the script written to it: every sentence names something we can show (`script.txt`, 125 words).
2. **One continuous narration take**: ElevenLabs library voice **John "Passionate Founder"** (Korean accent, `PXo7njgt8slUVdtKa3La`), multilingual v2, stability 0.3, style 0.55. Picked from 3 takes by Whisper (take 2: word-perfect incl. "Huzhou" and "yuan"). Pauses >0.2 s squeezed, atempo 1.2, then gaps >0.35 s cut to 0.30 s, giving 199 wpm (her reels run at 200–250).
3. **Picture cut to the voice**: `words.json` (faster-whisper medium word stamps). Each cue in `e_plan.py` is a word index; the cut lands 0.10 s before that word. Shots fill their slot in order and slow down only if needed (60 fps sources ≥0.72×, 30 fps ≥0.9×; one shot at 0.87×).
4. **Her graphics**: a 2×2 collage under the hook with the title "CHINA'S / Giraffe Hotel" in DM Serif Display on pale-yellow highlight boxes, plus a handwritten "breakfast included" tag (Chewy). Handwritten object labels (Giraffe Manor, capybara, raccoons, red-crowned cranes, 6:30 AM). Serif info cards for the price and Kenya. One-word captions (Poppins SemiBold 54, centred, uppercase), hidden under the title and cards.
5. Mix: marimba bed (ElevenLabs Music) ducked under the voice, whoosh out of the collage, soft pops on labels and cards. -15 LUFS, TP -1.7.

Voice shortlist (creator's picks): Andy Lin (Chinese), John (Korean), Chris (Chinese), in `voice_shortlist.txt`.
