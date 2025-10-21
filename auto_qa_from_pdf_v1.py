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
import subprocess
import sys
from pathlib import Path

import random
import sys, time, argparse
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
import re
import smtplib, ssl          # 新增
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    JavascriptException,
    WebDriverException,
)
from urllib3.exceptions import ReadTimeoutError as URLLib3ReadTimeoutError, ProtocolError as URLLib3ProtocolError
try:
    from requests.exceptions import ConnectionError as RequestsConnectionError
except Exception:
    class RequestsConnectionError(Exception):  # 兜底
        pass

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
    prompt_text: str = "什么意思？详细解释，中文回答 并且在后面加一项主要归纳你的这次回答，变成一个口语化的表述，内容要覆盖整个截图，格式是[口语化表达] 正文"
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
    # 限流专用
    max_backoff: int = 5          # 最大连续翻倍次数
    backoff_mult: int = 2        # 每次翻倍倍数
    driver_http_timeout: int = 300   # WebDriver 命令读超时（秒）


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
    # ASSISTANT_MESSAGE = (By.CSS_SELECTOR, "[data-message-author-role='assistant'], div.assistant, div.markdown")
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
    ERROR_BUBBLE = (By.CSS_SELECTOR, "div.text-token-text-error")  # 红色错误提示容器
    REGENERATE_ERROR_BTN = (By.CSS_SELECTOR, "button[data-testid='regenerate-thread-error-button']")

def extract_wait_seconds(text: str) -> int | None:
    """从错误提示中提取等待秒数；只在 wait/等待 的语境里取数，避免命中 3h0m0s。"""
    if not text:
        return None

    # 归一化
    t = text.strip()
    t = re.sub(r"^>\s*⚠️.*?\n+", "", t, flags=re.S)  # 去回退提示
    t = re.sub(r"(?m)^\s*>\s*", "", t)              # 去 blockquote
    t = re.sub(r"\s+", " ", t).strip().lower()

    # 1) 英文优先：please wait / retry in / wait ... before trying
    m = re.search(r"(?:please\s*wait|wait)\D{0,12}?(\d+)\s*(?:s|sec|secs|second|seconds)\b", t, flags=re.I)
    if m:
        return int(m.group(1))

    m = re.search(r"retry\s*in\D{0,12}?(\d+)\s*(?:s|sec|secs|second|seconds)\b", t, flags=re.I)
    if m:
        return int(m.group(1))

    m = re.search(r"(\d+)\s*(?:s|sec|secs|second|seconds)\s*before\s*(?:retry|trying)\b", t, flags=re.I)
    if m:
        return int(m.group(1))

    # 2) 中文：请等待 N 秒 / N 秒后重试
    m = re.search(r"请等待\s*(\d+)\s*秒", t)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*秒\s*后(?:重试|再试|重发|重提问)", t)
    if m:
        return int(m.group(1))

    # 3) “等待 1分30秒”这类（必须出现在 等待/please wait 语境里，避免命中 3h0m0s）
    m = re.search(r"(?:请?等待|please\s*wait)\D{0,12}?(\d+)\s*(?:分钟?|min|m)\s*(\d+)\s*(?:秒|sec|s)\b", t, flags=re.I)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))

    # 调试帮助（可保留）
    print(f"[extract_wait_seconds] 未识别到秒数，片段: {t[:140]}")
    return None


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
    # ← 新增：提高 WebDriver 命令读超时 / 脚本执行超时
    try:
        drv.command_executor.set_timeout(CFG.driver_http_timeout)
    except Exception:
        pass
    try:
        drv.set_script_timeout(CFG.driver_http_timeout)
    except Exception:
        pass

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
    """打开聊天页；一旦超时立即刷新，无限重试直到成功。"""
    for url in (CFG.login_url, CFG.site_url):
        while True:                       # 死循环，直到加载成功
            try:
                drv.get(url)              # 尝试加载
                break                     # 成功就跳出
            except TimeoutException as e:
                print(f"[net] 加载 {url} 超时，立即刷新重试… ({e})")
                try:
                    drv.refresh()         # 刷新一次
                except Exception as e2:   # 刷新也超时？继续刷新
                    print(f"[net] 刷新同样超时，继续刷新… ({e2})")
                continue                  # 继续 while True

        maybe_login(drv)

    # 以下是你原来的授权 & hook
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
    # 1. 清空剪贴板缓存
    try:
        drv.execute_script("window.__lastCopiedText = '';")
    except Exception:
        pass
    try:
        import pyperclip
        pyperclip.copy("")
    except Exception:
        pass

    turns = drv.find_elements(*SELECTORS.ASSISTANT_TURN)
    if not turns:
        return False
    turn = turns[-1]
    drv.execute_script("arguments[0].scrollIntoView({block:'center'});", turn)
    time.sleep(0.1)

    btns = turn.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN) or drv.find_elements(*SELECTORS.COPY_BUTTON_IN_TURN)
    if not btns:
        return False
    btn = btns[-1]

    try:
        WebDriverWait(drv, 5).until(EC.element_to_be_clickable(btn))
    except Exception:
        pass

    # 2. 点击复制按钮
    try:
        btn.click()
    except Exception:
        try:
            drv.execute_script("arguments[0].click();", btn)
        except Exception:
            return False

    # 3. ✅ 检测是否出现“Failed to copy”提示（显式等待 1.5 s）
    try:
        WebDriverWait(drv, 1.5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Failed to copy')]")
            )
        )
        print("[copy] 检测到“Failed to copy”提示，视为复制失败")
        return False
    except TimeoutException:
        # 未出现提示，认为点击成功
        pass

    return True

import hashlib

def _fingerprint(text: str) -> str:
    return hashlib.sha1((text or "").strip().encode("utf-8", "ignore")).hexdigest()

def wait_for_latest_answer(drv, timeout, last_fp: str = "") -> dict:
    """
    返回：
      {"kind":"rate_limit", "wait":秒, "raw":文本}
      {"kind":"answer", "md":markdown_or_text, "fp":sha1}
      {"kind":"empty"}  # 没拿到新内容
    """

    # 1. 等待最后一条 assistant turn 出现（确保页面已加载）
    wait_for(drv, SELECTORS.ASSISTANT_TURN, timeout)
    wait_until_idle(drv)
    time.sleep(0.4)
    install_clipboard_hook(drv)

    # 2. 获取最后一条 assistant turn
    turns = drv.find_elements(*SELECTORS.ASSISTANT_TURN)
    if not turns:
        return {"kind": "empty"}
    turn = turns[-1]
    drv.execute_script("arguments[0].scrollIntoView({block:'center'});", turn)

    # 3. ✅ 优先获取内容（复制或 DOM）
    copied = click_copy_button_in_last_turn(drv)
    md = ""
    if copied:
        md = read_captured_markdown(drv, timeout=6.0) or read_clipboard_via_browser(drv, timeout=6.0)
        if not md:
            try:
                import pyperclip
                md = (pyperclip.paste() or "").strip()
            except Exception:
                md = ""
    if not md:
        # 兜底：直接读 DOM
        try:
            md_nodes = turn.find_elements(By.CSS_SELECTOR, ".markdown, .prose, [data-message-author-role='assistant']")
            md = (md_nodes[-1].text if md_nodes else turn.text).strip()
        except Exception:
            md = ""

    # 4. ✅ 如果内容为空，**直接返回 empty**，**不再检查限流**
    if not md:
        return {"kind": "empty"}

    # 5. ✅ 内容非空，再检查是否有限流提示（避免残留误报）
    err_nodes = turn.find_elements(By.CSS_SELECTOR, "div.text-token-text-error")
    if err_nodes:
        err_text = (err_nodes[-1].text or "").strip()
        sec = extract_wait_seconds(err_text)
        if sec is not None:
            return {"kind": "rate_limit", "wait": sec, "raw": err_text}

    # 6. ✅ 内容指纹去重
    fp = _fingerprint(md)
    if last_fp and fp == last_fp:
        return {"kind": "empty"}

    return {"kind": "answer", "md": md, "fp": fp}

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
    def _upload_and_ask():
        upload_image(drv, img_path)
        tiles = count_tiles(drv)
        if tiles == 0:
            upload_image(drv, img_path)
        type_prompt_and_send(drv, prompt)

    attempt = 1
    timeout = int(base_timeout)
    last_fp = ""  # 记录上一条内容的指纹，防止读到旧内容
    transient_errs = 0
    transient_err_cap = 8  # 每页最多软错误次数

    while attempt <= max_attempts:
        print(f"[ask] 尝试 #{attempt}，当前等待时长={timeout}s")
        try:
            _upload_and_ask()
            res = wait_for_latest_answer(drv, timeout, last_fp=last_fp)

            if res.get("kind") == "rate_limit":
                wait_sec = max(5, min(600, int(res.get("wait", 30))))
                wait_sec += random.randint(2, 7)  # 抖动
                print(f"[rate-limit] 命中限流：{res.get('wait')}s → 实际等待 {wait_sec}s 后在【同一页】重试…")
                time.sleep(wait_sec)
                last_fp = ""
                # 直接继续同一页，不增 attempt
                continue

            if res.get("kind") == "empty":
                print("[copy] 未拿到新内容（可能复制失败或仍在生成），刷新后原页重试…")
                refresh_and_prepare(drv, reason="empty content")
                time.sleep(1.0)
                # 不增 attempt，继续同一页
                continue

            if res.get("kind") == "answer":
                last_fp = res.get("fp", "")
                print(f"[ask] 成功于尝试 #{attempt}")
                return res["md"]

            # 兜底
            print("[ask] 未知返回，按 empty 处理，原页重试…")
            continue

        except TimeoutException as e:
            print(f"[ask] 尝试 #{attempt} 超时：{e}")
            # ✅ 超过 300 s 就视为卡死，刷新重试当前页
            if timeout >= 300:
                print(f"[ask] 等待时长已达 {timeout}s，视为卡死，刷新页面后重试当前页…")
                refresh_and_prepare(drv, reason=f"等待超时已达 {timeout}s")
                time.sleep(1)
                # 不增加 attempt，继续当前页
                continue

            # ✅ 300 s 以内才允许翻倍
            if attempt == 1:
                refresh_and_prepare(drv, reason="首次超时 → 刷新重试")
            elif attempt == 2:
                print("[ask] 二次超时：sleep(10s) 后再刷新重试")
                time.sleep(10.0)
                refresh_and_prepare(drv, reason="二次超时 → 再次刷新重试")
            else:
                timeout = min(300, max(timeout * 2, timeout + 30))  # ✅ 封顶 300 s
                print(f"[ask] 将等待时长翻倍为 {timeout}s 后继续尝试")
            attempt += 1

        except Exception as e:
            # 归类：哪些属于“可恢复”（刷新即可），哪些属于“需要重启”（此处先不做重启，只刷新），其余才真正抛出
            transient_types = (
                URLLib3ReadTimeoutError, URLLib3ProtocolError, RequestsConnectionError,
                StaleElementReferenceException,
                ElementClickInterceptedException,
                ElementNotInteractableException,
                JavascriptException,
            )

            msg = (str(e) or "").lower()
            looks_transient = isinstance(e, transient_types) or any(
                s in msg for s in [
                    "stale element reference",
                    "element is not clickable",
                    "javascript error",
                    "httpconnectionpool",
                    "read timed out",
                    "net::err_",  # 网络波动
                ]
            )

            if looks_transient:
                transient_errs += 1
                if transient_errs > transient_err_cap:
                    print(f"[ask] 可恢复异常已超过 {transient_err_cap} 次，按一次失败处理并增加 attempt…")
                    attempt += 1
                    continue

                print(f"[ask] 可恢复异常：{e!r} → 刷新页面后【同一页】重试…")
                try:
                    refresh_and_prepare(drv, reason="transient exception")
                except Exception as e2:
                    print(f"[ask] 刷新时也出错（忽略继续）：{e2!r}")
                time.sleep(1.5)
                # 关键：不计入 attempt，不前进页
                continue

            # WebDriverException 里也有一部分可以当软错误（例如短暂的 devtools 断连）
            if isinstance(e, WebDriverException):
                if any(s in msg for s in ["not connected to devtools", "target closed"]):
                    print(f"[ask] WebDriver 短暂断连：{e!r} → 刷新后同页重试…")
                    try:
                        refresh_and_prepare(drv, reason="devtools reconnect")
                    except Exception as e2:
                        print(f"[ask] 刷新失败（忽略继续）：{e2!r}")
                    time.sleep(1.5)
                    continue

            # 其余才按真正异常处理
            print(f"[ask] 尝试 #{attempt} 出现不可恢复异常：{e!r}")
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

def send_qq_mail(to_addr: str, subject: str, body: str):
    """用 QQ 邮箱 SMTP 发信，端口 465（SSL）。"""
    smtp_server = "smtp.qq.com"
    port = 465
    # 这里写你自己的 QQ 邮箱和「授权码」（不是登录密码！）
    sender_email = "1144097453@qq.com"
    password = "drljclcjrxfmgjdg"          # 去 QQ 邮箱设置里生成

    msg = f"From: {sender_email}\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_addr, msg.encode("utf-8"))
    print(f"[mail] 提醒邮件已发送至 {to_addr}")


# =====================  MAIN  =====================
def main():
    parser = argparse.ArgumentParser(description="PDF逐页问答并生成备课Markdown")
    parser.add_argument("-t", "--target",
                        default=None,  # ← 关键：允许缺省
                        help="备课目标文件名（可含路径，可带/不带扩展名）。"
                            "缺省时用第一个 PDF 的路径（去扩展名）作为前缀。")
    parser.add_argument("-p", "--pdf", required=True, action="append", type=Path,
                        help="输入 PDF 文件路径，可多次指定，例如：-p a.pdf -p b.pdf")
    parser.add_argument("--start", dest="ranges", action="append", type=int,
                    help="对该 PDF 的起始页码（从 1 开始）")
    parser.add_argument("--end", dest="ranges", action="append", type=int,
                    help="对该 PDF 的终止页码（包含）")
    parser.add_argument("--headless", action="store_true",
                        help="无界面模式运行 Chrome")
    args = parser.parse_args()

    # 把 --start/--end 按顺序配给前面的 -p
    pdf_and_ranges = []
    starts = args.ranges[::2] if args.ranges else []   # 0,2,4...
    ends   = args.ranges[1::2] if args.ranges else []   # 1,3,5...
    for i, pdf in enumerate(args.pdf):
        start = starts[i] if i < len(starts) else 1
        end   = ends[i]   if i < len(ends)   else None
        pdf_and_ranges.append((Path(pdf), start, end))
    done_list = []          # 记录成功完成的 (pdf, md)
    drv = None              # 浏览器实例

    # ── 缺省 target 逻辑 ──
    if args.target is None:
        if not args.pdf:
            print("[ERROR] 必须至少提供一个 PDF 文件（-p）")
            sys.exit(2)
        args.target = str(args.pdf[0].with_suffix(''))  # 去掉 .pdf
    # ----------------------

    for pdf_path, start, end in pdf_and_ranges:
        pdf_path = pdf_path.expanduser().resolve()
        if not pdf_path.exists():
            print(f"[ERROR] PDF 不存在：{pdf_path}")
            continue

        stem = pdf_path.stem
        base_dir, notes_md, assets_dir = compute_paths_by_target(
            Path(args.target).parent / stem
        )
        assets_dir = ensure_assets_dir(assets_dir)

        pdf_doc = fitz.open(pdf_path)
        total_pages = pdf_doc.page_count
        pdf_doc.close()
        start_idx = max(1, start)
        end_idx = min(end if end else total_pages, total_pages)
        print(f"[INFO] 将处理 {pdf_path.name} 第 {start_idx} 至 {end_idx} 页。")

        # 浏览器只启动一次
        if drv is None:
            drv = start_browser(args.headless)
            go_to_chat(drv)

        # 逐页处理
        for page_no in range(start_idx, end_idx + 1):
            img_path = render_page_if_needed(pdf_path, assets_dir, page_idx=page_no - 1, dpi=CFG.render_dpi)
            rel_img = Path(assets_dir.name) / img_path.name
            print(f"  - 处理第 {page_no} 页：{img_path.name}")

            try:
                answer = ask_with_retries(drv, img_path, CFG.prompt_text, CFG.answer_timeout)
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

        # ===== 单本 PDF 已跑完：生成讲解视频 =====
        print(f"[VIDEO] 开始生成 {notes_md.stem} 的讲解视频…")
        try:
            result = subprocess.run(
                [sys.executable, "auto_gen_audio.py", "--md", str(notes_md)],
                capture_output=True, text=True, check=True
            )
            last_line = result.stdout.strip().splitlines()[-1]
            if "🎉 完整视频已生成" in last_line:
                mp4_path = last_line.split("：")[-1].strip()
                done_list.append((pdf_path, notes_md, Path(mp4_path)))
                print(f"[VIDEO] 已生成并记录：{mp4_path}")
            else:
                print(f"[VIDEO] 未解析到 MP4 路径：{last_line}")
                done_list.append((pdf_path, notes_md, None))
        except subprocess.CalledProcessError as e:
            print(f"[VIDEO] 视频生成失败：{e.stderr}")
            done_list.append((pdf_path, notes_md, None))

   # ===== 全部 PDF 跑完：发邮件（只发通知，不附带视频） =====
    if done_list:
        mp4_lines = [f"{pdf.name} → {mp4}" for pdf, _, mp4 in done_list if mp4]
        if mp4_lines:
            # 邮件正文：只包含视频生成的路径说明，不附带文件
            body = (
                "以下完整讲解视频已生成：\n\n"
                + "\n".join(mp4_lines)
                + "\n\n视频文件已保存在本地，请手动查看或上传云盘。"
            )
            try:
                send_qq_mail(
                    "1144097453@qq.com",
                    "PDF 讲解视频全部完成（无附件）",
                    body
                )
                print("[mail] 已发送完成通知（不包含视频附件）")
            except Exception as e:
                print(f"[mail] 邮件发送失败：{e}")
        else:
            print("[mail] 无成功生成的 MP4，跳过邮件。")


    # 退出浏览器
    if drv:
        drv.quit()

if __name__ == "__main__":
    main()
