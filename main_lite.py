import asyncio
import re
import warnings
import time
import os
import sys
import json
import urllib.request
import subprocess
import threading
import ctypes
import random
import string
import locale
import atexit
import shutil
_FORCE_ENGLISH = False

def _setup_unicode_terminal():
    global _FORCE_ENGLISH
    if sys.platform != 'win32':
        return
    if os.environ.get('WT_SESSION'):
        return
    if os.environ.get('_DOOMX_RELAUNCHED'):
        return
    _localappdata = os.environ.get('LOCALAPPDATA', '')
    _wt_candidates = [os.path.join(_localappdata, 'Microsoft', 'WindowsApps', 'wt.exe')]
    wt = None
    for path in _wt_candidates:
        if os.path.isfile(path):
            wt = path
            break
    if wt is None:
        wt = shutil.which('wt.exe')
    if wt:
        env = os.environ.copy()
        env['_DOOMX_RELAUNCHED'] = '1'
        if getattr(sys, 'frozen', False):
            _args = [sys.executable] + sys.argv[1:]
        else:
            _args = [sys.executable] + sys.argv
        try:
            subprocess.Popen([wt, '--'] + _args, env=env, creationflags=134217728)
            sys.exit(0)
        except Exception:
            pass
    _FORCE_ENGLISH = True
_setup_unicode_terminal()

def _suppress_unraisable(hook_args):
    if hook_args.exc_type is PermissionError:
        return
    sys.__unraisablehook__(hook_args)
sys.unraisablehook = _suppress_unraisable
from tqdm import TqdmExperimentalWarning
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from faker import Faker
from rich.console import Console
warnings.filterwarnings('ignore', category=TqdmExperimentalWarning)
console = Console()
CONFIG_FILE = 'last_config.json'
BROWSERS_FILE = 'browsers.json'
GITHUB_RAW = 'https://raw.githubusercontent.com/TDoomX/exitlag-auto-signup-revamp-lite/main'
LOCAL_VERSION_FILE = 'version.txt'
TRANSLATIONS_LANGS = ['de', 'en', 'es', 'fr', 'it', 'ja', 'pt', 'ru', 'zh', 'vi', 'ar']
_translation_cache = None

def get_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_local_version():
    try:
        with open(os.path.join(get_base(), LOCAL_VERSION_FILE), 'r') as f:
            return f.read().strip()
    except Exception:
        return '0.0.0'

def get_remote_version():
    try:
        url = f'{GITHUB_RAW}/{LOCAL_VERSION_FILE}'
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.read().decode().strip()
    except Exception:
        return None

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    tmp_path = dest_path + '.tmp'
    try:
        urllib.request.urlretrieve(url, tmp_path)
        os.replace(tmp_path, dest_path)
        return True
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False

def load_translations():
    if _FORCE_ENGLISH:
        base = get_base()
        translation_path = os.path.join(base, 'translations', 'en.json')
        with open(translation_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    LANG_MAP = {'pt': 'pt', 'en': 'en', 'es': 'es', 'fr': 'fr', 'de': 'de', 'it': 'it', 'ru': 'ru', 'ja': 'ja', 'zh': 'zh', 'vi': 'vi', 'ar': 'ar', 'portuguese': 'pt', 'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de', 'italian': 'it', 'russian': 'ru', 'japanese': 'ja', 'chinese': 'zh', 'vietnamese': 'vi', 'arabic': 'ar'}
    try:
        locale.setlocale(locale.LC_ALL, '')
        lang_tuple = locale.getlocale()
        raw = lang_tuple[0].split('_')[0].lower() if lang_tuple and lang_tuple[0] else 'en'
        lang = LANG_MAP.get(raw, 'en')
    except Exception:
        lang = 'en'
    base = get_base()
    translation_path = os.path.join(base, 'translations', f'{lang}.json')
    if not os.path.exists(translation_path):
        translation_path = os.path.join(base, 'translations', 'en.json')
    with open(translation_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def tr(key):
    global _translation_cache
    if _translation_cache is None:
        _translation_cache = load_translations()
    return _translation_cache.get(key, key)

def save_config(browser_path, password, proxy, execution_count, plan, fill_speed, silent, close_after=True):
    config = {'browser_path': browser_path, 'password': password, 'proxy': proxy, 'execution_count': execution_count, 'plan': plan, 'fill_speed': fill_speed, 'silent': silent, 'close_after': close_after}
    try:
        with open(os.path.join(get_base(), CONFIG_FILE), 'w') as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

def load_config():
    try:
        path = os.path.join(get_base(), CONFIG_FILE)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[!@#$%^&*()_+\\-=\\[\\]{};\':\\"|,.<>/?]', password):
        return False
    return True

def generate_random_password():
    length = 12
    special_chars = '!@#$%^&*()_+-=[]{};\':"|,.<>/?'
    chars = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits), random.choice(special_chars)]
    all_chars = string.ascii_letters + string.digits + special_chars
    chars.extend((random.choice(all_chars) for _ in range(length - 4)))
    random.shuffle(chars)
    return ''.join(chars)

def gerar_email_aleatorio():
    return ''.join((random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))) + '@juno.com'

def gerar_email_plan2():
    return ''.join((random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))) + '@juno.com'
try:
    import psutil
    _PSUTIL_OK = True
except ImportError:
    _PSUTIL_OK = False

class GhostModeAPI:
    SW_HIDE = 0

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self._EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def _hide_by_title(self, title_substring):
        if not _PSUTIL_OK:
            return

        def foreach_window(hwnd, _):
            try:
                buf = ctypes.create_unicode_buffer(256)
                self.user32.GetWindowTextW(hwnd, buf, 256)
                if title_substring in buf.value and self.user32.IsWindowVisible(hwnd):
                    self.user32.ShowWindow(hwnd, self.SW_HIDE)
            except Exception:
                pass
            return True
        self.user32.EnumWindows(self._EnumWindowsProc(foreach_window), 0)

    def _watch_and_hide_by_pid(self, pid, timeout=60.0, interval=0.03, stop_event=None):
        elapsed = 0.0
        _EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        while elapsed < timeout:
            if stop_event and stop_event.is_set():
                break
            try:

                def foreach_window(hwnd, _):
                    try:
                        pid_out = ctypes.c_ulong(0)
                        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid_out))
                        if pid_out.value == pid and self.user32.IsWindowVisible(hwnd):
                            self.user32.ShowWindow(hwnd, self.SW_HIDE)
                    except Exception:
                        pass
                    return True
                self.user32.EnumWindows(_EnumProc(foreach_window), 0)
            except Exception:
                pass
            time.sleep(interval)
            elapsed += interval

def cleanup_orphaned_browsers():
    try:
        GhostModeAPI()._hide_by_title('DOOM_GHOSTAPI')
    except Exception:
        pass
atexit.register(cleanup_orphaned_browsers)
PLAN_CONFIGS = {'1': {'url': 'https://www.exitlag.com/lp/trial', 'email_fn': 'gerar_email_aleatorio', 'selectors': {'first': '#inputFirstName', 'last': '#inputLastName', 'email': '#inputEmail', 'password': '#inputNewPassword', 'confirm': '#inputNewPassword2', 'tos': '#hero-terms-check'}, 'pre_click': 'button.btn-signup-email', 'pre_delay': 1.0, 'success_url': 'exitlag.com/lp/trial/success', 'success_txt': 'your account has been created', 'submit_fn': 'onLpRegister'}, '2': {'url': 'https://www.exitlag.com/lp/omen', 'email_fn': 'gerar_email_plan2', 'selectors': {'first': '#firstName', 'last': '#lastName', 'email': '#email', 'password': '#password', 'confirm': '#confirmPassword', 'tos': '#acceptTos'}, 'pre_click': None, 'pre_delay': 0.0, 'success_url': 'account_created=1', 'success_txt': 'soon you will recieve an e-mail from exitlag', 'submit_fn': None}}
_EMAIL_FNS = {'gerar_email_aleatorio': gerar_email_aleatorio, 'gerar_email_plan2': gerar_email_plan2}

class BrowserAutomation:

    def __init__(self, plan_config: dict):
        self.cfg = plan_config
        self.fake = Faker()

    async def fill_field_instantly(self, tab, selector, text):
        import json as _json
        sel_json = _json.dumps(selector)
        text_json = _json.dumps(text)
        await tab.execute_script(f"\n            (function() {{\n                var el = document.querySelector({sel_json});\n                if (!el) return;\n                el.focus();\n                el.dispatchEvent(new MouseEvent('click', {{bubbles:true}}));\n                var nativeSetter = Object.getOwnPropertyDescriptor(\n                    Object.getPrototypeOf(el), 'value').set;\n                if (nativeSetter) {{\n                    nativeSetter.call(el, {text_json});\n                }} else {{\n                    el.value = {text_json};\n                }}\n                el.dispatchEvent(new Event('input',  {{bubbles:true}}));\n                el.dispatchEvent(new Event('change', {{bubbles:true}}));\n            }})();\n        ")
        await asyncio.sleep(0.05 + random.random() * 0.08)

    async def _inject_antidetect(self, tab):
        try:
            await tab.execute_script("\n                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});\n                Object.defineProperty(navigator, 'plugins', {\n                    get: () => [\n                        {name:'Chrome PDF Plugin', filename:'internal-pdf-viewer'},\n                        {name:'Chrome PDF Viewer', filename:'mhjfbmdgcfjbbpaeojofohoefgiehjai'},\n                        {name:'Native Client',     filename:'internal-nacl-plugin'}\n                    ]\n                });\n                Object.defineProperty(navigator, 'languages', {\n                    get: () => ['pt-BR','pt','en-US','en']\n                });\n                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});\n                Object.defineProperty(navigator, 'deviceMemory',        {get: () => 8});\n                const _toDataURL = HTMLCanvasElement.prototype.toDataURL;\n                HTMLCanvasElement.prototype.toDataURL = function(type) {\n                    const ctx = this.getContext('2d');\n                    if (ctx) {\n                        const img = ctx.getImageData(0, 0, this.width, this.height);\n                        for (let i = 0; i < img.data.length; i += 100) {\n                            img.data[i] ^= (Math.random() * 2) | 0;\n                        }\n                        ctx.putImageData(img, 0, 0);\n                    }\n                    return _toDataURL.apply(this, arguments);\n                };\n                const _getParam = WebGLRenderingContext.prototype.getParameter;\n                WebGLRenderingContext.prototype.getParameter = function(param) {\n                    if (param === 37445) return 'Google Inc. (NVIDIA)';\n                    if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)';\n                    return _getParam.call(this, param);\n                };\n            ")
        except Exception:
            pass

    async def register_account(self, password, browser_path, log_cb, headless=False, close_after=True, close_after_delay=5, fill_speed='slow'):
        cfg = self.cfg
        sel = cfg['selectors']
        email = _EMAIL_FNS[cfg['email_fn']]()
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        options = ChromiumOptions()
        options.browser_preferences = {'profile.default_content_setting_values.notifications': 2, 'profile.default_content_settings.popups': 0}
        _is_opera = 'opera' in (browser_path or '').lower()
        if headless:
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            if not _is_opera:
                options.add_argument('--window-position=30000,30000')
        elif _is_opera:
            options.add_argument(cfg['url'])
        if browser_path:
            options.binary_location = browser_path
        browser = Chrome(options=options)
        _watcher_stop = threading.Event()
        _ghost_watcher = None
        _existing_opera_pids: set = set()
        if headless and _is_opera and _PSUTIL_OK:
            try:
                _opera_bin = (browser_path or '').lower()
                for _proc in psutil.process_iter(['pid', 'exe']):
                    try:
                        _exe = (_proc.info['exe'] or '').lower()
                        if _opera_bin and _opera_bin in _exe:
                            _existing_opera_pids.add(_proc.info['pid'])
                    except Exception:
                        pass
            except Exception:
                pass
        if _is_opera and _PSUTIL_OK:
            try:
                _opera_bin = (browser_path or '').lower()
                for _proc in psutil.process_iter(['pid', 'exe', 'status']):
                    try:
                        _exe = (_proc.info['exe'] or '').lower()
                        if _opera_bin and _exe == _opera_bin and (_proc.info['status'] in (psutil.STATUS_ZOMBIE, psutil.STATUS_STOPPED, psutil.STATUS_DEAD)):
                            _proc.kill()
                    except Exception:
                        pass
            except Exception:
                pass
        try:
            log_cb(tr('opening_browser'), 'info')
            tab = await asyncio.wait_for(browser.start(), timeout=30.0)
        except asyncio.TimeoutError:
            try:
                await browser.stop()
            except Exception:
                pass
            return {'email': email, 'password': password, 'success': False}
        if headless and _PSUTIL_OK:
            if not _ghost_watcher:
                _ghost_watcher = GhostModeAPI()
            try:
                _bp = browser._browser_process_manager._process
                _browser_pid = _bp.pid if _bp else None
                if _browser_pid and _browser_pid not in _existing_opera_pids:
                    threading.Thread(target=_ghost_watcher._watch_and_hide_by_pid, args=(_browser_pid,), kwargs={'timeout': 60.0, 'interval': 0.03, 'stop_event': _watcher_stop}, daemon=True).start()
            except Exception:
                pass

        async def _safe_stop():
            try:
                _watcher_stop.set()
                await browser.stop()
            except Exception:
                pass
        try:
            log_cb(f'📧 Email: {email}', 'info')
            await self._inject_antidetect(tab)
            try:
                _ua_brand = 'Opera' if _is_opera else 'Brave' if 'brave' in (browser_path or '').lower() else 'Google Chrome'
                await tab.execute_script(f"\n                    Object.defineProperty(navigator, 'userAgentData', {{\n                        get: () => ({{\n                            brands: [\n                                {{brand: 'Chromium',     version: '124'}},\n                                {{brand: '{_ua_brand}',  version: '124'}},\n                                {{brand: 'Not-A.Brand',  version: '99'}}\n                            ],\n                            mobile: false,\n                            platform: 'Windows'\n                        }})\n                    }});\n                ")
            except Exception:
                pass
            if _is_opera and (not headless):
                _target_url = cfg['url'].lower().split('?')[0]
                _deadline, _elapsed = (30.0, 0.0)
                _found_tab = None
                while _elapsed < _deadline:
                    try:
                        for _t in await browser.get_opened_tabs():
                            try:
                                _cur = (await _t.current_url or '').lower()
                                if _target_url in _cur:
                                    _found_tab = _t
                                    break
                            except Exception:
                                pass
                        if _found_tab:
                            tab = _found_tab
                            break
                    except Exception:
                        pass
                    await asyncio.sleep(0.3)
                    _elapsed += 0.3
            elif _is_opera and headless:
                try:
                    await tab.go_to(cfg['url'])
                except Exception as _e:
                    if 'ERR_ABORTED' in str(_e) or 'net::' in str(_e):
                        _target_url = cfg['url'].lower().split('?')[0]
                        _deadline, _elapsed = (30.0, 0.0)
                        while _elapsed < _deadline:
                            await asyncio.sleep(0.3)
                            _elapsed += 0.3
                            try:
                                for _t in await browser.get_opened_tabs():
                                    try:
                                        _cur = (await _t.current_url or '').lower()
                                        if _target_url in _cur:
                                            tab = _t
                                            break
                                    except Exception:
                                        pass
                                else:
                                    continue
                                break
                            except Exception:
                                pass
                    else:
                        raise
            else:
                try:
                    await asyncio.wait_for(tab.go_to(cfg['url']), timeout=15.0)
                except asyncio.TimeoutError:
                    pass
            if headless:
                if _is_opera and _ghost_watcher:
                    _browser_pid_check = None
                    try:
                        _bp2 = browser._browser_process_manager._process
                        _browser_pid_check = _bp2.pid if _bp2 else None
                    except Exception:
                        pass
                    _confirm_deadline, _confirm_elapsed = (3.0, 0.0)
                    while _confirm_elapsed < _confirm_deadline:
                        _any_visible = False
                        if _browser_pid_check:
                            try:
                                _EnumProc2 = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
                                _vis = [False]

                                def _chk_vis(hwnd, _, _pid=_browser_pid_check):
                                    try:
                                        _pid2 = ctypes.c_ulong(0)
                                        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(_pid2))
                                        if _pid2.value == _pid and ctypes.windll.user32.IsWindowVisible(hwnd):
                                            _vis[0] = True
                                    except Exception:
                                        pass
                                    return True
                                ctypes.windll.user32.EnumWindows(_EnumProc2(_chk_vis), 0)
                                _any_visible = _vis[0]
                            except Exception:
                                pass
                        if not _any_visible:
                            break
                        await asyncio.sleep(0.1)
                        _confirm_elapsed += 0.1
                _watcher_stop.set()
            if cfg['pre_click']:
                _sel_esc = cfg['pre_click'].replace("'", "\\'")
                _deadline_pc, _elapsed_pc = (15.0, 0.0)
                while _elapsed_pc < _deadline_pc:
                    try:
                        if await tab.execute_script(f"return !!document.querySelector('{_sel_esc}');"):
                            break
                    except Exception:
                        pass
                    await asyncio.sleep(0.3)
                    _elapsed_pc += 0.3
                await tab.execute_script('window.__cfRLUnblockHandlers = true;')
                await asyncio.sleep(0.2)
                await tab.execute_script("\n                    (function() {\n                        var btn = document.querySelector('button.btn-signup-email')\n                                  || document.querySelector('#heroSocialFlow > button');\n                        if (!btn) return;\n                        var rect = btn.getBoundingClientRect();\n                        var cx = rect.left + rect.width / 2 + (Math.random() * 4 - 2);\n                        var cy = rect.top + rect.height / 2 + (Math.random() * 4 - 2);\n                        var evts = ['mouseover','mouseenter','mousemove','mousedown','mouseup','click'];\n                        var i = 0;\n                        function next() {\n                            if (i >= evts.length) return;\n                            btn.dispatchEvent(new MouseEvent(evts[i++], {\n                                bubbles: true, cancelable: true,\n                                view: window, clientX: cx, clientY: cy\n                            }));\n                            setTimeout(next, 30 + Math.random() * 60);\n                        }\n                        next();\n                    })();\n                ")
                await asyncio.sleep(cfg['pre_delay'])
                _first_sel_esc = sel['first'].replace("'", "\\'")
                _deadline_form, _elapsed_form = (15.0, 0.0)
                while _elapsed_form < _deadline_form:
                    try:
                        if await tab.execute_script(f"return !!document.querySelector('{_first_sel_esc}');"):
                            break
                    except Exception:
                        pass
                    await asyncio.sleep(0.1)
                    _elapsed_form += 0.1
            log_cb(tr('filling_form'), 'info')
            if fill_speed == 'superfast':
                import json as _json
                _fields = [(sel['first'], first_name), (sel['last'], last_name), (sel['email'], email), (sel['password'], password), (sel['confirm'], password)]
                _fill_js = ''
                for _s, _v in _fields:
                    _sel_j = _json.dumps(_s)
                    _val_j = _json.dumps(_v)
                    _fill_js += '(function(){var el=document.querySelector(' + _sel_j + ');if(el){el.value=' + _val_j + ";el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}})();"
                await tab.execute_script(_fill_js)
                await asyncio.sleep(0.05 + random.random() * 0.1)
                await self.fill_field_instantly(tab, sel['first'], first_name)
                await self.fill_field_instantly(tab, sel['last'], last_name)
                await self.fill_field_instantly(tab, sel['email'], email)
                await self.fill_field_instantly(tab, sel['password'], password)
                await self.fill_field_instantly(tab, sel['confirm'], password)
            else:
                delay = 0.05 if fill_speed == 'fast' else 0.2
                await self.fill_field_instantly(tab, sel['first'], first_name)
                await asyncio.sleep(delay + random.random() * 0.15)
                await self.fill_field_instantly(tab, sel['last'], last_name)
                await asyncio.sleep(delay + random.random() * 0.15)
                await self.fill_field_instantly(tab, sel['email'], email)
                await asyncio.sleep(delay + random.random() * 0.15)
                await self.fill_field_instantly(tab, sel['password'], password)
                await asyncio.sleep(delay + random.random() * 0.15)
                await self.fill_field_instantly(tab, sel['confirm'], password)
            await asyncio.sleep(0.2)
            await tab.execute_script(f"document.querySelector('{sel['tos']}').click();")
            log_cb(tr('waiting_captcha'), 'warning')
            await asyncio.sleep(5)
            log_cb(tr('submitting_form'), 'info')
            _submit_fn = cfg.get('submit_fn')
            if _submit_fn:
                await tab.execute_script(f"document.querySelector('#registerButton').click();")
                await asyncio.sleep(0.5)
                await tab.execute_script(f"if(typeof {_submit_fn}==='function') {_submit_fn}('dummy-token');")
            else:
                await tab.execute_script("document.querySelector('#registerButton').click();")
            _post_submit_deadline = asyncio.get_event_loop().time() + 15
            while asyncio.get_event_loop().time() < _post_submit_deadline:
                await asyncio.sleep(0.4)
                _url_now = None
                try:
                    _url_now = await tab.execute_script('return window.location.href;')
                    if isinstance(_url_now, dict):
                        try:
                            _url_now = _url_now['result']['result']['value']
                        except (KeyError, TypeError):
                            _url_now = None
                except Exception:
                    pass
                _url_now = str(_url_now or '').lower()
                _success_url_cfg = cfg.get('success_url', '').lower()
                if _success_url_cfg and _success_url_cfg in _url_now:
                    break
                if any((k in _url_now for k in ('success', 'account_created', 'register-success', 'signup-complete'))):
                    break
                _err_quick = None
                try:
                    _err_quick = await tab.execute_script('\n                        const s=[\'.alert-danger\',\'[class*="invalid-feedback"]\',\n                                 \'[class*="error-msg"]\',\'[class*="alert-error"]\'];\n                        for(const sel of s){const e=document.querySelector(sel);\n                        if(e&&e.offsetParent!==null&&e.textContent.trim())return e.textContent.trim();}\n                        return null;\n                    ')
                    if isinstance(_err_quick, dict):
                        try:
                            _err_quick = _err_quick['result']['result']['value']
                        except (KeyError, TypeError):
                            _err_quick = None
                except Exception:
                    pass
                if _err_quick and str(_err_quick).strip() not in (None, 'None', ''):
                    break

            def _extract(result):
                if isinstance(result, dict):
                    try:
                        return result['result']['result']['value']
                    except (KeyError, TypeError):
                        return None
                return result
            current_url = _extract(await tab.execute_script('return window.location.href;'))
            page_body_txt = _extract(await tab.execute_script("return document.body ? document.body.innerText : '';"))
            error_text = _extract(await tab.execute_script('\n                const errorSelectors = [\'.alert-danger\', \'[data-error]\',\n                    \'[class*="invalid-feedback"]\', \'.form-error\',\n                    \'[class*="error-msg"]\', \'[class*="alert-error"]\'];\n                for (const sel of errorSelectors) {\n                    const error = document.querySelector(sel);\n                    if (error && error.offsetParent !== null && error.textContent.trim()) {\n                        return error.textContent.trim();\n                    }\n                }\n                return null;\n            '))
            success_el = _extract(await tab.execute_script('\n                const s = document.querySelector(\n                    \'.success, .alert-success, [class*="success"], [class*="thank"],\' +\n                    \'[class*="confirm"], [class*="complete"], [class*="registered"],\' +\n                    \'[id*="success"], [id*="confirm"], [id*="complete"]\'\n                );\n                return s ? s.textContent.trim() : null;\n            '))
            error_text = str(error_text).strip() if error_text not in (None, 'None', '') else None
            success_el = str(success_el).strip() if success_el not in (None, 'None', '') else None
            current_url = str(current_url) if current_url else ''
            page_body_txt = str(page_body_txt).lower() if page_body_txt else ''
            ERROR_BODY_KEYWORDS = ('invalid email', 'email already', 'already registered', 'already in use', 'email taken', 'this email is', 'password is too', 'password must', 'senha inválida', 'e-mail já', 'email já', 'já cadastrado', 'captcha', 'robot', 'automated', 'unusual traffic', 'too many requests', 'rate limit', 'blocked')
            hard_error = bool(error_text)
            body_error = any((k in page_body_txt for k in ERROR_BODY_KEYWORDS))
            if hard_error or body_error:
                _err_reason = error_text or next((k for k in ERROR_BODY_KEYWORDS if k in page_body_txt), 'unknown error')
                if any((k in _err_reason.lower() for k in ('captcha', 'robot', 'automated'))):
                    log_cb(f'✗ {tr('captcha_failed')}', 'error')
                else:
                    log_cb(f'✗ {tr('error_fill_form').format(e=_err_reason)}', 'error')
                if close_after:
                    await _safe_stop()
                return {'email': email, 'password': password, 'success': False}
            _success_url = cfg.get('success_url', '').lower()
            _success_txt = cfg.get('success_txt', '').lower()
            url_lower = current_url.lower()
            body_lower = page_body_txt.lower()
            exact_url = bool(_success_url and _success_url in url_lower)
            exact_txt = bool(_success_txt and _success_txt in body_lower)
            has_success_el = bool(success_el)
            FALLBACK_BODY = ('thank you for registering', 'thank you for signing up', 'successfully created', 'account created', 'registration complete', 'registration successful', 'bem-vindo', 'cadastro realizado com sucesso')
            FALLBACK_URL = ('account_created', 'registration-success', 'signup-complete', 'register-success')
            fallback_body = any((k in body_lower for k in FALLBACK_BODY))
            fallback_url = any((k in url_lower for k in FALLBACK_URL))
            success = exact_url or exact_txt or has_success_el or fallback_body or fallback_url
            if success:
                log_cb(f'✓ {tr('registration_success')}', 'success')
            else:
                log_cb(f'✗ {tr('step_failed')}', 'error')
            if close_after:
                try:
                    if success and close_after_delay > 0:
                        await asyncio.sleep(close_after_delay)
                    await _safe_stop()
                except Exception:
                    pass
            return {'email': email, 'password': password, 'success': success}
        except Exception as e:
            log_cb(f'✗ {tr('error_fill_form').format(e=str(e)[:80])}', 'error')
            await _safe_stop()
            return {'email': email, 'password': password, 'success': False}

def check_for_updates():
    console.print(f'[cyan]{tr('checking_updates')}[/cyan]')
    old_exe = os.path.join(get_base(), 'mainrev-lite_old.exe')
    if os.path.exists(old_exe):
        try:
            os.remove(old_exe)
        except Exception:
            pass
    remote_version = get_remote_version()
    if remote_version is None:
        console.print(f'[yellow]{tr('update_check_failed')}[/yellow]')
        return
    local_version = get_local_version()
    if remote_version == local_version:
        console.print(f'[green]{tr('up_to_date').format(local_version=local_version)}[/green]')
        return
    console.print(f'\n[bold cyan]{'=' * 50}[/bold cyan]')
    console.print(f'[bold yellow]{tr('update_available')}[/bold yellow]')
    console.print(f'[cyan]{tr('current_version').format(local_version=local_version)}[/cyan]')
    console.print(f'[cyan]{tr('new_version').format(remote_version=remote_version)}[/cyan]')
    console.print(f'[bold cyan]{'=' * 50}[/bold cyan]')
    console.print(f'[yellow]{tr('update_downloading')}[/yellow]\n')
    base = get_base()
    success = True
    if getattr(sys, 'frozen', False):
        new_exe_path = os.path.join(base, 'mainrev-lite_new.exe')
        ok = download_file('https://github.com/TDoomX/exitlag-auto-signup-revamp-lite/releases/latest/download/mainrev-lite.exe', new_exe_path)
        if not ok:
            success = False
    ok = download_file(f'{GITHUB_RAW}/main_lite.py', os.path.join(base, 'main_lite.py'))
    if not ok:
        success = False
    os.makedirs(os.path.join(base, 'translations'), exist_ok=True)
    for lang in TRANSLATIONS_LANGS:
        ok = download_file(f'{GITHUB_RAW}/translations/{lang}.json', os.path.join(base, 'translations', f'{lang}.json'))
        if not ok:
            success = False
    ok = download_file(f'{GITHUB_RAW}/version.txt', os.path.join(base, 'version.txt'))
    if not ok:
        success = False
    if not success:
        console.print(f'\n[bold red]{tr('update_partial_fail')}[/bold red]')
        return
    console.print(f'\n[bold green]{tr('update_complete')}[/bold green]')
    console.print(f'[bold yellow]{tr('update_reopening')}[/bold yellow]\n')
    skip = threading.Event()

    def wait_for_enter():
        input()
        skip.set()
    threading.Thread(target=wait_for_enter, daemon=True).start()
    for i in range(5, 0, -1):
        if skip.is_set():
            break
        console.print(f'[cyan]{tr('update_countdown').format(i=i)}[/cyan]', end='\r')
        time.sleep(1)
    console.print()
    if getattr(sys, 'frozen', False):
        exe_path = os.path.join(base, 'mainrev-lite.exe')
        new_exe = os.path.join(base, 'mainrev-lite_new.exe')
        bat_path = os.path.join(base, 'update.bat')
        bat_content = f'@echo off\r\ntimeout /t 2 /nobreak > nul\r\nmove /y "{new_exe}" "{exe_path}"\r\nexplorer.exe "{exe_path}"\r\ndel "%~f0"\r\n'
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        subprocess.Popen(bat_path, shell=True)
        time.sleep(0.5)
    else:
        subprocess.Popen([sys.executable, os.path.join(base, 'main_lite.py')])
    sys.exit(0)
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
_PROGRESS_STEPS = 5
_STEP_MAP = {'opening_browser': 0, 'email': 1, 'filling_form': 2, 'waiting_captcha': 3, 'submitting_form': 4}
_progress_ctx = None
_progress_task = None

def _progress_start(label: str):
    global _progress_ctx, _progress_task
    _progress_stop()
    _progress_ctx = Progress(SpinnerColumn(style='cyan'), TextColumn('[bold cyan]{task.description}'), BarColumn(bar_width=30, complete_style='cyan', finished_style='green'), TextColumn('[cyan]{task.completed}/{task.total}'), console=console, transient=False, refresh_per_second=10)
    _progress_ctx.start()
    _progress_task = _progress_ctx.add_task(label, total=_PROGRESS_STEPS)

def _progress_stop():
    global _progress_ctx, _progress_task
    if _progress_ctx is not None:
        try:
            _progress_ctx.stop()
        except Exception:
            pass
        _progress_ctx = None
        _progress_task = None

def log_cb(msg: str, level: str='info'):
    global _progress_ctx, _progress_task
    step_key = None
    if tr('opening_browser') in msg:
        step_key = 'opening_browser'
    elif msg.startswith('📧'):
        step_key = 'email'
    elif tr('filling_form') in msg:
        step_key = 'filling_form'
    elif tr('waiting_captcha') in msg:
        step_key = 'waiting_captcha'
    elif tr('submitting_form') in msg:
        step_key = 'submitting_form'
    if step_key is not None and _progress_ctx is not None and (_progress_task is not None):
        step_num = _STEP_MAP[step_key]
        _progress_ctx.update(_progress_task, description=msg[:55], completed=step_num + 1)
        return
    if level in ('success', 'error') or _progress_ctx is None:
        _progress_stop()
    colors = {'info': 'cyan', 'success': 'green', 'warning': 'yellow', 'error': 'red'}
    color = colors.get(level, 'white')
    console.print(f'[{color}]{msg}[/{color}]')

def display_accounts(accounts):
    successful = [a for a in accounts if a['success']]
    if not successful:
        return
    console.print(f'\n[bold cyan]{'=' * 50}[/bold cyan]')
    console.print(f'[bold cyan]{tr('accounts_created')}[/bold cyan]')
    console.print(f'[bold cyan]{'=' * 50}[/bold cyan]')
    for acc in successful:
        console.print(f'[cyan]{tr('email_label')} {acc['email']}[/cyan]')
        console.print(f'[cyan]{tr('password_display_label')} {acc['password']}[/cyan]')
        console.print('')
    console.print(f'[bold cyan]{'=' * 50}[/bold cyan]\n')

async def run_accounts(plan_key, passw, count, browser_path, headless=False, close_after=True, close_after_delay=5, fill_speed='slow'):
    cfg = PLAN_CONFIGS[plan_key]
    automation = BrowserAutomation(cfg)
    accounts = []
    for x in range(count):
        console.print(f'\n[bold cyan]{'─' * 40}[/bold cyan]')
        console.print(f'[bold cyan]{tr('account_counter').format(x=x + 1, count=count)}[/bold cyan]')
        console.print(f'[bold cyan]{'─' * 40}[/bold cyan]')
        _progress_start(tr('signup_process'))
        result = await automation.register_account(passw, browser_path, log_cb, headless=headless, close_after=close_after, close_after_delay=close_after_delay, fill_speed=fill_speed)
        accounts.append(result)
        if x < count - 1:
            delay = random.uniform(5, 10)
            console.print(f'[yellow]{tr('waiting_next_account').format(delay=int(delay))}[/yellow]')
            await asyncio.sleep(delay)
    with open(os.path.join(get_base(), 'accounts.txt'), 'a') as f:
        for acc in accounts:
            if acc['success']:
                f.write(f'{acc['email']} | {acc['password']}\n')
    successful = sum((1 for a in accounts if a['success']))
    console.print(f'\n[bold cyan]{'=' * 50}[/bold cyan]')
    console.print(f'[bold green]✓ {tr('successfully_created_account').format(x=successful, executionCount=count)}[/bold green]')
    console.print(f'[bold green]{tr('credentials_saved')}[/bold green]')
    console.print(f'[bold cyan]{'=' * 50}[/bold cyan]')
    display_accounts(accounts)

async def main():
    check_for_updates()
    while True:
        last_config = load_config()
        browser_path = ''
        passw = ''
        proxy = ''
        execution_count = 1
        escolha_plano = '1'
        fill_speed = 'slow'
        silent = False
        close_after = True
        if last_config:
            console.print(f'\n[bold cyan]{'=' * 50}[/bold cyan]')
            console.print(f'[bold cyan]{tr('last_config_found')}[/bold cyan]')
            console.print(f'[bold cyan]{'=' * 50}[/bold cyan]')
            console.print(f'[cyan]{tr('browser_label')} {last_config.get('browser_path', tr('default_browser'))}[/cyan]')
            console.print(f'[cyan]{tr('password_label_display')} {last_config.get('password', '')}[/cyan]')
            console.print(f'[cyan]{tr('proxy_label_display')} {last_config.get('proxy', tr('no_proxy'))}[/cyan]')
            console.print(f'[cyan]{tr('accounts_label')} {last_config.get('execution_count', 1)}[/cyan]')
            plan_name = tr('seven_days') if last_config.get('plan') == '2' else tr('three_days')
            console.print(f'[cyan]{tr('plan_label')} {plan_name}[/cyan]')
            _speed_map = {'slow': tr('fill_speed_slow'), 'fast': tr('fill_speed_fast'), 'superfast': tr('fill_speed_superfast')}
            console.print(f'[cyan]{tr('fill_speed_label')} {_speed_map.get(last_config.get('fill_speed', 'slow'), last_config.get('fill_speed', 'slow'))}[/cyan]')
            console.print(f'[cyan]{(tr('menu_silent_on') if last_config.get('silent') else tr('menu_silent_off'))}[/cyan]')
            console.print(f'[cyan]{(tr('menu_close_after_on') if last_config.get('close_after', True) else tr('menu_close_after_off'))}[/cyan]')
            console.print(f'[bold cyan]{'=' * 50}[/bold cyan]\n')
            use_last = input(tr('use_last_config_prompt')).strip().lower()
            if use_last in ('y', 's', 'o', 'j', 'д'):
                browser_path = last_config.get('browser_path', '')
                passw = last_config.get('password', '')
                proxy = last_config.get('proxy', '')
                execution_count = last_config.get('execution_count', 1)
                escolha_plano = last_config.get('plan', '1')
                fill_speed = last_config.get('fill_speed', 'slow')
                silent = last_config.get('silent', False)
                close_after = last_config.get('close_after', True)
            else:
                last_config = None
        if not last_config:
            while True:
                browser_path = input(f'\n{tr('browser_path_info')}\n{tr('supported_browsers')}\n{tr('browser_executable_path')}').replace('"', '').replace("'", '')
                if browser_path == '' or os.path.exists(browser_path):
                    break
                console.print(f'[bold red]{tr('invalid_path')}[/bold red]')
            while True:
                passw = input(f'\n{tr('password_info')}\n{tr('password_label')}')
                if passw == '':
                    passw = generate_random_password()
                    console.print(f'[bold green]{tr('random_password_generated').format(passw=passw)}[/bold green]')
                    break
                if not is_valid_password(passw):
                    console.print(f'[bold red]{tr('password_not_meeting_requirements')}[/bold red]')
                    continue
                break
            proxy = input(f'\n{tr('proxy_info')}\n{tr('proxy_label')}: ')
            while True:
                raw = input(f'\n{tr('number_of_accounts_prompt')}')
                try:
                    execution_count = int(raw) if raw.strip() else 1
                    break
                except ValueError:
                    console.print(f'[bold red]{tr('invalid_number')}[/bold red]')
            console.print(f'\n{tr('plan_selection_title')}', style='bold cyan')
            console.print(f'1 - {tr('plan_option_3days')}')
            console.print(f'2 - {tr('plan_option_7days')}')
            escolha_plano = (await asyncio.to_thread(input, tr('plan_input_prompt'))).strip() or '1'
            if escolha_plano not in ('1', '2'):
                escolha_plano = '1'
            console.print(f'\n[bold cyan]{tr('fill_speed_label')}[/bold cyan]')
            console.print(f'1 - {tr('fill_speed_slow')}')
            console.print(f'2 - {tr('fill_speed_fast')}')
            console.print(f'3 - {tr('fill_speed_superfast')}')
            _speed_raw = (await asyncio.to_thread(input, tr('fill_speed_prompt'))).strip() or '1'
            fill_speed = {'1': 'slow', '2': 'fast', '3': 'superfast'}.get(_speed_raw, 'slow')
            _silent_raw = (await asyncio.to_thread(input, f'\n{tr('silent_mode_prompt')}')).strip().lower()
            silent = _silent_raw in ('y', 's')
            _close_raw = (await asyncio.to_thread(input, f'\n{tr('close_after_prompt')}')).strip().lower()
            close_after = _close_raw not in ('n', 'no', 'não', 'nao', 'нет', 'non', 'nein', 'لا', 'không')
            save_config(browser_path, passw, proxy, execution_count, escolha_plano, fill_speed, silent, close_after)
        plan_label = tr('seven_days') if escolha_plano == '2' else tr('three_days')
        console.print(f'\n[bold cyan]{tr('account_generation_process')} - {plan_label}[/bold cyan]\n')
        await run_accounts(plan_key=escolha_plano, passw=passw, count=execution_count, browser_path=browser_path, headless=silent, close_after=close_after, close_after_delay=3, fill_speed=fill_speed)
        console.print(f'\n[bold cyan]{'─' * 50}[/bold cyan]\n')
if __name__ == '__main__':
    asyncio.run(main())