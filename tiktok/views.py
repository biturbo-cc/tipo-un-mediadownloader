import os, json
import environ, requests
from django.views import View
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from django.conf import settings


env = environ.Env()
environ.Env.read_env(settings.BASE_DIR / 'tiktok/.env')

cookies = {
    'tt_csrf_token': env.str('tt_csrf_token'),
    '_abck': env.str('_abck'),
    'ak_bmsc': env.str('ak_bmsc'),
    'bm_sz': env.str('bm_sz'),
    '__tea_cache_tokens_1988': env.str('__tea_cache_tokens_1988'),
    'passport_csrf_token': env.str('passport_csrf_token'),
    'passport_csrf_token_default': env.str('passport_csrf_token_default'),
    'bm_mi': env.str('bm_mi'),
    'ttwid': env.str('ttwid'),
    'msToken': env.str('msToken'),
    'cmpl_token': env.str('cmpl_token'),
    'store-idc': env.str('store_idc'),
    'store-country-code': env.str('store_country_code'),
    'tt-target-idc': env.str('tt_target_idc'),
    'bm_sv': env.str('bm_sv'),
    'odin_tt': env.str('odin_tt'),
    'sid_guard': env.str('sid_guard'),
    'uid_tt': env.str('uid_tt'),
    'uid_tt_ss': env.str('uid_tt_ss'),
    'sid_tt': env.str('sid_tt'),
    'sessionid': env.str('sessionid'),
    'sessionid_ss': env.str('sessionid_ss'),
    'sid_ucp_v1': env.str('sid_ucp_v1'),
    'ssid_ucp_v1': env.str('ssid_ucp_v1'),
    'msToken': env.str('msToken_2'),
}

headers = {
    'sec-ch-ua': env.str('sec_ch_ua'),
    'sec-ch-ua-mobile': env.str('sec_ch_ua_mobile'),
    'sec-fetch-dest': env.str('sec_fetch_dest'),
    'sec-fetch-mode': env.str('sec_fetch_mode'),
    'sec-fetch-site': env.str('sec_fetch_site'),
    'upgrade-insecure-requests': env.str('upgrade_insecure_requests'),
    'user-agent': env.str('user_agent'),
}


def video_dict(kwargs):
    url = 'https://'

    if 'code' in kwargs:
        url += f'vm.tiktok.com/{kwargs["code"]}/'
    else:
        url += f'www.tiktok.com/{kwargs["user"]}/video/{kwargs["id"]}'

    response = requests.get(url, cookies=cookies, headers=headers)
    if not response.ok:
        return HttpResponseNotFound('Video not found.')

    text = response.text
    start = text.find('"video":{"i') + 8
    end = text.find(',"author"')
    result = text[start:end]

    return json.loads(result)


class InfoView(View):

    def get(self, request, *args, **kwargs):
        content = video_dict(kwargs)
        return JsonResponse(content, json_dumps_params={'indent': 4, 'sort_keys': False})


class StreamingView(View):

    def get(self, request, *args, **kwargs):
        content = video_dict(kwargs)
        response = requests.get(content['playAddr'], stream=True)
        streaming = StreamingHttpResponse(
            response.raw,
            content_type=response.headers.get('content-type'),
            status=response.status_code,
            reason=response.reason,
        )
        streaming['Content-Disposition'] = f'inline; filename="{content["id"]}.mp4"'
        return streaming


class DownloadView(View):

    def get(self, request, *args, **kwargs):
        content = video_dict(kwargs)
        response = requests.get(content['playAddr'], stream=True)
        download = StreamingHttpResponse(
            response.raw,
            content_type=response.headers.get('content-type'),
            status=response.status_code,
            reason=response.reason,
        )
        download['Content-Disposition'] = f'attachement; filename="{content["id"]}.mp4"'
        return download


class CoverView(View):

    def get(self, request, *args, **kwargs):
        content = video_dict(kwargs)
        response = requests.get(content['dynamicCover'], stream=True)
        return StreamingHttpResponse(
            response.raw,
            content_type=response.headers.get('content-type'),
            status=response.status_code,
            reason=response.reason,
        )
