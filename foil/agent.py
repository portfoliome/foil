from types import SimpleNamespace

import requests


UserAgent = SimpleNamespace(
    aol='Mozilla/4.0 (compatible; MSIE 4.01; AOL 4.0; Windows 95)',
    ie='Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)',
    chrome='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/530.10 (KHTML, like Gecko) Chrome/ Safari/530.5',
    safari='Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit (KHTML, like Gecko)',
    firefox='Mozilla/5.0 (Windows 95; en-US; rv:1.8.1.13) Gecko/20080313 Firefox',
    ios='mozilla/5.0 (iphone; cpu iphone os 8_0_0 like mac os x) applewebkit/537.51.1 (KHTML, like Gecko) version/7.0 mobile/11a501 safari/9537.53',
    android='Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'
)


class Agent:
    def __init__(self, user_agent='chrome'):
        self.session = requests.session()
        self.user_agent = user_agent
        self.set_user_agent(self.user_agent)

    def set_header(self, params):
        self.session.headers.update(params)

    def get_header(self, name):
        return self.session.headers[name]

    def get(self, url):
        return self.session.get(url)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def set_user_agent(self, agent):
        agent_string = getattr(UserAgent, agent)
        params = {'User-Agent': agent_string}
        self.set_header(params)
