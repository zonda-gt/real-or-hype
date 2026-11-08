#!/bin/bash
# footage-only renders + every-frame OCR of clean and final renders
cd "$(dirname "$0")/.."
for v in A B C; do python3 -I bin/render.py specs/${v}3.py out/${v}_v4_clean.mp4 --clean > proof/${v}_clean_render.log 2>&1; done
for v in A B C; do
  python3 -I bin/qa_ocr.py out/${v}_v4_clean.mp4 proof/${v}_clean_ocr.json 1080 > proof/${v}_clean_ocr.txt 2>&1
  python3 -I bin/qa_ocr.py out/${v}_v4.mp4 proof/${v}_final_ocr.json 1080 > proof/${v}_final_ocr.txt 2>&1
done
echo PROOF_DONE
