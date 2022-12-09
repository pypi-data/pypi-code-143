# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wonda',
 'wonda.api',
 'wonda.api.request_validator',
 'wonda.api.response_validator',
 'wonda.api.utils',
 'wonda.bot',
 'wonda.bot.blueprint',
 'wonda.bot.dispatch',
 'wonda.bot.dispatch.handlers',
 'wonda.bot.dispatch.labelers',
 'wonda.bot.dispatch.middlewares',
 'wonda.bot.dispatch.return_manager',
 'wonda.bot.dispatch.router',
 'wonda.bot.dispatch.view',
 'wonda.bot.polling',
 'wonda.bot.rules',
 'wonda.bot.states',
 'wonda.bot.states.dispenser',
 'wonda.bot.updates',
 'wonda.contrib',
 'wonda.contrib.rules',
 'wonda.contrib.storage',
 'wonda.errors',
 'wonda.errors.error_handler',
 'wonda.errors.swear_handler',
 'wonda.http',
 'wonda.tools',
 'wonda.tools.keyboard',
 'wonda.tools.storage',
 'wonda.tools.text',
 'wonda.tools.text.formatting',
 'wonda.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'certifi>=2022.6.15,<2023.0.0',
 'choicelib>=0.1.5,<0.2.0',
 'pydantic>=1.9.0,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{'auto-reload': ['watchfiles>=0.16.0,<0.17.0'],
 'power-ups': ['orjson>=3.7.11,<4.0.0', 'uvloop>=0.16.0,<0.17.0']}

setup_kwargs = {
    'name': 'wonda',
    'version': '0.1.0',
    'description': 'Asynchronous, feature-rich, high performant Telegram Bot API framework for building stunning bots',
    'long_description': '# wonda ✨\n\n[//]: # (Links to examples)\n[text formatting]: https://github.com/wondergram-org/framework/blob/main/examples/high_level/formatting_example.py\n[middleware]: https://github.com/wondergram-org/framework/blob/main/examples/high_level/setup_middleware.py\n[file uploading]: https://github.com/wondergram-org/framework/blob/main/examples/high_level/file_upload_example.py\n[blueprints]: https://github.com/wondergram-org/framework/blob/main/examples/high_level/load_blueprints.py\n[FSM]: https://github.com/wondergram-org/framework/blob/main/examples/high_level/use_state_dispenser.py\n[awesome examples]: https://github.com/wondergram-org/framework/tree/main/examples/high_level\n\n![Version](https://img.shields.io/pypi/v/wonda?label=version&style=flat-square)\n![Package downloads](https://img.shields.io/pypi/dw/wonda?label=downloads&style=flat-square)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/wonda?label=supported%20python%20versions&style=flat-square)\n\n## > why\n\n`wonda` empowers you to build powerful bots using simple tools while not sacrifing performance and extensibility. It has all batteries included: [text formatting], [file uploading], [blueprints], [middleware] and [FSM] are available to use right away.\n\n## > install\n\nTo install a default version, use\n\n```shell script\npip install -U wonda\n```\n\nIf you decided to go beta, use the same command with `--pre` option or update from dev branch .zip [archive](https://github.com/wondergram-org/framework/archive/refs/heads/dev.zip).\n\nYou can make `wonda` perform even better by installing power-ups. They are optional, but highly recommended. Install them using\n\n```shell script\npip install --force wonda[power-ups]\n```\n\nTo see the full list of packages, refer to our [project file](https://github.com/wondergram-org/framework/blob/main/pyproject.toml).\n\n## > examples\n\nIt\'s easy to build an echo bot with `wonda` — it\'s ready in *six* lines of code. And expanding it further is a piece of cake too.\n\n```python\nfrom wonda import Bot\n\nbot = Bot("your-token")\n\n\n@bot.on.message()\nasync def handler(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n```\n\nIsn\'t it beautiful how little code is needed to achieve something this big? To get started on `wonda`, check out our [awesome examples].\n\n## > license\n\nThis project is MIT licensed. Big thanks to maintainers and contributors of [vkbottle](https://github.com/vkbottle/vkbottle) upon which it is built!\n\n© **timoniq** (2019-2021), **feeeek** (2022), **exthrempty** (2022)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/wonda/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
