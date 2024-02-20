import ssl

import nltk


def download_resource(resources: list):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    if type(resources) is str:
        nltk.download(resources)
    elif type(resources) is list:
        for resource in resources:
            nltk.download(resource)
    else:
        raise TypeError('Resources need a string or a list')