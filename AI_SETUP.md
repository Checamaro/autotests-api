# Настройка ИИ-конвейера тестирования (Windows)

Скопируйте содержимое архива в корень `autotests-api` (с сохранением папок).

## 1. Сервисы (бесплатно)
| Роль | Сервис | Что сделать |
|---|---|---|
| TMS | Qase, Free-план | Зарегистрироваться на qase.io, создать проект с кодом **LMS**, в профиле → API tokens создать токен |
| Баг-трекер | GitHub Issues | В репозитории создать метки: `bug`, `ai-triage`, `flaky`, `test-issue` |
| CI | GitHub Actions | Уже есть `tests.yml`; добавляется `ai-triage.yml` |
| Отчёты | Allure на GitHub Pages | Уже настроено |

## 2. Программы
```powershell
winget install Git.Git GitHub.cli OpenJS.NodeJS.LTS Python.Python.3.12
irm https://claude.ai/install.ps1 | iex      # Claude Code
gh auth login                                  # вход в GitHub для gh
setx QASE_API_TOKEN "ваш_токен_qase"          # перезапустите терминал после setx
```
Сервер для тестов — по README `qa-automation-engineer-api-course`, клонируйте его рядом:
`..\qa-automation-engineer-api-course` (requirements-analyst будет читать его код).

## 3. Связка тестов с Qase
```powershell
pip install qase-pytest
```
Добавьте `qase-pytest` в requirements.txt. В тестах: `from qase.pytest import qase` и `@qase.id(N)`.
Отправка результатов прогона в Qase (локально или в CI):
```powershell
$env:QASE_MODE="testops"; $env:QASE_TESTOPS_PROJECT="LMS"; $env:QASE_TESTOPS_API_TOKEN=$env:QASE_API_TOKEN
pytest -m regression
```
В CI — те же переменные в шаге pytest, токен в секрете `QASE_API_TOKEN`.

## 4. ИИ-разбор в CI
```powershell
claude setup-token          # выдаст токен для подписки
gh secret set CLAUDE_CODE_OAUTH_TOKEN
```
Также один раз выполните в Claude Code `/install-github-app` — он поставит GitHub App Claude на репозиторий.

## 5. Проверка
```powershell
cd autotests-api
claude
/mcp                         # qase должен быть connected
/agents                      # 4 субагента
```
Первый прогон конвейера: `/qa-pipeline courses`
