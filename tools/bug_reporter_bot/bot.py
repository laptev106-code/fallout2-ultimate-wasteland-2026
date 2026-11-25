"""
Fallout 2: Ultimate Wasteland Edition (2026) — Telegram Bug Reporter Bot.
Zero external dependencies (uses Python stdlib urllib + json).
Collects bug reports, screenshots, and logs (sfall-log.txt, debug.log),
saves them locally to bugs_inbox/, and forwards them to ADMIN_CHAT_ID.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
INBOX_DIR = BASE_DIR.parent.parent / "bugs_inbox"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Не найден {CONFIG_PATH}. Скопируйте config.example.json в config.json и впишите токен.")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if not cfg.get("bot_token") or "PUT_YOUR_TOKEN" in cfg["bot_token"]:
        print("[ERROR] В config.json не указан рабочий bot_token от @BotFather.")
        sys.exit(1)
    return cfg


def tg_request(token: str, method: str, payload: dict | None = None, timeout: int = 35) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_message(token: str, chat_id: int, text: str) -> None:
    try:
        tg_request(token, "sendMessage", {"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"[WARN] Ошибка отправки сообщения в {chat_id}: {e}")


def forward_message(token: str, to_chat_id: int, from_chat_id: int, message_id: int) -> None:
    try:
        tg_request(
            token,
            "forwardMessage",
            {"chat_id": to_chat_id, "from_chat_id": from_chat_id, "message_id": message_id},
        )
    except Exception as e:
        print(f"[WARN] Ошибка пересылки сообщения {message_id}: {e}")


def save_report_locally(msg: dict) -> Path:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    user = msg.get("from", {})
    username = user.get("username") or f"id_{user.get('id', 'unknown')}"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = INBOX_DIR / f"bug_{ts}_{username}.txt"

    lines = [
        f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"От: {user.get('first_name', '')} {user.get('last_name', '')} (@{user.get('username', 'none')}, id={user.get('id')})",
        f"Chat ID: {msg.get('chat', {}).get('id')}",
        "-" * 50,
        msg.get("text") or msg.get("caption") or "[Без текста — приложен медиафайл/документ]",
        "",
    ]
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_file


def handle_update(token: str, admin_chat_id: int | None, update: dict) -> None:
    msg = update.get("message")
    if not msg:
        return

    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    if text.startswith("/start"):
        welcome = (
            "Терминал приема баг-репортов Fallout 2: Ultimate Wasteland Edition (2026).\n\n"
            "Отправьте сюда:\n"
            "1. Отчет из лаунчера (кнопка «Скопировать отчет» -> вставьте сюда).\n"
            "2. Описание проблемы: локация, профиль (Gameplay или HD), что именно сломалось.\n"
            "3. При желании прикрепите скриншот или файлы sfall-log.txt / debug.log.\n\n"
            "Все обращения сразу попадают разработчику."
        )
        send_message(token, chat_id, welcome)
        return

    if text.startswith("/help"):
        send_message(
            token,
            chat_id,
            "Просто напишите описание бага одним сообщением или прикрепите скриншот/лог. "
            "Команда /start покажет памятку.",
        )
        return

    saved_path = save_report_locally(msg)
    print(f"[REPORT] Сохранен: {saved_path.name}")

    if admin_chat_id and chat_id != admin_chat_id:
        forward_message(token, admin_chat_id, chat_id, msg["message_id"])

    send_message(
        token,
        chat_id,
        "Принято. Отчет записан и передан разработчику. Спасибо за помощь в полировке сборки.",
    )


def main() -> None:
    cfg = load_config()
    token = cfg["bot_token"]
    admin_chat_id = cfg.get("admin_chat_id")
    offset = 0

    print("[BOT] Запуск long-polling...")
    while True:
        try:
            res = tg_request(token, "getUpdates", {"offset": offset, "timeout": 25}, timeout=35)
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                handle_update(token, admin_chat_id, upd)
        except urllib.error.HTTPError as e:
            print(f"[HTTP ERROR] {e.code}: {e.reason}")
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
