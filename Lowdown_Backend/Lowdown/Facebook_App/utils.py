import logging
import requests
import threading

logger = logging.getLogger(__name__)

PARALLEL = True

def _make_request(url, payload, results):
    result = requests.get(url, params=payload)
    results.update(result.json())

def get_data(request, target, fields):
    social_user = request.user.social_auth.filter(
         provider='facebook',
    ).first()
    if target is None:
        target = social_user.uid
    url = 'https://graph.facebook.com/%s' % target
    threads = []
    results = {}
    for field in fields:
        field = field.replace("%s", "500")
        payload = {
            'fields': field,
            'access_token': social_user.extra_data['access_token'],
        }
        threads.append(threading.Thread(
            target=_make_request, args=(url, payload, results,)))
    for thread in threads:
        if PARALLEL:
            thread.start()
        else:
            thread.run()
    if PARALLEL:
        for thread in threads:
            thread.join()
    return results
