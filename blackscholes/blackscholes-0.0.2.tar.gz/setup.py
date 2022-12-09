# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackscholes', 'blackscholes.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'blackscholes',
    'version': '0.0.2',
    'description': 'Black Scholes calculator for Python including all Greeks',
    'long_description': '# blackscholes\n\nBlack Scholes calculator for Python including all Greeks.\n\n## Installation\n\n`pip install blackscholes`\n\n## Examples\n\n### Input variables\n```python3\nS = 55.0  # Asset price of 55\nK = 50.0  # Strike price of 50\nT = 1.0  # 1 year to maturity\nr = 0.0025  # 0.25% risk-free rate\nsigma = 0.15  # 15% vol\n```\n\n### Call\n\n```python3\nfrom blackscholes import BlackScholesCall\ncall = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma)\ncall.price()  ## 6.339408\ncall.delta()  ## 0.766407\ncall.charm()  ## 0.083267\n```\n\n### Put\n\n```python3\nfrom blackscholes import BlackScholesPut\nput = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma)\nput.price()  ## 1.214564\nput.delta()  ## -0.23359\nput.charm()  ## 0.083267\n```\n\n## Contributing\n\nWe very much welcome new contributions! Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues)\nto see what is currently being worked on.\n\nAlso check out [5. Contributing](https://carlolepelaars.github.io/blackscholes/5.%20contributing/) in the documentation to learn more about \ncontributing to [blackscholes](https://github.com/CarloLepelaars/blackscholes).\n',
    'author': 'CarloLepelaars',
    'author_email': 'info@carlolepelaars.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
