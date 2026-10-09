"""
Сводка упавших тестов из allure-results для анализа ИИ-агентом.

Зачем: сырые allure-results — это десятки JSON и вложений. Агенту дешевле и точнее
читать одну компактную сводку: имя теста, статус, сообщение, начало трейса и curl-вложение.

Использование:
    python tools/ai/summarize_allure.py allure-results [--json]
"""
import json
import sys
from collections import Counter
from pathlib import Path

TRACE_LINES = 25          # сколько строк трейса оставлять
ATTACH_CHARS = 1500       # сколько символов вложения (curl/ответ) оставлять


def read_attachments(results_dir: Path, item: dict) -> list[str]:
    """Собирает текстовые вложения из теста и его шагов (там лежат curl-команды)."""
    out = []
    stack = [item]
    while stack:
        node = stack.pop()
        for att in node.get("attachments", []):
            path = results_dir / att.get("source", "")
            if path.suffix in {".txt", ".json", ".log", ""} and path.exists():
                text = path.read_text(encoding="utf-8", errors="replace")
                out.append(f"[{att.get('name', 'attachment')}]\n{text[:ATTACH_CHARS]}")
        stack.extend(node.get("steps", []))
    return out


def failed_step(item: dict) -> str | None:
    """Находит первый упавший шаг — обычно это конкретная проверка."""
    for step in item.get("steps", []):
        if step.get("status") in {"failed", "broken"}:
            return failed_step(step) or step.get("name")
    return None


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    results_dir = Path(sys.argv[1])
    as_json = "--json" in sys.argv

    # При перезапусках (rerun) один тест имеет несколько результатов — берём последний по времени
    latest: dict[str, dict] = {}
    for f in results_dir.glob("*-result.json"):
        item = json.loads(f.read_text(encoding="utf-8"))
        key = item.get("historyId") or item.get("fullName")
        if key not in latest or item.get("stop", 0) > latest[key].get("stop", 0):
            latest[key] = item

    statuses = Counter(i.get("status") for i in latest.values())
    failures = []
    for item in latest.values():
        if item.get("status") not in {"failed", "broken"}:
            continue
        details = item.get("statusDetails", {})
        failures.append({
            "test": item.get("fullName"),
            "title": item.get("name"),
            "status": item.get("status"),
            "failed_step": failed_step(item),
            "message": (details.get("message") or "").strip(),
            "trace": "\n".join((details.get("trace") or "").splitlines()[-TRACE_LINES:]),
            "attachments": read_attachments(results_dir, item),
        })

    if as_json:
        print(json.dumps({"statuses": statuses, "failures": failures}, ensure_ascii=False, indent=2))
        return

    print("Итог: " + ", ".join(f"{k}={v}" for k, v in sorted(statuses.items())))
    for n, f in enumerate(failures, 1):
        print(f"\n=== {n}. {f['test']} [{f['status']}]")
        print(f"Шаг: {f['failed_step']}")
        print(f"Сообщение: {f['message']}")
        print(f"Трейс (конец):\n{f['trace']}")
        for att in f["attachments"]:
            print(att)


if __name__ == "__main__":
    main()
