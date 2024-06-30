def sec2hms(sec):
    m, s = divmod(sec, 60)
    print( m, s)
    h, m= divmod(m, 60)
    print(h, m)
    str = '%02d:%02d:%02d' % (h, m, s)
    return str

print(sec2hms(-3601))
