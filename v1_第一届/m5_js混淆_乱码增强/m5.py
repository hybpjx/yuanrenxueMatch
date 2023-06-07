import requests
import execjs


def get_params():
    ctx = execjs.compile(open('m5.js', 'r', encoding='utf-8').read())
    params = ctx.call('get_params')

    return params


def get_page(page):
    par = get_params()
    headers = {
        "user-agent": "yuanrenxue.project",
    }

    url = "https://match.yuanrenxue.com/api/match/5"

    cookies = {
        "sessionid": "94hkmtl47z6i4pb57gwikd3eaxv247ev",
        "RM4hZBv0dDon443M": par['RM4hZBv0dDon443M']
    }

    params = {
        "page": str(page),
        "m": par['url_m'],
        "f": par['url_m']
    }
    print(par)
    res = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(res.text)
    return [data['value'] for data in res.json()['data']]


if __name__ == '__main__':
    total = []
    for i in range(1, 6):
        total += get_page(i)

    # print(sorted(total)[-5:])
    # sum(sorted(total)[:5])
    print('5名直播间热度的加和:', sum(sorted(total)[-5:]))
