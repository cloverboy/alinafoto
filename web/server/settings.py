# -*- coding: utf-8 -*-
import os

SERVER_ENVIRON = os.environ.get('SERVER_ENVIRON', 'local')

if 'production' == SERVER_ENVIRON:
    from launcher.production.settings import *

elif 'development' == SERVER_ENVIRON:
    from launcher.development.settings import *

else:
    from launcher.local.settings import *