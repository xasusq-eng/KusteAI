# KusteAI

KusteAI — персональный ИИ-ассистент на русском языке с:

- интернет-поиском;
- подключением к готовой LLM (OpenAI-compatible API);
- памятью в SQLite;
- управлением Android через ADB;
- защитой от опасных удалений/деинсталляции без PIN владельца.

## 1) Установка (Linux / Termux)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Для **Termux** можно использовать готовый скрипт:

```bash
bash scripts_termux_setup.sh
```

## 2) Настройка

```bash
cp .env.example .env
```

Обязательно задайте:

- `KUSTEAI_API_KEY`
- `KUSTEAI_BASE_URL`
- `KUSTEAI_MODEL`
- `KUSTEAI_OWNER_PIN` (PIN владельца для разрешения опасных ADB-команд)

## 3) Запуск

```bash
python main.py
```

## Команды

- `текст` — обычный диалог с ИИ;
- `/search <запрос>` — поиск в интернете;
- `/remember <факт>` — сохранить факт в долгую память;
- `/memories` — показать последние факты;
- `/adb <shell-команда>` — выполнить `adb shell <команда>`;
- `/approve <PIN>` — одноразово разрешить опасную ADB-команду;
- `/exit` — выйти.

## Защита от удаления/опасных действий

KusteAI блокирует потенциально опасные команды (например `rm`, `pm uninstall`, `mkfs`, `dd`, `reboot`) до подтверждения владельцем.

Поток работы:

1. Ввести опасную команду `/adb ...`.
2. KusteAI попросит подтверждение `/approve <PIN>`.
3. Повторно выполнить команду — разрешение одноразовое.

Это дает **полный доступ для управления устройством**, но с защитой от случайного или несанкционированного удаления.

## Файлы проекта

- `main.py` — CLI;
- `kusteai/agent.py` — логика ассистента;
- `kusteai/adb_bridge.py` — выполнение ADB-команд;
- `kusteai/security.py` — защитный слой для опасных команд;
- `kusteai/memory.py` — SQLite-память;
- `kusteai/search.py` — веб-поиск;
- `tests/` — автотесты.
