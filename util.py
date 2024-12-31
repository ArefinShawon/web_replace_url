from odoo.addons.base.models.assetsbundle import JavascriptAsset
from odoo.tools import transpile_javascript
import re
from odoo import http
from .models.ir_http import base_sorturl

@property
def content(self):
    content = super(JavascriptAsset, self).content
    if self.name == "/web/static/src/core/browser/router.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.name == "/web/static/src/webclient/navbar/navbar.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.is_transpiled:
        if not self._converted_content:
            self._converted_content = transpile_javascript(self.url, content)
        return self._converted_content
    return content


JavascriptAsset.content = content


def url_init(self, httprequest):
    if "odoo" in httprequest.path:
        httprequest.path = httprequest.path.replace("odoo", base_sorturl[0])
    self.httprequest = httprequest
    self.future_response = http.FutureResponse()
    self.dispatcher = http._dispatchers['http'](self)
    self.geoip = http.GeoIP(httprequest.remote_addr)
    self.registry = None
    self.env = None


http.Request.__init__ = url_init
