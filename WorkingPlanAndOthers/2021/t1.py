false = False
true = True

l1 = [

    {
        "date": "2021-10-01",
        "denominator": 1551.5103,
        "is_predicted": false,
        "numerator": 441.47394
    },
    {
        "date": "2021-10-02",
        "denominator": 1562.3945,
        "is_predicted": false,
        "numerator": 494.8201
    },
    {
        "date": "2021-10-03",
        "denominator": 1562.8374,
        "is_predicted": false,
        "numerator": 442.07965
    },
    {
        "date": "2021-10-04",
        "denominator": 1556.405,
        "is_predicted": false,
        "numerator": 529.2389
    },
    {
        "date": "2021-10-05",
        "denominator": 1201.2075,
        "is_predicted": false,
        "numerator": 478.56244
    },
    {
        "date": "2021-10-06",
        "denominator": 1867.5093,
        "is_predicted": false,
        "numerator": 686.5389
    },
    {
        "date": "2021-10-07",
        "denominator": 1532.4255,
        "is_predicted": false,
        "numerator": 576.65845
    },
    {
        "date": "2021-10-08",
        "denominator": 1355.7467,
        "is_predicted": false,
        "numerator": 507.10345
    },
    {
        "date": "2021-10-09",
        "denominator": 1558.9772,
        "is_predicted": false,
        "numerator": 591.44543
    },
    {
        "date": "2021-10-10",
        "denominator": 1611.5509,
        "is_predicted": false,
        "numerator": 616.3495
    },
    {
        "date": "2021-10-11",
        "denominator": 1423.3396,
        "is_predicted": false,
        "numerator": 577.3433
    },
    {
        "date": "2021-10-12",
        "denominator": 1386.1381,
        "is_predicted": false,
        "numerator": 499.91977
    },
    {
        "date": "2021-10-13",
        "denominator": 1516.5726,
        "is_predicted": false,
        "numerator": 507.7093
    },
    {
        "date": "2021-10-14",
        "denominator": 1505.1439,
        "is_predicted": false,
        "numerator": 751.342
    },
    {
        "date": "2021-10-15",
        "denominator": 1210.028,
        "is_predicted": false,
        "numerator": 668.5328
    },
    {
        "date": "2021-10-16",
        "denominator": 1352.1182,
        "is_predicted": false,
        "numerator": 752.28644
    },
    {
        "date": "2021-10-17",
        "denominator": 1279.7565,
        "is_predicted": false,
        "numerator": 582.8617
    },
    {
        "date": "2021-10-18",
        "denominator": 1132.9838,
        "is_predicted": false,
        "numerator": 481.14438
    },
    {
        "date": "2021-10-19",
        "denominator": 1120.4856,
        "is_predicted": true,
        "numerator": 369.1888
    },
    {
        "date": "2021-10-20",
        "denominator": 1107.4694,
        "is_predicted": true,
        "numerator": 421.51392
    },
    {
        "date": "2021-10-21",
        "denominator": 467.92688,
        "is_predicted": true,
        "numerator": 210.01495
    },
    {
        "date": "2021-10-22",
        "denominator": 1530.5571,
        "is_predicted": true,
        "numerator": 711.8468
    },
    {
        "date": "2021-10-23",
        "denominator": 793.9076,
        "is_predicted": true,
        "numerator": 369.97684
    },
    {
        "date": "2021-10-24",
        "denominator": 895.0702,
        "is_predicted": true,
        "numerator": 374.24673
    },
    {
        "date": "2021-10-25",
        "denominator": 866.8705,
        "is_predicted": true,
        "numerator": 415.0576
    },
    {
        "date": "2021-10-26",
        "denominator": 877.61017,
        "is_predicted": true,
        "numerator": 280.33502
    },
    {
        "date": "2021-10-27",
        "denominator": 843.66925,
        "is_predicted": true,
        "numerator": 257.336
    },
    {
        "date": "2021-10-28",
        "denominator": 623.1402,
        "is_predicted": true,
        "numerator": 350.03033
    },
    {
        "date": "2021-10-29",
        "denominator": 491.12094,
        "is_predicted": true,
        "numerator": 229.04898
    },
    {
        "date": "2021-10-30",
        "denominator": 862.0416,
        "is_predicted": true,
        "numerator": 292.34418
    },
    {
        "date": "2021-10-31",
        "denominator": 558.99365,
        "is_predicted": true,
        "numerator": 236.95183
    },
    {
        "date": "2021-11-01",
        "denominator": 793.66797,
        "is_predicted": true,
        "numerator": 328.29282
    }
]

sum_rev = 0
sum_spend = 0

start_Date = '2021-10-01'
end_Date = '2021-11-01'

for i in l1:
    if start_Date <= i.get('date', 0) <= end_Date:
        sum_rev += i.get('numerator', 0)
        sum_spend += i.get('denominator', 0)
print(sum_rev)
print(sum_spend)
#
# 936.29
# 3113.9
