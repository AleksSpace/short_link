from string import ascii_letters, digits

'''Константы'''
SYMBOLS = f'{ascii_letters}{digits}'
MAX_LEN_SHORT_URL = 16
MIN_LEN_SHORT_URL = 1
LEN_SHORT_URL = 6
PATTERN = rf'^[{SYMBOLS}]+$'
FORMAT_DATE = '%Y-%m-%d %H:%M'

'''Сообщения'''
NAME_BUSY = 'Имя {} уже занято!'
URL_READY = 'Ваша ссылка готова:'

EMPTY_REQUEST = 'Отсутствует тело запроса'
REQ_FIELD = '\"url\" является обязательным полем!'
BAD_NAMING = 'Указано недопустимое имя для короткой ссылки'
NO_ID = 'Указанный id не найден'
API_NAME_BUSY = 'Имя "{}" уже занято.'
NO_FORMAT_DATE = 'Дата должна быть в формате: Год-месяц-день часы:минуты'
NO_DATETIME_PAST = 'Дата и время должны быть больше текущего'