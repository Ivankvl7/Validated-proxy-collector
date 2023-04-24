# Validated-proxy-collector
A proxy collector which gathers anynymous proxies and checks them for validity.
By importing GetValidatedProxy class into your project and running the following code you can get access to free and validated proxies as a list, assigned to a variable proxies.

import asyncio

pr = GetValidatedProxy()
proxies: list[str] = asyncio.run(pr.main())

Please import the class and asyncio module properly before running the code

REQUIREMENTS:
python 3.10+ '\n'
bs4
requests
asyncio
aiohttp
fake_useragent
pprint
