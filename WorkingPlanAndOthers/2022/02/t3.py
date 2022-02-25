m1 = {
    'applovin_exchange': 'applovin',
    'google admob': 'admob',
    'unity ads': 'unity',
    'verve': 'pubnative',
    'com.google.ads.mediation.ironsource.IronSourceAdapter': 'ironsource',
    'com.google.ads.mediation.admob.AdMobAdapter': 'admob',
    'com.google.ads.mediation.unity.UnityAdapter': 'unity',
    'com.google.ads.mediation.adcolony.AdColonyMediationAdapter': 'adcolony',
    'com.google.ads.mediation.applovin.AppLovinMediationAdapter': 'applovin',
}

new_dict = dict((k.lower(), v) for k, v in m1.items())
print(new_dict)

str1 = 'com.google.ads.mediation.admob.AdMobAdapter'
str2 = 'com.google.ads.mediation.admob.admobadapter'


if str1 in new_dict:
    print('true')
else:
    print('false')



if str2 in new_dict:
    print('true')
else:
    print('false')
