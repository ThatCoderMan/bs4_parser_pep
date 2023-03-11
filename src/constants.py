from pathlib import Path

MAIN_PEP_URL = 'https://peps.python.org/'
MAIN_DOC_URL = 'https://docs.python.org/3/'

BASE_DIR = Path(__file__).parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

STATUS_WARNING = ('Несовпадающие статусы:\n'
                  '{link}\n'
                  'Статус в карточке: {status}\n'
                  'Ожидаемые статусы: {general_status}')

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
