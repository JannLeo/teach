#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Stable Version (with idle-wait):
- 同一会话连续提问
- 每次只上传 1 张图，上传前清理旧预览
- 回答未完成(存在 stop-button)时不进行下一轮
- 生成 Markdown 笔记
"""

from __future__ import annotations
import sys, time, shutil
from dataclasses import dataclass
from pathlib import Path
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pyperclip

# ===================== CONFIG =====================
@dataclass
class Config:
    input_pdf: Path = Path("Week 11 - 2. Scalable Algorithm Templates.pdf")
    out_dir: Path = Path("output")
    site_url: str = "https://dn7vxt.aitianhu2.top/?model=gpt-5"
    login_url: str = "https://dn7vxt.aitianhu2.top/list"
    access_key: str = "sk-fi9uVjhlfirEQMJRE8Da97D764624a948fC2B2657b58636e"
    prompt_text: str = "这张截图里的内容是什么意思？请面向初学者详细解释，分点讲清楚。"
    reuse_session: bool = True
    headless: bool = False
    page_load_timeout: int = 30
    upload_timeout: int = 90
    answer_timeout: int = 120
    post_submit_sleep: float = 1.2
    render_dpi: int = 180
    stable_pause: float = 0.8
    # 等待“生成完成”最大时长（等待 stop→send）
    idle_timeout: int = 180

CFG = Config()

# ===================== SELECTORS =====================
class SELECTORS:
    # 登录
    KEY_INPUT = (By.CSS_SELECTOR, "input#input-code")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button#login-button")
    # 发送区
    FILE_INPUT = (By.CSS_SELECTOR, "input#upload-photos[type='file']")
    PROMPT_AREA = (By.CSS_SELECTOR, "div#prompt-text-area[contenteditable='true']")
    PROMPT_AREA_FALLBACK = (By.CSS_SELECTOR, "div.ProseMirror[contenteditable='true']")
    SEND_BUTTON = (By.CSS_SELECTOR, "button[data-testid='send-button'], button#composer-submit-button[aria-label*='发送']")
    STOP_BUTTON = (By.CSS_SELECTOR, "button[data-testid='stop-button'], button#composer-submit-button[aria-label*='停止'], button[aria-label*='Stop']")
    ASSISTANT_MESSAGE = (By.CSS_SELECTOR, "[data-message-author-role='assistant'], div.assistant, div.markdown")
    # 预览缩略图（DOM 层面）
    TILE_SEL = "span[style*='background-image'],img[src^='blob:'],img[src^='data:']"
    # 回答整块（article）
    ASSISTANT_TURN = (
        By.CSS_SELECTOR,
        'article[data-turn="assistant"], '
        'article[data-message-author-role="assistant"], '
        '[data-message-author-role="assistant"] article'
    )

    # 每条回答里的“复制”按钮（你的页面 aria-label="复制"；也兼容 Copy）
    COPY_BUTTON_IN_TURN = (
        By.CSS_SELECTOR,
        'button[data-testid="copy-turn-action-button"], '
        'button[aria-label*="复制"], button[aria-label*="拷贝"], '
        'button[aria-label*="Copy"]'
    )
    # 按钮变成勾时常会把 aria-label 改成“已复制/Copied”
    COPIED_STATE_MATCHERS = [
        (By.CSS_SELECTOR, "button[aria-label*='已复制']"),
        (By.CSS_SELECTOR, "button[aria-label*='Copied']"),
    ]
    OVERFLOW_BUTTON_IN_TURN = (By.CSS_SELECTOR,
        "button[data-testid='overflow-menu-trigger'], "
        "button[aria-label*='更多'], button[aria-label*='More']")
    # 菜单项：复制为 Markdown
    MENU_COPY_AS_MD = (By.XPATH,
        "//div[@role='menu']//div[contains(., '复制为 Markdown') or contains(., 'Copy as Markdown')]")

# ===================== 工具函数 =====================
def grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top"):
    try:
        drv.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": origin,
            "permissions": ["clipboardReadWrite", "clipboardSanitizedWrite"]
        })
    except Exception:
        pass

def install_clipboard_hook(drv):
    """
    在页面里 hook navigator.clipboard.writeText，把文本镜像到 window.__lastCopiedText。
    多次调用也安全（只安装一次）。
    """
    js = r"""
    if (!window.__tap_copy_hooked__) {
      window.__tap_copy_hooked__ = true;
      (function(){
        try {
          const orig = (navigator.clipboard && navigator.clipboard.writeText)
                       ? navigator.clipboard.writeText.bind(navigator.clipboard) : null;
          window.__lastCopiedText = window.__lastCopiedText || '';
          // 包一层 writeText：把要写入的文本也存到 window.__lastCopiedText
          if (orig) {
            navigator.clipboard.writeText = (t) => {
              window.__lastCopiedText = (t || '');
              try { return orig(t); } catch(e) { return Promise.resolve(); }
            };
          } else {
            // 没有 clipboard 对象就造一个最基本的
            navigator.clipboard = {
              writeText: (t)=>{ window.__lastCopiedText = (t || ''); return Promise.resolve(); },
              readText: ()=>Promise.resolve(window.__lastCopiedText || '')
            };
          }
          // 兜底：有些实现用 document.execCommand('copy')，监听 copy 事件
          document.addEventListener('copy', function(e){
            try {
              const sel = document.getSelection && document.getSelection();
              if (sel && sel.toString()) { window.__lastCopiedText = sel.toString(); }
            } catch(_){}
          }, true);
        } catch(_){}
      })();
    }
    """
    drv.execute_script(js)

def read_captured_markdown(drv, timeout=6.0) -> str:
    """优先从我们挂的 window.__lastCopiedText 取到 Markdown。"""
    end = time.time() + timeout
    last = None
    while time.time() < end:
        try:
            txt = drv.execute_script("return window.__lastCopiedText || '';") or ""
            if txt.strip() and txt != last:
                return txt.strip()
            last = txt
        except Exception:
            pass
        time.sleep(0.2)
    return ""

def click_copy_button_in_last_turn(drv) -> bool:
    turns = drv.find_elements(*SELECTORS.ASSISTANT_TURN)
    if not turns: return False
    turn = turns[-1]
    drv.execute_script("arguments[0].scrollIntoView({block:'center'});", turn)
    time.sleep(0.1)

    btns = turn.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN)
    if not btns:
        btns = drv.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN)
    if not btns:
        return False
    btn = btns[-1]
    try:
        WebDriverWait(drv, 5).until(EC.element_to_be_clickable(btn))
    except Exception:
        pass
    try:
        btn.click()
        return True
    except Exception:
        try:
            drv.execute_script("arguments[0].click();", btn)
            return True
        except Exception:
            return False



def read_clipboard_via_browser(drv, timeout=6.0) -> str:
    """
    用浏览器原生剪贴板读取（navigator.clipboard.readText）。
    需要 https + 用户手势；我们已点击“复制”，所以通常能读到。
    """
    end = time.time() + timeout
    last_text = None
    while time.time() < end:
        try:
            js = """
                const done = arguments[0];
                if (!navigator.clipboard || !navigator.clipboard.readText) { done(null); return; }
                navigator.clipboard.readText().then(t => done(t)).catch(_ => done(null));
            """
            text = drv.execute_async_script(js)
            if text and text.strip():
                if text != last_text:
                    return text.strip()
            last_text = text
        except Exception:
            pass
        time.sleep(0.2)
    return ""

def _last_assistant_article(driver):
    # 找到最后一条 assistant 回复
    arts = driver.find_elements(By.CSS_SELECTOR, 'article[data-turn="assistant"]')
    if not arts:
        raise RuntimeError("没找到任何 assistant 回复的 article。")
    return arts[-1]

def copy_markdown_of_last_answer(driver, timeout=15, fallback_menu=True):
    """
    点击“复制/复制为Markdown”，等待剪贴板变化并返回文本。
    - 优先点主复制按钮 data-testid=copy-turn-action-button
    - 如果被收起，则点“更多”按钮，再点菜单里的“复制为 Markdown”
    """
    root = _last_assistant_article(driver)

    # 记下点击前剪贴板
    try:
        before = pyperclip.paste()
    except Exception:
        before = ""

    # 1) 直接找“复制”按钮（优先）
    copy_btn = None
    try:
        copy_btn = root.find_element(By.CSS_SELECTOR, 'button[data-testid="copy-turn-action-button"]')
    except Exception:
        copy_btn = None

    if copy_btn and copy_btn.is_enabled():
        copy_btn.click()
    else:
        # 2) 走“更多”→“复制为 Markdown” 兜底
        if not fallback_menu:
            raise RuntimeError("找不到复制按钮。")
        # 更多按钮：通常是右侧动作区那个圆角按钮组里（aria-label 可能是“更多”“更多操作”等）
        more_btn = WebDriverWait(root, timeout).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                # 常见选择器（两种都试）：data-testid 或 aria-label
                'button[data-testid="copy-turn-action-button-in-overflow"], '
                'button[aria-label*="更多"], button[aria-label*="更多操作"], '
                'button[data-testid*="turn-action-button"][aria-expanded="false"]'
            ))
        )
        more_btn.click()

        # 弹出菜单里找 “复制为 Markdown”
        md_item = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH,
                # 菜单项文字可能是“复制为 Markdown”“复制为Markdown”“复制 Markdown”等
                "//div[@role='menu' or @role='listbox']//*[self::div or self::button or self::span]"
                "[contains(., '复制为 Markdown') or contains(., '复制为Markdown') or contains(., '复制 Markdown')]"
            ))
        )
        md_item.click()

    # 3) 等剪贴板变更（按钮会短暂显示✅，但等剪贴板更稳）
    t0 = time.time()
    copied = None
    while time.time() - t0 < timeout:
        try:
            txt = pyperclip.paste()
        except Exception:
            txt = None
        if txt and txt != before:
            copied = txt
            break
        time.sleep(0.2)

    if not copied:
        raise RuntimeError("等待剪贴板内容变化超时，可能复制失败。")

    return copied

def get_last_assistant_turn(drv):
    """定位最后一条助手消息（整块 turn 区域，用于在其中找【复制】按钮）"""
    turns = drv.find_elements(*SELECTORS.ASSISTANT_TURN)
    if not turns:
        raise TimeoutException("未找到助手消息 turn。")
    return turns[-1]

def wait_button_feedback_or_clipboard(drv, btn, sentinel: str, timeout: float = 5.0) -> bool:
    """等待两种反馈任一发生：按钮进入“已复制”状态 或 剪贴板不等于哨兵。"""
    end = time.time() + timeout
    while time.time() < end:
        # 1) aria-label/按钮状态变化（✔）
        try:
            for how, what in SELECTORS.COPIED_STATE_MATCHERS:
                if get_last_assistant_turn(drv).find_elements(how, what):
                    return True
        except Exception:
            pass
        # 2) 剪贴板变化
        try:
            text = (pyperclip.paste() or "").strip()
            if text and text != sentinel:
                return True
        except Exception:
            pass
        time.sleep(0.15)
    return False

def copy_markdown_from_last_turn(drv, wait_secs: float = 8.0) -> str:
    """
    点击【复制】或菜单项【复制为 Markdown】，
    以“✔ 反馈”或剪贴板变化作为成功信号，再读取 Markdown。
    """
    # 置哨兵，防止读到旧剪贴板
    SENTINEL = "__WAITING_FOR_MD__"
    try:
        pyperclip.copy(SENTINEL)
    except Exception:
        pass

    turn = get_last_assistant_turn(drv)
    drv.execute_script("arguments[0].scrollIntoView({block:'center'});", turn)
    time.sleep(0.2)

    used_action = False
    # 先点卡片上的“复制”
    btns = turn.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN)
    if btns:
        try:
            btns[0].click()
            used_action = True
            # 等“✔或剪贴板变化”
            if not wait_button_feedback_or_clipboard(drv, btns[0], SENTINEL, timeout=wait_secs):
                # 若无反馈，继续尝试菜单
                used_action = False
        except Exception:
            used_action = False

    # 菜单里的“复制为 Markdown / Copy as Markdown”
    if not used_action:
        # 你若已实现 OVERFLOW_BUTTON_IN_TURN/MENU_COPY_AS_MD，也可以在这里补充菜单逻辑
        pass

    # 最终读剪贴板
    md = ""
    try:
        md = (pyperclip.paste() or "").strip()
        if md == SENTINEL:
            md = ""
    except Exception:
        md = ""
    return md


def ensure_out_dirs(base: Path):
    img_dir, asset_dir = base / "pages", base / "notes_assets"
    base.mkdir(exist_ok=True)
    img_dir.mkdir(exist_ok=True)
    asset_dir.mkdir(exist_ok=True)
    return img_dir, asset_dir

def pdf_to_images(pdf_path: Path, out_dir: Path, dpi: int = 180):
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        out_path = out_dir / f"page-{i:03d}.png"
        pix.save(out_path)
        paths.append(out_path)
    doc.close()
    return paths

def start_browser(headless=False):
    opt = ChromeOptions()
    if headless:
        opt.add_argument("--headless=new")
    opt.add_argument("--disable-gpu"); opt.add_argument("--no-sandbox")
    opt.add_argument("--window-size=1400,900")
    drv = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opt)
    drv.set_page_load_timeout(CFG.page_load_timeout)
    return drv

def wait_for(drv, selector, timeout):
    return WebDriverWait(drv, timeout).until(EC.presence_of_element_located(selector))

def maybe_login(drv):
    try:
        key_input = WebDriverWait(drv, 3).until(EC.presence_of_element_located(SELECTORS.KEY_INPUT))
        key_input.clear(); key_input.send_keys(CFG.access_key)
        try:
            drv.find_element(*SELECTORS.LOGIN_BUTTON).click()
        except NoSuchElementException:
            key_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except TimeoutException:
        pass

def go_to_chat(drv):
    drv.get(CFG.login_url); maybe_login(drv)
    drv.get(CFG.site_url);  maybe_login(drv)
    # 👇 新增：进入站点后安装剪贴板 hook + 申请权限
    grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top")
    install_clipboard_hook(drv)
    time.sleep(0.5)


# —— 预览清理 & 计数 ——
def clear_all_uploads(drv):
    """彻底清理所有上传预览 DOM 和文件输入值（不依赖 UI 的 × 按钮）"""
    drv.execute_script("""
        document.querySelectorAll('span[style*="background-image"], img[src^="blob:"], img[src^="data:"]').forEach(el => el.remove());
        document.querySelectorAll('input#upload-photos').forEach(inp => { try { inp.value = ''; } catch(e){} });
    """)
    time.sleep(0.3)

def count_tiles(drv):
    return drv.execute_script("return document.querySelectorAll(arguments[0]).length;", SELECTORS.TILE_SEL)

def wait_stable_tile_count(drv, expect, timeout=60):
    end = time.time() + timeout
    last = -1; stable_for = 0
    while time.time() < end:
        cnt = count_tiles(drv)
        if cnt == expect:
            if cnt == last:
                stable_for += 0.2
                if stable_for > CFG.stable_pause:
                    return
            else:
                stable_for = 0
            last = cnt
        else:
            stable_for = 0; last = cnt
        time.sleep(0.2)
    raise TimeoutException(f"等待图片数量稳定为 {expect} 超时（当前={cnt}）。")

# —— 生成状态：等待 stop 按钮消失 / send 按钮出现 ——
def is_generating(drv) -> bool:
    return len(drv.find_elements(*SELECTORS.STOP_BUTTON)) > 0

def wait_until_idle(drv, timeout: int = None):
    """
    仅等待：stop 按钮消失 且 发送可用（或输入框可用），绝不点击“停止”。
    """
    if timeout is None:
        timeout = CFG.idle_timeout  # 可在配置里调大/调小

    t0 = time.time()
    last_state = None
    # 更鲁棒的“发送可用”判断：要么出现 send-button，要么 composer 的输入框可编辑
    while time.time() - t0 < timeout:
        has_stop = len(drv.find_elements(*SELECTORS.STOP_BUTTON)) > 0
        has_send = len(drv.find_elements(*SELECTORS.SEND_BUTTON)) > 0
        prompt_ready = len(drv.find_elements(*SELECTORS.PROMPT_AREA)) > 0 or \
                       len(drv.find_elements(*SELECTORS.PROMPT_AREA_FALLBACK)) > 0

        state = f"stop={has_stop}, send={has_send}, prompt={prompt_ready}"
        if state != last_state:
            print(f"[idle] {state}")
            last_state = state

        # 生成中 → 等
        if has_stop:
            time.sleep(0.35)
            continue

        # 不在生成：出现 send 或输入框可编辑，即视为空闲
        if has_send or prompt_ready:
            return

        time.sleep(0.35)

    raise TimeoutException("等待模型生成完成超时（stop 未消失或发送不可用）。")


# —— 上传 / 发送 / 抓取 ——
def upload_image(drv, img_path: Path):
    # 上传前先确认空闲（不点击停止）
    try:
        wait_until_idle(drv)
    except TimeoutException:
        print("[upload] 警告：未能确认空闲，仍尝试上传（可能站点选择器需再对齐）")

    # 彻底清理历史预览，再上传
    clear_all_uploads(drv)
    file_input = wait_for(drv, SELECTORS.FILE_INPUT, CFG.upload_timeout)
    drv.execute_script("arguments[0].style='';", file_input)
    file_input.send_keys(str(img_path.resolve()))
    print(f"[upload] 发送文件：{img_path.name}")
    wait_stable_tile_count(drv, 1, CFG.upload_timeout)
    print("[upload] 预览稳定为 1")



def type_prompt_and_send(drv, text):
    try:
        prompt = wait_for(drv, SELECTORS.PROMPT_AREA, 10)
    except TimeoutException:
        prompt = wait_for(drv, SELECTORS.PROMPT_AREA_FALLBACK, 5)
    prompt.click(); prompt.send_keys(text); prompt.send_keys(Keys.ENTER)
    time.sleep(CFG.post_submit_sleep)
    # 有的站点需要点击按钮
    try:
        btns = drv.find_elements(*SELECTORS.SEND_BUTTON)
        if btns:
            btns[0].click()
    except Exception:
        pass

def wait_for_latest_answer(drv, timeout):
    # 1) 等到至少出现一条助手消息
    wait_for(drv, SELECTORS.ASSISTANT_TURN, timeout)
    # 2) 等生成彻底完成（stop→send / 输入框可用）
    wait_until_idle(drv)
    time.sleep(0.4)

    # 3) 再保险：复制前确保 hook 已装
    install_clipboard_hook(drv)

    # 4) 只点最后一条回答里的复制按钮
    clicked = click_copy_button_in_last_turn(drv)

    # 5) A 路：优先从我们挂的 window.__lastCopiedText 读取（最稳）
    if clicked:
        md = read_captured_markdown(drv, timeout=6.0)
        if md:
            return md

    # 6) B 路：尝试浏览器剪贴板读取
    if clicked:
        md = read_clipboard_via_browser(drv, timeout=6.0)
        if md:
            return md

    # 7) C 路：系统剪贴板（pyperclip）
    try:
        md2 = (pyperclip.paste() or "").strip()
        if md2:
            return md2
    except Exception:
        pass

    # 8) 兜底：纯文本 + 明确提示
    nodes = drv.find_elements(*SELECTORS.ASSISTANT_MESSAGE)
    fallback = nodes[-1].text.strip() if nodes else ""
    return f"> ⚠️ 未能复制为 Markdown，以下为纯文本回退：\n\n{fallback}"




def append_to_md(md_file: Path, rel_img: Path, answer_md: str, idx: int):
    with md_file.open("a", encoding="utf-8") as f:
        f.write(f"\n\n---\n\n## 第 {idx} 页\n\n")
        f.write(f"![第 {idx} 页]({rel_img.as_posix()})\n\n")
        f.write(f"**提问：** {CFG.prompt_text}\n\n")
        f.write(answer_md)  # 直接写入 Markdown（不加额外包裹）
        f.write("\n")


# ===================== MAIN =====================
def main():
    img_dir, asset_dir = ensure_out_dirs(CFG.out_dir)
    notes_md = CFG.out_dir / "notes.md"
    if not CFG.input_pdf.exists():
        print(f"[ERROR] PDF 不存在：{CFG.input_pdf}"); sys.exit(2)

    print("[1/5] PDF → 图片")
    pages = pdf_to_images(CFG.input_pdf, img_dir, CFG.render_dpi)
    drv = start_browser(CFG.headless)
    go_to_chat(drv)
    print("[2/5] 登录成功，开始循环上传...")

    for idx, img_path in enumerate(pages, start=1):
        print(f"  - 处理第 {idx} 页：{img_path.name}")
        target = asset_dir / img_path.name
        shutil.copy(img_path, target)
        rel = Path("notes_assets") / img_path.name

        upload_image(drv, target)                 # 只允许一张缩略图
        type_prompt_and_send(drv, CFG.prompt_text)
        answer = wait_for_latest_answer(drv, CFG.answer_timeout)  # 等到停止→发送
        append_to_md(notes_md, rel, answer, idx)

    print(f"[✔] 完成！结果保存在：{notes_md.resolve()}")
    drv.quit()

if __name__ == "__main__":
    main()
