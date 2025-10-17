#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Q&A from PDF → chat → Markdown notes.
这版新增：
- 通过命令行参数指定“备课目标文件名”（可含路径，可带/不带扩展名）
- output/ 放在该目标文件名的同目录
- 生成的 md 命名为 <目标文件名>_prepare.md
"""

from __future__ import annotations
import sys, time, shutil, argparse
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
import re

# ===================== CONFIG =====================
@dataclass
class Config:
    input_pdf: Path = Path("Week 11 - 2. Scalable Algorithm Templates.pdf")
    out_dir: Path = Path("output")  # 会在运行时根据 --target 重置
    site_url: str = "https://dn7vxt.aitianhu2.top/?model=gpt-5"
    login_url: str = "https://dn7vxt.aitianhu2.top/list"
    access_key: str = "sk-fi9uVjhlfirEQMJRE8Da97D764624a948fC2B2657b58636e"
    # prompt_text: str = "我是一名远程教学老师，正在准备一堂课的教学内容。我需要你帮助我对以下截图中的内容进行逐句解析和教学指导，具体要求如下： \
    # 1. **内容解析要求：**                                                                                                              \
    # - 对每句话/段落进行详细解释（包括含义、背景知识、关键概念等）\
    # - 指出学生可能不理解的部分\
    # - 提供简单易懂的类比或例子辅助理解\
    # 2. **教学应用要求：**\
    # - 为每部分内容设计教学步骤\
    # - 建议讲解重点和强调部分\
    # - 提供引导学生思考的问题\
    # - 设计课堂互动环节\
    # 3. **输出格式：**\
    # [截图内容]     \
    # - 详细解释：\
    # - 教学重点：\
    # - 学生可能的问题："
    prompt_text: str = "我现在是一名远程教学老师，需要备课，告诉我这个截图是什么意思并且详细解释，到时候上课我会根据这个回答讲课"
    # prompt_text: str = "我现在是一名远程教学老师，需要备课，请对截图中的内容逐句详细使用中文解释，不仅仅只是翻译，还需要对它们进行适当的解释,告诉我该怎么教学生并且指导怎么做，到时候上课我会根据这个回答讲课"
    reuse_session: bool = True
    headless: bool = False
    page_load_timeout: int = 30
    upload_timeout: int = 90
    answer_timeout: int = 120
    post_submit_sleep: float = 1.2
    render_dpi: int = 180
    stable_pause: float = 0.8
    idle_timeout: int = 180

CFG = Config()

# ===================== SELECTORS =====================
class SELECTORS:
    KEY_INPUT = (By.CSS_SELECTOR, "input#input-code")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button#login-button")
    FILE_INPUT = (By.CSS_SELECTOR, "input#upload-photos[type='file']")
    PROMPT_AREA = (By.CSS_SELECTOR, "div#prompt-text-area[contenteditable='true']")
    PROMPT_AREA_FALLBACK = (By.CSS_SELECTOR, "div.ProseMirror[contenteditable='true']")
    SEND_BUTTON = (By.CSS_SELECTOR, "button[data-testid='send-button'], button#composer-submit-button[aria-label*='发送']")
    STOP_BUTTON = (By.CSS_SELECTOR, "button[data-testid='stop-button'], button#composer-submit-button[aria-label*='停止'], button[aria-label*='Stop']")
    ASSISTANT_MESSAGE = (By.CSS_SELECTOR, "[data-message-author-role='assistant'], div.assistant, div.markdown")
    TILE_SEL = "span[style*='background-image'],img[src^='blob:'],img[src^='data:']"
    CHANGE_ACCOUNT_BUTTON = (By.CSS_SELECTOR,
        "div#changeButton, div[title*='切换系统后台账号'], div[title*='change account']"
    )
    ASSISTANT_TURN = (
        By.CSS_SELECTOR,
        'article[data-turn="assistant"], '
        'article[data-message-author-role="assistant"], '
        '[data-message-author-role="assistant"] article'
    )
    COPY_BUTTON_IN_TURN = (
        By.CSS_SELECTOR,
        'button[data-testid="copy-turn-action-button"], '
        'button[aria-label*="复制"], button[aria-label*="拷贝"], '
        'button[aria-label*="Copy"]'
    )

# ===================== 剪贴板 hook（与你现有一致，略） =====================
def grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top"):
    try:
        drv.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": origin,
            "permissions": ["clipboardReadWrite", "clipboardSanitizedWrite"]
        })
    except Exception:
        pass

def install_clipboard_hook(drv):
    js = r"""
    if (!window.__tap_copy_hooked__) {
      window.__tap_copy_hooked__ = true;
      (function(){
        try {
          const orig = (navigator.clipboard && navigator.clipboard.writeText)
                       ? navigator.clipboard.writeText.bind(navigator.clipboard) : null;
          window.__lastCopiedText = window.__lastCopiedText || '';
          if (orig) {
            navigator.clipboard.writeText = (t) => {
              window.__lastCopiedText = (t || '');
              try { return orig(t); } catch(e) { return Promise.resolve(); }
            };
          } else {
            navigator.clipboard = {
              writeText: (t)=>{ window.__lastCopiedText = (t || ''); return Promise.resolve(); },
              readText: ()=>Promise.resolve(window.__lastCopiedText || '')
            };
          }
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

def read_clipboard_via_browser(drv, timeout=6.0) -> str:
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

# ===================== 工具函数（与你现有一致，略） =====================
def ensure_assets_dir(assets_dir: Path):
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir

class OverloadedAccountError(Exception):
    """当前会话所属官网账号超负荷。"""
    pass

def is_overloaded_text(txt: str) -> bool:
    if not txt:
        return False
    needles = [
        "官网账号超负荷", "更换账号并新建会话",
        "account to which the current conversation belongs is overloaded",
        "please change the account and create a new conversation",
    ]
    low = txt.lower()
    return any(n in low for n in [s.lower() for s in needles])


def render_page_if_needed(pdf_path: Path, assets_dir: Path, page_idx: int, dpi: int = 180) -> Path:
    """
    page_idx : 0-based
    返回 assets_dir / page-xxx.png 的绝对路径
    已存在且比 pdf 新 → 直接复用；否则只渲染这一页
    """
    png_path = assets_dir / f"page-{page_idx+1:03d}.png"
    pdf_mtime = pdf_path.stat().st_mtime
    if png_path.exists() and png_path.stat().st_mtime > pdf_mtime:
        print(f"[reuse] 复用已有图片：{png_path.name}")
        return png_path

    # 只抽这一页
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_idx)          # 0-based
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    pix.save(png_path)
    doc.close()
    print(f"[render] 已渲染单页：{png_path.name}")
    return png_path

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
    grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top")
    install_clipboard_hook(drv)
    time.sleep(0.5)

def start_new_conversation(drv):
    drv.get(CFG.site_url); maybe_login(drv)
    grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top")
    install_clipboard_hook(drv); time.sleep(0.5)

def click_change_account_and_new_session(drv, reason: str = "") -> bool:
    """
    点击右侧“切换系统后台账号”按钮，并回到新会话页面。
    返回 True 表示点击成功并完成会话重建；False 表示未找到/未点击成功。
    """
    tag = "[switch]"
    if reason:
        tag += f" {reason}"
    print(f"{tag} 尝试点击“切换系统后台账号”按钮…")
    try:
        btn = WebDriverWait(drv, 5).until(EC.element_to_be_clickable(SELECTORS.CHANGE_ACCOUNT_BUTTON))
    except Exception as e:
        print(f"{tag} 未找到按钮：{e!r}")
        return False

    try:
        # 两种方式都试一次，提升成功率
        btn.click()
    except Exception:
        try:
            drv.execute_script("arguments[0].click();", btn)
        except Exception as e:
            print(f"{tag} 点击失败：{e!r}")
            return False

    # 等页面切换完成后，回到聊天页（新会话）
    time.sleep(0.8)
    try:
        start_new_conversation(drv)  # 复用你已有的逻辑：打开 site_url + 重新安装 clipboard hook
        print(f"{tag} 已切换账号并新建会话。")
        return True
    except Exception as e:
        print(f"{tag} 切换后重建会话失败：{e!r}")
        return False


def refresh_and_prepare(drv, reason: str = ""):
    """刷新页面并恢复必要状态（权限 + clipboard hook），附带日志。"""
    tag = f"[refresh] {reason}".strip() if reason else "[refresh]"
    print(f"{tag} 正在刷新页面…")
    try:
        drv.refresh()
    except Exception as e:
        print(f"{tag} 刷新时发生异常：{e!r}")
    # 尝试等待空闲，但不要因再次超时而中断整个恢复流程
    try:
        wait_until_idle(drv, timeout=CFG.idle_timeout)
    except Exception as e:
        print(f"{tag} 刷新后等待空闲出现问题：{e!r}（忽略，继续）")
    # 重新授权 & 安装剪贴板 hook
    try:
        grant_clipboard_permissions(drv, origin="https://dn7vxt.aitianhu2.top")
        install_clipboard_hook(drv)
    except Exception as e:
        print(f"{tag} 恢复剪贴板 hook 出现问题：{e!r}（忽略，继续）")


def clear_all_uploads(drv):
    drv.execute_script("""
        document.querySelectorAll('span[style*="background-image"], img[src^="blob:"], img[src^="data:"]').forEach(el => el.remove());
        document.querySelectorAll('input#upload-photos').forEach(inp => { try { inp.value = ''; } catch(e){} });
    """)
    time.sleep(0.3)

def count_tiles(drv) -> int:
    try:
        return drv.execute_script("return document.querySelectorAll(arguments[0]).length;", SELECTORS.TILE_SEL)
    except Exception:
        return 0


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

def is_generating(drv) -> bool:
    return len(drv.find_elements(*SELECTORS.STOP_BUTTON)) > 0

def wait_until_idle(drv, timeout: int = None):
    if timeout is None:
        timeout = CFG.idle_timeout
    t0 = time.time()
    last_state = None
    while time.time() - t0 < timeout:
        has_stop = len(drv.find_elements(*SELECTORS.STOP_BUTTON)) > 0
        has_send = len(drv.find_elements(*SELECTORS.SEND_BUTTON)) > 0
        prompt_ready = len(drv.find_elements(*SELECTORS.PROMPT_AREA)) > 0 or \
                       len(drv.find_elements(*SELECTORS.PROMPT_AREA_FALLBACK)) > 0
        state = f"stop={has_stop}, send={has_send}, prompt={prompt_ready}"
        if state != last_state:
            print(f"[idle] {state}")
            last_state = state
        if has_stop:
            time.sleep(0.35); continue
        if has_send or prompt_ready:
            return
        time.sleep(0.35)
    raise TimeoutException("等待模型生成完成超时。")

def upload_image(drv, img_path: Path):
    try:
        wait_until_idle(drv)
    except TimeoutException:
        print("[upload] 警告：未确认空闲，仍尝试上传")
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
    try:
        btns = drv.find_elements(*SELECTORS.SEND_BUTTON)
        if btns: btns[0].click()
    except Exception:
        pass

def click_copy_button_in_last_turn(drv) -> bool:
    turns = drv.find_elements(*SELECTORS.ASSISTANT_TURN)
    if not turns: return False
    turn = turns[-1]
    drv.execute_script("arguments[0].scrollIntoView({block:'center'});", turn)
    time.sleep(0.1)
    btns = turn.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN) or drv.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN)
    if not btns: return False
    btn = btns[-1]
    try:
        WebDriverWait(drv, 5).until(EC.element_to_be_clickable(btn))
    except Exception:
        pass
    try:
        btn.click(); return True
    except Exception:
        try:
            drv.execute_script("arguments[0].click();", btn); return True
        except Exception:
            return False

def wait_for_latest_answer(drv, timeout):
    wait_for(drv, SELECTORS.ASSISTANT_TURN, timeout)
    wait_until_idle(drv)
    time.sleep(0.4)
    install_clipboard_hook(drv)

    # ===== 新增：多次尝试复制 =====
    last_text = ""
    for retry in range(2):  # 尝试两次
        clicked = click_copy_button_in_last_turn(drv)
        if clicked:
            md = read_captured_markdown(drv, timeout=6.0)
            if md and md.strip() and md.strip() != last_text:
                return md.strip()
            md = read_clipboard_via_browser(drv, timeout=6.0)
            if md and md.strip() and md.strip() != last_text:
                return md.strip()
            try:
                md2 = (pyperclip.paste() or "").strip()
                if md2 and md2 != last_text:
                    return md2
            except Exception:
                pass

            # 如果没读到内容或内容没变化，就再按一次复制按钮
            print(f"[copy] 第 {retry+1} 次复制无变化，准备重试点击复制按钮…")
            last_text = md or md2 or ""
            time.sleep(1.0)
        else:
            print("[copy] 未能点击复制按钮，重试中…")
            time.sleep(1.0)

    # ===== 原 fallback 部分 =====
    nodes = drv.find_elements(*SELECTORS.ASSISTANT_MESSAGE)
    fallback = nodes[-1].text.strip() if nodes else ""
    return f"> ⚠️ 未能复制为 Markdown，以下为纯文本回退：\n\n{fallback}"

def compact_blank_lines(text: str) -> str:
    """
    清理 Markdown 里的多余空行：
    - 去掉文首文尾空行
    - 把连续 2 个以上空行压缩成 1 个
    - 删除行首/行尾的空格
    """
    # 去掉前后空白行
    text = text.strip()

    # 删除行首尾空格
    lines = [line.strip() for line in text.splitlines()]

    # 压缩连续空行（最多保留 1 个）
    cleaned = []
    last_blank = False
    for line in lines:
        if line == "":
            if not last_blank:
                cleaned.append("")
            last_blank = True
        else:
            cleaned.append(line)
            last_blank = False

    return "\n".join(cleaned)

def append_to_md(md_file: Path, rel_img: Path, answer_md: str, page_no: int):
    with md_file.open("a", encoding="utf-8") as f:
        f.write(f"\n\n---\n\n## 第 {page_no} 页\n\n")
        f.write(f"![第 {page_no} 页]({rel_img.as_posix()})\n\n")
        f.write(compact_blank_lines(answer_md))   # ← 只改这一行
        f.write("\n")

def ask_with_retries(drv, img_path: Path, prompt: str, base_timeout: int, max_attempts: int = 5) -> str:
    """
    针对当前图片执行：上传 → 提问 → 等待答案，并在超时时进行：
      1) 刷新并重问
      2) 仍不行：sleep(10) 再刷新并重问
      3) 仍不行：翻倍等待时间并继续尝试（直到 max_attempts）

    返回：Markdown 文本（或纯文本回退）。
    """
    # 每次尝试前都重新上传并提问，确保刷新后上下文干净
    def _upload_and_ask():
        upload_image(drv, img_path)
        # ===== 新增：检查图片是否被吞掉 =====
        try:
            tiles = count_tiles(drv)
            if tiles == 0:
                print("[ask] 检测到图片预览丢失，重新上传一次…")
                upload_image(drv, img_path)
                tiles2 = count_tiles(drv)
                if tiles2 == 0:
                    raise RuntimeError("图片多次上传后仍未显示，可能被网页吞掉。")
        except Exception as e:
            print(f"[ask] 上传检查出错：{e!r}（将重试上传）")
            time.sleep(2)
            upload_image(drv, img_path)

        # ===================================
        type_prompt_and_send(drv, prompt)

    attempt = 1
    timeout = int(base_timeout)

    while attempt <= max_attempts:
        print(f"[ask] 尝试 #{attempt}，当前等待时长={timeout}s")
        try:
            _upload_and_ask()
            answer = wait_for_latest_answer(drv, timeout)

            # ====== 新增：检测“账号超负荷” ======
            if is_overloaded_text(answer):
                print("[ask] 检测到“账号超负荷”提示，准备切换后台账号并新建会话…")
                if click_change_account_and_new_session(drv, reason="因超负荷触发"):
                    # 切换成功：不计入一次失败，直接继续重试当前页（重新上传&提问）
                    print("[ask] 已完成后台账号切换，新会话已就绪，将在当前页重新发起提问。")
                    # 不 return，不 raise，不递增 attempt，直接继续下一轮 while
                    continue
                else:
                    # 按钮没点成，退回到你的刷新/翻倍策略（等同一次失败）
                    print("[ask] 未能点击“切换”按钮，将按超时重试策略继续。")
                    raise TimeoutException("账号超负荷，但切换按钮点击失败。")
            # ===================================

            print(f"[ask] 成功于尝试 #{attempt}")
            return answer

        except TimeoutException as e:
            msg = str(e) or "TimeoutException"
            print(f"[ask] 尝试 #{attempt} 超时：{msg}")

            if attempt == 1:
                refresh_and_prepare(drv, reason="首次超时 → 刷新重试")
            elif attempt == 2:
                print("[ask] 二次超时：sleep(10s) 后再刷新重试")
                time.sleep(10.0)
                refresh_and_prepare(drv, reason="二次超时 → 再次刷新重试")
            else:
                timeout = max(timeout * 2, timeout + 30)
                print(f"[ask] 多次超时：将等待时长翻倍为 {timeout}s 后继续尝试")

            attempt += 1

        except Exception as e:
            print(f"[ask] 尝试 #{attempt} 出现非超时异常：{e!r}（将继续下一轮或最终抛出）")
            raise

    raise TimeoutException(f"多次重试后仍超时（共 {max_attempts} 次），请稍后再试。")


# ===================== 路径解析：根据 --target 计算输出位置 =====================
def compute_paths_by_target(target_arg: str):
    """
    target_arg 可为：
      - 仅文件名（不带扩展名）：如 'week0'
      - 带扩展名：如 'week0.md'
      - 含路径：如 'D:/notes/week0' 或 'D:/notes/week0.md'

    返回：
      base_dir: 目标所在目录
      notes_md: <stem>_prepare.md（与目标同目录）
      assets_dir: <stem>_assets（与目标同目录、存放图片）
    """
    raw = Path(target_arg).expanduser()
    stem = raw.stem if raw.suffix else raw.name
    base_dir = (raw.parent if str(raw.parent) not in ("", ".") else Path.cwd()).resolve()

    notes_md = base_dir / f"{stem}_prepare.md"
    assets_dir = base_dir / f"{stem}_assets"   # ← 每个目标独立资产目录
    return base_dir, notes_md, assets_dir


# ===================== MAIN =====================
# =====================  MAIN  =====================
def main():
    parser = argparse.ArgumentParser(description="PDF逐页问答并生成备课Markdown")
    parser.add_argument("-t", "--target", required=True,
                        help="备课目标文件名（可含路径，可带/不带扩展名）")
    parser.add_argument("-p", "--pdf", required=True,
                        help="输入 PDF 文件路径")
    parser.add_argument("--start", type=int, default=1,
                        help="起始页码（从 1 开始）")
    parser.add_argument("--end", type=int, default=None,
                        help="终止页码（包含）")
    parser.add_argument("--headless", action="store_true",
                        help="无界面模式运行 Chrome")
    args = parser.parse_args()

    # 覆盖配置
    CFG.input_pdf = Path(args.pdf).expanduser().resolve()
    CFG.headless = bool(args.headless)
    base_dir, notes_md, assets_dir = compute_paths_by_target(args.target)
    assets_dir = ensure_assets_dir(assets_dir)

    if not CFG.input_pdf.exists():
        print(f"[ERROR] PDF 不存在：{CFG.input_pdf}")
        sys.exit(2)

    # 计算合法页码范围
    pdf_doc = fitz.open(CFG.input_pdf)
    total_pages = pdf_doc.page_count
    pdf_doc.close()
    start_idx = max(1, args.start)
    end_idx = min(args.end if args.end else total_pages, total_pages)
    if start_idx > end_idx:
        print(f"[ERROR] 页码范围非法：start={start_idx}, end={end_idx}")
        sys.exit(2)
    print(f"[INFO] 将处理第 {start_idx} 至 {end_idx} 页，共 {end_idx - start_idx + 1} 页。")

    drv = start_browser(CFG.headless)
    go_to_chat(drv)
    print(f"[2/5] 登录成功，资产目录：{assets_dir}")
    print(f"[2/5] 目标笔记：{notes_md}")

    # 逐页按需渲染 / 复用
    for page_no in range(start_idx, end_idx + 1):
        img_path = render_page_if_needed(CFG.input_pdf, assets_dir,
                                         page_idx=page_no - 1,
                                         dpi=CFG.render_dpi)
        rel_img = Path(assets_dir.name) / img_path.name
        print(f"  - 处理第 {page_no} 页：{img_path.name}")

        try:
            answer = ask_with_retries(drv=drv,
                                      img_path=img_path,
                                      prompt=CFG.prompt_text,
                                      base_timeout=CFG.answer_timeout,
                                      max_attempts=5)
        except TimeoutException as e:
            print(f"[ask] 第 {page_no} 页最终失败：{e}")
            answer = f"> ⚠️ 本页多次重试仍超时，稍后请手动重试。\n\n原因：{e}"
        except Exception as e:
            print(f"[FATAL] 第 {page_no} 页出现致命错误：{e!r}")
            with open(notes_md, "a", encoding="utf-8") as f:
                f.write(f"\n\n> ❌ 程序在第 {page_no} 页因异常停止：{e!r}\n")
            drv.quit()
            sys.exit(1)

        append_to_md(notes_md, rel_img, answer, page_no)

    print(f"[✔] 完成！结果保存在：{notes_md.resolve()}")
    drv.quit()

if __name__ == "__main__":
    main()
