# make_chattts.py
import sys
from pathlib import Path
import soundfile as sf
import ChatTTS

def main():
    if len(sys.argv) < 3:
        print("usage: make_chattts.py <text_file> <out_wav>")
        sys.exit(1)

    text_path = Path(sys.argv[1])
    out_path  = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    txt = text_path.read_text(encoding="utf-8")

    chat = ChatTTS.Chat()
    chat.load_models(source="huggingface", force_redownload=False)
    wav = chat.infer([txt], skip_refine_text=True)[0]  # numpy 1D, 24kHz

    sf.write(str(out_path), wav, 24000)  # 写出 WAV
    print(str(out_path))

if __name__ == "__main__":
    main()
