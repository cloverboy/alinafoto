# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-10'

from apps.frontend.views.base import BaseHandler
from apps.frontend.data_provider import get_data_provider


class NewsHandler(BaseHandler):

    def get(self, lang, page, item_id=None, *args, **kwargs):
        dp = get_data_provider(self.application.settings)
        items = dp.get('news', lang=lang)
        sliced_items = []
        found = False

        tpl_kwargs={
            'item_id': item_id,
        }

        if item_id:
            item_id = abs(int(item_id))
            for item in items:
                if item.get('item_id') == item_id:
                    page = 'news_item'
                    found = True
                    tpl_kwargs.update({
                        'page': page,
                        'news_item': item,
                        'page_title': item.get('title'),
                    })
                else:
                    sliced_items.append(item)

        if found:
            items = sliced_items

        tpl_kwargs.update({
            'items': items,
        })

        tpl_name = '%s.html' % page

        super(NewsHandler, self).render(tpl_name, lang, page, tpl_kwargs)