# -*- coding: utf-8 -*-

import logging
import json

from lib.utils.encoding import addslashes, encode_emails_with_rot13, escape

from settings import DEFAULT_LANG

logger = logging.getLogger('default')


class Translation(object):

    def find(self, key, lang=DEFAULT_LANG, default=None, more_slashes=False, fix_unicode_prefixes=False):
        result = TRANSLATIONS.get(lang, {}).get(key)

        if result is None:
            logger.error('translation not found. key: <%s>, lang: <%s>' % (key, lang))
            result = default

        if isinstance(result, str):
            result = encode_emails_with_rot13(escape(result))

            if fix_unicode_prefixes:
                result = json.dumps(result, ensure_ascii=False)

                if more_slashes:
                    result = addslashes(result)

        return result


TRANSLATIONS = {
    'lv': {
        'site_name': 'Profesionāls fotogrāfs Alīna Taranovska',
        'page_description': 'Kāzu fotogrāfs, svētku fotogrāfs, bērnu pasākumu fotogrāfs, '
                            'portretu meistars. Zemas cenas. Kāzu fotogrāfs Rīgā.',
        'page_keywords': ['profesionāls fotogrāfs', 'bilžu apstrāde', 'kāzas', 'zemas cenas'],
        'author_name': 'Alina Taranovska',
        'author_email': 'alina.taranovska@gmail.com',
        'author_phone': '(+371) 268-676-08',
        'no_flash_1': 'Profesionāla fotogrāfa Alīnas Taranovskas web lapa',
        'no_flash_2': 'Lai, apskatītu portfolio, lūdzu, instalējiet pielikumu Flash Player',
        'download': 'Ielādēt',
        'lang_lv': 'Latviski',
        'lang_ru': 'Krieviski',
        'lang_en': 'Angliski',
        'all': 'Visas fotogrāfijas',
        'weddings': 'Kāzu fotogrāfijas',
        'children': 'Fotogrāfijas ar bērniem',
        'parties': 'Fotogrāfijas no ballītēm',
        'others': 'Dažādas fotogrāfijas',
        'guestbook': 'Viesu grāmata',
        'index_page_title': 'Galvenā',
        'weddings_page_title': 'Kāzas',
        'children_page_title': 'Bērni',
        'parties_page_title': 'Ballītes',
        'others_page_title': 'Dažādi',
        'error_page_title': 'Ou! Lapa nav atrasta',
        'error_page_description': 'Atvainojiet, pieprasītā lapa netika atrasta',
        'error_page_h1': 'Ou! Lapa nav atrasta',
        'error_page_p_1': 'Atvainojiet, pieprasītā lapa netika atrasta - 404',
        'error_page_img': 'Kaķēns',
        'error_page_return': 'Atgriezties un sākuma lapu',
    },
    'ru': {
        'site_name': 'Профессиональная фотосъёмка от Алины Тарановской',
        'page_description': 'Профессиональная фотосъёмка от Алины Тарановской. '
                            'Свадебный фотограф, фотограф мероприятий, фотограф детских '
                            'праздников, детский фотограф. Низкие цены. Фотограф в Риге.',
        'page_keywords': ['профессиональный фотограф', 'обработка фотографий', 'свадьба', 'низкие цены'],
        'author_name': 'Алина Тарановская',
        'author_email': 'alina.taranovska@gmail.com',
        'author_phone': '(+371) 268-676-08',
        'no_flash_1': 'Веб страница профессионального фотографа Алины Тарановской',
        'no_flash_2': 'Для просмотра веб страницы требуется Flash Player',
        'download': 'Скачать',
        'lang_lv': 'По-латышски',
        'lang_ru': 'По-русски',
        'lang_en': 'По-английски',
        'all': 'Все фотографии',
        'weddings': 'Свадебные фотографии',
        'children': 'Фотографии с детьми',
        'parties': 'Фотографии с вечеринок',
        'others': 'Разные фотографии',
        'guestbook': 'Гостевая книга',
        'index_page_title': 'Главная',
        'weddings_page_title': 'Свадьбы',
        'children_page_title': 'Дети',
        'parties_page_title': 'Вечеринки',
        'others_page_title': 'Разное',
        'error_page_title': 'Ой! Страница не найдена',
        'error_page_description': 'Запрашиваемая Вами страница не найдена',
        'error_page_h1': 'Ой! Страница не найдена',
        'error_page_p_1': 'Запрашиваемая Вами страница не найдена - 404',
        'error_page_img': 'Котёнок',
        'error_page_return': 'Вернуться на главную страницу',
    },
    'en': {
        'site_name': 'Professional photographer Alina Taranovska',
        'page_description': 'Web page of photographer Alina Taranovska. '
                            'Weddings, parties, portraits. Low prices.',
        'page_keywords': ['professional photographer', 'photo editing retouching', 'wedding', 'low price'],
        'author_name': 'Alina Taranovska',
        'author_email': 'alina.taranovska@gmail.com',
        'author_phone': '(+371) 268-676-08',
        'no_flash_1': 'Web page of photographer Alina Taranovska',
        'no_flash_2': 'In order to see content you need Flash Player',
        'download': 'Download',
        'lang_lv': 'Latvian',
        'lang_ru': 'Russian',
        'lang_en': 'English',
        'all': 'All photos',
        'weddings': 'Photos from weddings',
        'children': 'Photos with children',
        'parties': 'Photos from parties',
        'others': 'Other photos',
        'guestbook': 'Guestbook',
        'index_page_title': 'Main',
        'weddings_page_title': 'Weddings',
        'children_page_title': 'Children',
        'parties_page_title': 'Parties',
        'others_page_title': 'Others',
        'error_page_title': 'Wou! Page wasnt found',
        'error_page_description': 'Requested page can not be found',
        'error_page_h1': 'Wou! Page wasnt found',
        'error_page_p_1': 'Requested page can not be found - 404',
        'error_page_img': 'Kitten',
        'error_page_return': 'Visit main page',
    },
}