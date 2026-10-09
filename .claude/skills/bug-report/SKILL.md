---
name: bug-report
description: Оформляет баг LMS API по шаблону и заводит его в GitHub Issues после подтверждения. Вызов /bug-report <описание проблемы>.
---
Проблема: $ARGUMENTS

1. Воспроизведи через curl или минимальный pytest-тест; сохрани точный запрос и ответ.
2. Заполни `templates/bug.md`. Заголовок: `[<Сущность>] <что не так> при <условии>`.
3. Найди дубли: `gh issue list --state all --label bug --search "<ключевые слова>"`.
4. Покажи черновик и дождись «да».
5. `gh issue create --title "..." --body-file <файл> --label bug` — верни ссылку.
6. Если есть падающий автотест — предложи пометить его `@pytest.mark.xfail(reason="#<номер>", strict=True)`.
