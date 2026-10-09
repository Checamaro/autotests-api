#!/usr/bin/env bash
# Генерация Allure-отчёта с историей для публикации на GitHub Pages.
# Ожидает: allure-results/ (результаты прогона), gh-pages/ (checkout ветки gh-pages, может отсутствовать).
# Результат: allure-history/ — содержимое для деплоя в gh-pages.
set -euo pipefail

mkdir -p allure-history gh-pages

# Переносим ранее опубликованные отчёты (только папки с номерами прогонов и историю трендов)
for d in gh-pages/[0-9]* gh-pages/last-history; do
  [ -d "$d" ] && cp -r "$d" allure-history/
done

# История трендов из прошлого прогона
if [ -d gh-pages/last-history ]; then
  mkdir -p allure-results/history
  cp -r gh-pages/last-history/. allure-results/history/
fi

# Ссылка на прогон в шапке отчёта
cat > allure-results/executor.json <<JSON
{"name":"GitHub Actions","type":"github","reportName":"Allure Report with history",
 "url":"${PAGES_URL}","reportUrl":"${PAGES_URL}/${RUN_NUMBER}",
 "buildUrl":"${BUILD_URL}","buildName":"GitHub Actions Run #${RUN_NUMBER}","buildOrder":"${RUN_NUMBER}"}
JSON

allure generate --clean allure-results -o allure-report

rm -rf "allure-history/${RUN_NUMBER}" allure-history/last-history
cp -r allure-report "allure-history/${RUN_NUMBER}"
cp -r allure-report/history allure-history/last-history

# Оставляем только последние KEEP_REPORTS отчётов
ls -d allure-history/[0-9]* | sort -t/ -k2 -n | head -n -"${KEEP_REPORTS}" | xargs -r rm -rf

# Корневая страница перенаправляет на свежий отчёт
echo "<!DOCTYPE html><meta charset=\"utf-8\"><meta http-equiv=\"refresh\" content=\"0; URL=${PAGES_URL}/${RUN_NUMBER}/index.html\">" > allure-history/index.html
echo "Отчёт: ${PAGES_URL}/${RUN_NUMBER}/"
