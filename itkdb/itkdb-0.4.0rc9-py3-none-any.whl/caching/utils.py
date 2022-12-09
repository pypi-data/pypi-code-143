from __future__ import annotations

import json

try:
    # Python 3
    from urllib.parse import urlencode, urlparse
except ImportError:
    # Python 2
    from urllib import urlencode

    from urlparse import urlparse


def build_url(request):
    if request.body:
        parsed = urlparse(request.url)
        if request.headers.get("content-type") == "application/json":
            parsed_body = json.loads(request.body)
        else:
            parsed_body = request.body
        query = "&".join([parsed.query, urlencode({"body": parsed_body})])
        # return '{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}'
        return "{:s}://{:s}{:s}?{:s}".format(
            parsed.scheme, parsed.netloc, parsed.path, query
        )
    return request.url
