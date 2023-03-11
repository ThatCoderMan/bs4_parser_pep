import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, MAIN_PEP_URL,
                       STATUS_WARNING)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python, desc='Whats new'):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    pat = r'.+pdf-a4\.zip$'
    archive = find_tag(soup, 'a', {'href': re.compile(pat)})
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_url = urljoin(downloads_url, archive['href'])
    archive_path = downloads_dir / archive_url.split('/')[-1]
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, MAIN_PEP_URL)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    section = find_tag(soup, 'section', {'id': 'index-by-category'})
    tbodys_from_section = section.find_all('tbody')
    results = {}
    for table in tqdm(tbodys_from_section, desc='Sections'):
        rows = table.find_all('tr')
        for row in rows:
            abbr = find_tag(row, 'abbr').text[1:]
            general_status = EXPECTED_STATUS[abbr]
            pep_link = urljoin(MAIN_PEP_URL, find_tag(row, 'a')['href'])
            response = get_response(session, pep_link)
            if response is None:
                continue
            soup = BeautifulSoup(response.text, features='lxml')
            pep_info = find_tag(
                soup,
                'dl',
                {'class': 'rfc2822 field-list simple'}
            )
            pep_info_items = pep_info.find_all()
            for row_info in pep_info_items:
                if row_info.text == 'Status:':
                    status = row_info.find_next_sibling().text
                    break
            else:
                status = None
            if status not in general_status:
                logging.warning(STATUS_WARNING.format(
                    link=pep_link,
                    status=status,
                    general_status=general_status)
                )
            if status in results:
                results[status] += 1
            else:
                results[status] = 1

    results_table = [('Статус', 'Количество')]
    results_table += list(results.items())
    results_table += [('Total', sum(results.values()))]
    return results_table


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
