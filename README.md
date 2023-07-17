# Парсер Python.org
![workflows](https://github.com/ThatCoderMan/bs4_parser_pep/actions/workflows/workflow.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.10
- BeautifulSoup4
- lxml
- argparse
- logging
- GitHub Actions

</details>

## Описание

Данный код представляет собой парсер документации Python. Он предоставляет возможность получить информацию о новых версиях Python, скачать архив с документацией, получить информацию о PEP (Python Enhancement Proposal) и их статусах.

## Установка
Клонируйте репозиторий:
```commandline
git clone git@github.com:ThatCoderMan/bs4_parser_pep.git
```
Активируйте вертуальное окружение:
- для Linux/MacOS
  ```commandline
  source venv/bin/activate
  ```
- для Windows
  ```commandline
  venv\Scripts\activate
  ```

Установите зависимости, указанные в файле `requirements.txt`:
```commandline
pip install -r requirements.txt
```
Перейти в папку `src`:
```commandline
cd src
```

## Использование

Для запуска парсера необходимо выполнить команду:
```commandline
python main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
```
Позиционный аргумент - один из режимов работы парсера (`whats-new`, `latest-versions`, `download`, `pep`)
- **whats-new**

  Парсинг последних обновлений с сайта
  ```commandline
  python main.py whats-new <args>
  ```
  
- **latest-versions**

  Парсинг последних версий документации
  ```commandline
  python main.py latest_versions <args>
  ```
  
- **download**

  Загрузка и сохранение архива с документацией
  ```commandline
  python main.py download <args>
  ```
  
- **pep**

  Парсинг статусов PEP
  ```commandline
  python main.py pep <args>
  ```

`-h`, `-help` - вывести информацию о парсере

`-c`, `--clear-cache` - флаг для очистки кэша запросов

`-o`, `--output-format` - формат вывода результата (`pretty` - в табличном формате в консоли или `file` - в CSV файл)

## Примеры запуска:

```
python parser.py whats-new --output-format table
python parser.py latest-versions --output-format pretty 
python parser.py download --clear-cache
python parser.py pep
```

### Автор проекта:

[Artemii Berezin](https://github.com/ThatCoderMan)

