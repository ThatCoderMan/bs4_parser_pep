# Парсер Python.org

## Описание

Данный код представляет собой парсер документации Python. Он предоставляет возможность получить информацию о новых версиях Python, скачать архив с документацией, получить информацию о PEP (Python Enhancement Proposal) и их статусах.

## Установка

Для корректной работы парсера необходимо активировать вертуальное окружение.

для Linux/MacOS
```
source venv/bin/activate
```
для Windows
```
venv\Scripts\activate
```

После необходимо установить зависимости, указанные в файле `requirements.txt`. Для этого необходимо выполнить следующую команду:

```
pip install -r requirements.txt
```

## Использование

Для запуска парсера необходимо выполнить команду:

```
python main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
```

Позиционный аргумент - один из режимов работы парсера (`whats-new`, `latest-versions`, `download`, `pep`), 

`-c`, `--clear-cache` - флаг для очистки кэша запросов, 

`-o`, `--output-format` - формат вывода результата (`pretty` или `file`), 

Примеры запуска:

```
python parser.py whats-new --output-format table
python parser.py latest-versions --output-format pretty 
python parser.py download --clear-cache
python parser.py pep
```

### Автор проекта:

[Artemii Berezin](https://github.com/ThatCoderMan)

