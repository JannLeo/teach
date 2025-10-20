import subprocess
from pathlib import Path
import os
import re
import tempfile
from pathlib import Path
from PIL import Image
import math
import wave
import textwrap
from gtts import gTTS

# —— Windows 事件循环修正（edge_tts + websockets 更稳定）——
import os, asyncio
if os.name == "nt":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

def parse_args():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True, type=Path, help="对应 _prepare.md 路径")
    return ap.parse_args()

import argparse
ap = parse_args()

# 获取md文件的路径
md_file = ap.md.resolve()
print(f"[DEBUG] 输入文件：{md_file}")

# 获取图片目录
image_dir = md_file.with_suffix('').parent / f"{md_file.stem.replace('_prepare', '')}_assets"
print(f"[DEBUG] 图片目录：{image_dir}")
# === 动态输出目录 ===
OUTPUT_ROOT = r'D:\other\teacher\teach_video'
md_path      = Path(md_file).resolve()
course_name  = md_path.parent.name
stem_clean   = md_path.stem.replace('_prepare', '')
output_video_dir = Path(OUTPUT_ROOT) / course_name / stem_clean
output_video_dir.mkdir(parents=True, exist_ok=True)
print(f"[DEBUG] 视频将输出到：{output_video_dir}")
os.makedirs(output_video_dir, exist_ok=True)


def clean_markdown(text: str) -> str:
    # 1. 去掉图片链接 ![...](...)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 2. 去掉普通链接 [...](...)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 3. 去掉代码块 ```...```
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 4. 去掉行内代码 `...`
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # 5. 去掉 **加粗** 和 *斜体* 的星号
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **加粗**
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # *斜体*
    # 6. 去掉 # 标题标记
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # 7. 去掉列表符号 - * +
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    # 8. 合并多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def adjust_image_size(image_path):
    """调整图片尺寸为偶数"""
    with Image.open(image_path) as img:
        width, height = img.size
        # 如果宽度或高度是奇数，则将其加1，确保是偶数
        new_width = width + 1 if width % 2 != 0 else width
        new_height = height + 1 if height % 2 != 0 else height

        # 调整尺寸，使用 LANCZOS 高质量滤镜
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img.save(image_path)  # 保存调整后的图片

    print(f"Image {image_path} resized to {new_width}x{new_height}.")

def parse_markdown(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pages = []
    matches = re.split(r'##\s*第\s*(\d+)\s*页', content)
    print(f"[DEBUG] 共匹配到 {len(matches)//2} 页")

    for i in range(1, len(matches), 2):
        page_no = matches[i].strip()  # 页码
        page_content = matches[i + 1]
        print(f"\n[DEBUG] 正在解析第 {page_no} 页")

        # 1. 图片：根据页码生成图片文件名
        img_filename = f"page-{int(page_no):03d}.png"  # 根据页码生成类似 "page-001.png"
        img_path = os.path.join(image_dir, img_filename).replace("\\", "/")  # 获取图片完整路径

        print(f"[DEBUG] 第 {page_no} 页 ✅ 图片：{img_filename}")

        if os.path.exists(img_path):
            adjust_image_size(img_path)  # 调整图像尺寸
        else:
            print(f"[DEBUG] 第 {page_no} 页 ❌ 图片不存在：{img_path}")
            continue

        # 2. 正文：图片后直到下一页标题之前的所有内容
        text_match = re.search(
            r'!\[.*?\]\(.*?\)\s*\n+(.*?)(?=\n##\s*第\s*\d+\s*页|\Z)',  # 提取正文内容
            page_content,
            re.DOTALL
        )
        if not text_match:
            print(f"[DEBUG] 第 {page_no} 页 ❌ 取不到正文")
            continue
        text = text_match.group(1).strip()

        if len(text) < 10:
            print(f"[DEBUG] 第 {page_no} 页 ❌ 正文过短（<10）")
            continue
        print(f"[DEBUG] 第 {page_no} 页 ✅ 正文长度：{len(text)}")

        # 添加解析结果：页码、图片路径、正文
        pages.append({'page_no': page_no, 'image': img_filename, 'text': text})

    print(f"[DEBUG] 最终解析成功 {len(pages)} 页")
    return pages

# === 直接生成音频（无需 make_chattts.py） ===


def split_sentences(text, max_len=22):
    text = re.sub(r'\s+', ' ', text.strip())
    # 先按句号/问号/感叹号切
    parts = [s.strip() for s in re.split(r'(?<=[。！？.!?])', text) if s.strip()]
    out = []
    for p in parts:
        while len(p) > max_len:
            # 按中文逗号/顿号优先切，否则硬切
            m = re.search(r'[，、,]\s*', p[:max_len][::-1])
            cut = max_len if not m else max_len - m.start()
            out.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            out.append(p)
    return out

def _tts_edge(sentence: str, mp3_out: Path) -> None:
    """用 edge_tts 生成 MP3；失败抛异常"""
    import asyncio, edge_tts, random, time, re
    s = re.sub(r'\s+', ' ', sentence).strip().replace('"', '“').replace("'", "‘")
    if not s:
        s = "无内容"
    voices_try = [
        ("zh-CN-XiaoxiaoNeural", "-10%"),
        ("zh-CN-XiaoxiaoNeural", None),
        ("zh-CN-XiaoyiNeural",   None),
    ]
    last_err = None
    for voice, rate in voices_try:
        for attempt in range(4):
            try:
                async def _amain():
                    kwargs = dict(text=s, voice=voice)
                    if rate:
                        kwargs["rate"] = rate
                    comm = edge_tts.Communicate(**kwargs)
                    await comm.save(str(mp3_out))
                asyncio.run(_amain())
                return
            except Exception as e:
                last_err = e
                # 指数退避
                time.sleep((1.2 * (2 ** attempt)) + random.uniform(0, 0.5))
    raise RuntimeError(f"edge_tts 生成失败：{last_err}")

def _tts_gtts(sentence: str, mp3_out: Path) -> None:
    """用 gTTS 生成 MP3；失败抛异常（需要能访问 Google）"""
    try:
        from gtts import gTTS
    except ImportError:
        raise RuntimeError("未安装 gTTS（pip install gTTS）")
    s = re.sub(r'\s+', ' ', sentence).strip()
    if not s:
        s = "无内容"
    tts = gTTS(text=s, lang='zh-cn', slow=False)
    tts.save(str(mp3_out))

def _tts_pyttsx3(sentence: str, wav_out: Path) -> None:
    """用 pyttsx3 离线 TTS 直接输出 WAV；失败抛异常"""
    try:
        import pyttsx3
    except ImportError:
        raise RuntimeError("未安装 pyttsx3（pip install pyttsx3 pypiwin32）")
    engine = pyttsx3.init()
    # 选个中文可用的语音；不同机器可遍历 voices 再挑选
    for v in engine.getProperty('voices'):
        if 'zh' in (v.id.lower() + ' ' + (getattr(v, 'name', '') or '').lower()):
            engine.setProperty('voice', v.id); break
    engine.setProperty('rate', 180)    # 语速可调
    engine.setProperty('volume', 1.0)
    engine.save_to_file(sentence, str(wav_out))
    engine.runAndWait()

def _mp3_to_wav(mp3_path: Path, wav_path: Path, sr=24000):
    subprocess.run([
        "ffmpeg","-y","-hide_banner","-loglevel","error",
        "-i", str(mp3_path), "-ar", str(sr), "-ac","1","-acodec","pcm_s16le", str(wav_path)
    ], check=True)

def tts_one(sentence) -> Path:
    """
    统一入口：优先 edge_tts → gTTS → pyttsx3
    返回一个临时 WAV 路径
    """
    import tempfile
    # —— 新增：空句直接返回静音，避免把空串交给 gTTS/edge_tts ——
    s_clean = re.sub(r'\s+', ' ', (sentence or '')).strip()
    if not s_clean:
        return make_silence_wav(0.3)  # 0.3s 静音占位
    tmp_mp3 = Path(tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name)
    tmp_wav = tmp_mp3.with_suffix('.wav')

    # 1) edge_tts
    try:
        _tts_edge(sentence, tmp_mp3)
        _mp3_to_wav(tmp_mp3, tmp_wav, sr=24000)
        tmp_mp3.unlink(missing_ok=True)
        return tmp_wav
    except Exception as e1:
        print(f"[fallback] edge_tts 失败：{e1}")

    # 2) gTTS
    try:
        _tts_gtts(sentence, tmp_mp3)
        _mp3_to_wav(tmp_mp3, tmp_wav, sr=24000)
        tmp_mp3.unlink(missing_ok=True)
        return tmp_wav
    except Exception as e2:
        print(f"[fallback] gTTS 失败：{e2}")

    # 3) pyttsx3（直接生成 WAV）
    try:
        _tts_pyttsx3(sentence, tmp_wav)
        # 等 pyttsx3 写完文件；通常 runAndWait 已同步，这里做个存在性检查
        if not tmp_wav.exists() or tmp_wav.stat().st_size == 0:
            raise RuntimeError("pyttsx3 未生成有效 wav")
        return tmp_wav
    except Exception as e3:
        print(f"[fallback] pyttsx3 失败：{e3}")
        # 都失败就抛
        raise RuntimeError(f"所有 TTS 引擎均失败（edge_tts / gTTS / pyttsx3）")





def wav_duration(path: Path) -> float:
    import wave
    with wave.open(str(path), 'rb') as f:
        return f.getnframes() / f.getframerate()


def generate_audio_tmp(text) -> Path:
    """
    整段文本的回退版 TTS（当逐句都失败时调用）；
    这里直接用 gTTS→pyttsx3 两级兜底（也可以调用 tts_one 逐句拼）。
    """
    s = clean_markdown(text).replace('\n', '。').replace('"', '“').replace("'", "‘").strip()
    if not s:
        s = "本页内容请结合图片自行阅读。"
    # 这里直接用 tts_one 生成单句音频即可（简单稳妥）
    return tts_one(s)



def generate_ass_by_segments(segments, output_file, frame_w, frame_h):
    # segments: [{'text':..., 'start':t0, 'end':t1}, ...]
    import textwrap
    header = textwrap.dedent(f"""\
    [Script Info]
    ScriptType: v4.00+
    PlayResX: {frame_w}
    PlayResY: {frame_h}
    ScaledBorderAndShadow: yes

    [V4+ Styles]
    Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
    Style: Cur,Microsoft YaHei,36,&H00FFFF00,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,60,60,50,1
    Style: Prev,Microsoft YaHei,30,&H55FFFF00,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,60,60,120,1

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """)

    def ts(x):
        h=int(x//3600); m=int((x%3600)//60); s=x%60
        return f"{h:01}:{m:02}:{s:05.2f}"

    lines=[]
    for i, seg in enumerate(segments):
        def esc(text: str) -> str:
            # 基本转义：反斜杠、花括号，顺带把多空白压成空格
            t = re.sub(r'\s+', ' ', text).strip()
            t = t.replace('\\', r'\\').replace('{', '（').replace('}', '）')
            # 可选：把很长的句子手动断行，避免过宽（示例每 ~28 字加一次换行）
            if len(t) > 28:
                chunks = [t[i:i+28] for i in range(0, len(t), 28)]
                t = r'\N'.join(chunks)
            return t

        cur_txt  = esc(seg['text'])
        lines.append(f"Dialogue: 0,{ts(seg['start'])},{ts(seg['end'])},Cur,,0,0,0,,{cur_txt}")
        if i > 0:
            prev_txt = esc(segments[i-1]['text'])
            lines.append(f"Dialogue: 1,{ts(seg['start'])},{ts(seg['end'])},Prev,,0,0,0,,{prev_txt}")


    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")





def merge_videos(pages: list, output_dir: Path, stem_clean: str) -> Path:
    """把所有 page_XX.mp4 合并成单个文件"""
    # 按页号排序
    pages.sort(key=lambda p: int(p['page_no']))
    # 创建临时列表文件
    list_file = output_dir / 'concat_list.txt'
    with list_file.open('w', encoding='utf-8') as f:
        for p in pages:
            mp4 = output_dir / f"page_{p['page_no']}.mp4"
            f.write(f"file '{mp4.resolve()}'\n")

    full_video = output_dir / f"{stem_clean}_full.mp4"
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0', '-i', str(list_file),
        '-c', 'copy', '-y', str(full_video)
    ]
    subprocess.run(cmd, check=True)
    list_file.unlink(missing_ok=True)   # 删除列表文件
    # ✅ 新增：删除单页中间文件
    for p in pages:
        p['mp4'].unlink(missing_ok=True)
    print(f"🧹 已清理 {len(pages)} 个单页 MP4")
    return full_video

# === 合成视频（不变） ===
def create_video(image_file, audio_file, output_file, subtitle_file):
    from pathlib import Path
    image = Path(image_file).resolve().as_posix()
    audio = str(audio_file)
    outp  = str(output_file)

    sub_path = Path(subtitle_file).resolve().as_posix()
    sub_path_escaped = sub_path.replace(':', r'\:').replace("'", r"\'")

    # 仅保证偶数尺寸，然后烧 ASS（ASS 里已经有样式与两行逻辑）
    vf = f"scale=ceil(iw/2)*2:ceil(ih/2)*2,subtitles='{sub_path_escaped}'"

    cmd = [
        "ffmpeg","-hide_banner","-loglevel","error",
        "-loop","1","-framerate","1","-i", image,
        "-i", audio,
        "-filter:v", vf,
        "-c:v","libx264","-tune","stillimage","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","128k",
        "-shortest","-y", outp
    ]
    print("[DEBUG] ffmpeg 命令：", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("❌ ffmpeg 失败：", r.stderr)
        raise RuntimeError("ffmpeg 合成视频失败")
    print(f"✅ 视频已生成：{outp}")


def make_silence_wav(duration_sec: float) -> Path:
    """生成给定时长的单声道16bit PCM静音wav"""
    import tempfile, subprocess
    out = Path(tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name)
    subprocess.run([
        "ffmpeg","-y","-hide_banner","-loglevel","error",
        "-f","lavfi","-i",f"anullsrc=channel_layout=mono:sample_rate=24000",
        "-t",f"{max(duration_sec, 0.2):.3f}",  # 至少0.2秒
        "-ar","24000","-ac","1","-acodec","pcm_s16le", str(out)
    ], check=True)
    return out




def get_audio_duration(wav_file):
    """获取音频时长（秒）"""
    wav_path = str(Path(wav_file))    # ✅ 转字符串
    with wave.open(wav_path, 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def generate_videos(pages):
    pages_out  = []
    stem_clean = Path(md_file).stem.replace('_prepare', '')

    for p in pages:
        page_no    = p['page_no']
        image_file = Path(image_dir) / p['image']

        # 1) 逐句切分文本
        sentences = split_sentences(p['text'], max_len=28)
        # 强过滤：去掉空/全标点的句子
        sentences = [re.sub(r'\s+', ' ', s).strip() for s in sentences]
        sentences = [s for s in sentences if s and re.sub(r'[^\w\u4e00-\u9fa5]+', '', s)]
        if not sentences:
            sentences = ["本页内容请结合图片自行阅读。"]

        # === 2. 每句 TTS + 记录时长 ===
        wav_parts = []
        segments  = []
        t = 0.0
        for s in sentences:
            try:
                w = tts_one(s)
            except Exception as e:
                print(f"[WARN] 某句 TTS 全部失败，改用静音：{e}")
                w = make_silence_wav(0.4)

            d = wav_duration(w)
            # 多留 0.25 秒让字幕更好读；纯静音时可稍短
            pad = 0.25 if d > 0.25 else 0.15
            segments.append({'text': s, 'start': t, 'end': t + d + pad})
            wav_parts.append(w)
            t += d

        if not wav_parts:
            # 回退：整段一次性 TTS，至少保证页面能出片
            try:
                fallback_wav = generate_audio_tmp(p['text'])
                d = wav_duration(fallback_wav)
                # 用整段文本作为一条字幕（也可以 split_sentences 再粗分几条）
                segments = [{'text': p['text'], 'start': 0.0, 'end': d}]
                wav_parts = [fallback_wav]
                t = d
                print(f"[INFO] 第 {page_no} 页使用整段 TTS 回退")
            except Exception as e:
                print(f"[ERROR] 第 {page_no} 页 TTS 全部失败：{e}")
                continue



        # 3) 拼接所有句子的 wav 成该页总音频
        concat_list = output_video_dir / f"page_{page_no}_wavlist.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for w in wav_parts:
                # 用 POSIX 路径，避免反斜杠转义问题
                f.write(f"file '{w.resolve().as_posix()}'\n")

        page_wav = output_video_dir / f"page_{page_no}.wav"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", "-y", str(page_wav)
        ], check=True)

        # 4) 生成带精准时间轴的 ASS（两行：当前句+上一句）
        with Image.open(image_file) as im:
            fw, fh = im.size
        ass_file = output_video_dir / f"page_{page_no}.ass"
        generate_ass_by_segments(segments, ass_file, fw, fh)

        # 5) 合成该页视频
        mp4_file = output_video_dir / f"page_{page_no}.mp4"
        create_video(str(image_file), str(page_wav), str(mp4_file), str(ass_file))

        # 6) 清理临时文件
        for w in wav_parts:
            w.unlink(missing_ok=True)
        concat_list.unlink(missing_ok=True)
        page_wav.unlink(missing_ok=True)
        ass_file.unlink(missing_ok=True)

        pages_out.append({'page_no': page_no, 'mp4': mp4_file})

    # 7) 合并所有页的视频
    full = merge_videos(pages_out, output_video_dir, stem_clean)
    print(f'🎉 完整视频已生成：{full}')



if __name__ == '__main__':

    # 输出目录
    OUTPUT_ROOT = r'D:\other\teacher\teach_video'

    # 获取课程名和输出文件夹
    course_name = md_file.parent.name
    stem_clean = md_file.stem.replace('_prepare', '')
    output_video_dir = Path(OUTPUT_ROOT) / course_name / stem_clean

    # 创建输出目录
    output_video_dir.mkdir(parents=True, exist_ok=True)
    print(f"[DEBUG] 视频将输出到：{output_video_dir}")
    
    os.makedirs(output_video_dir, exist_ok=True)

    # 解析Markdown文件
    pages = parse_markdown(md_file)
    generate_videos(pages)  # 生成视频







