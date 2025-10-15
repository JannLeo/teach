import json, sys, re, os

output_dir = sys.argv[1]
md_file  = output_dir + '_prepare.md'
asset_dir = output_dir + '_assets'

if not os.path.isfile(md_file):
    with open(output_dir + '_split.json', 'w', encoding='utf-8') as f:
        json.dump([], f)
    sys.exit(0)

with open(md_file, encoding='utf-8') as f:
    md = f.read()

chunks = re.split(r'##\s*第\s*(\d+)\s*页\s*[\n:]', md, flags=re.I)
result = []

for i in range(1, len(chunks), 2):
    page_no = int(chunks[i])
    txt_block = chunks[i + 1] if i + 1 < len(chunks) else ''
    txt = re.sub(r'!\[.*?\]\([^)]+\)', '', txt_block)
    txt = re.sub(r'^\*\*提问：\*\*.*$', '', txt, flags=re.M)
    txt = re.sub(r'当然可以[。，]|下面我会逐句解释[。，]|我会对这张.*?截图的内容[逐句详细]*解释[。，]', '', txt)
    txt = re.sub(r'\*\*(.*?)\*\*', r'\1', txt)
    txt = re.sub(r'^\s*[-*]\s+', '第，', txt, flags=re.M)
    txt = re.sub(r'\n+', ' ', txt).strip()

    m = re.search(r'!\[.*?\]\((page-\d{3}\.png)\)', txt_block)
    rel_img = m.group(1) if m else f'page-{page_no:03d}.png'
    abs_img = os.path.join(asset_dir, rel_img)

    if txt:
        result.append({'txt': txt, 'img': abs_img, 'idx': page_no})

# ✅ 写文件，而不是 print
with open(output_dir + '_split.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)

# 给 n8n 一个 dummy item，只传 outputDir 继续用
print(json.dumps([{"outputDir": output_dir}]))