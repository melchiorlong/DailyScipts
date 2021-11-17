false = False
true = True

l1 =  [
            {
                "date": "2021-09-26",
                "denominator": 1195.2263,
                "is_predicted": false,
                "numerator": 71.86114
            },
            {
                "date": "2021-09-25",
                "denominator": 1005.4162,
                "is_predicted": false,
                "numerator": 49.390377
            },
            {
                "date": "2021-09-18",
                "denominator": 714.9336,
                "is_predicted": false,
                "numerator": 101.47436
            },
            {
                "date": "2021-10-07",
                "denominator": 1816.0845,
                "is_predicted": false,
                "numerator": 61.645164
            },
            {
                "date": "2021-10-10",
                "denominator": 1611.5472,
                "is_predicted": false,
                "numerator": 90.03519
            },
            {
                "date": "2021-10-08",
                "denominator": 1605.8652,
                "is_predicted": false,
                "numerator": 119.273026
            },
            {
                "date": "2021-10-12",
                "denominator": 1570.1869,
                "is_predicted": false,
                "numerator": 132.94281
            },
            {
                "date": "2021-09-30",
                "denominator": 993.36774,
                "is_predicted": false,
                "numerator": 151.35254
            },
            {
                "date": "2021-10-04",
                "denominator": 1426.2178,
                "is_predicted": false,
                "numerator": 129.89798
            },
            {
                "date": "2021-10-13",
                "denominator": 1658.5243,
                "is_predicted": false,
                "numerator": 123.29153
            },
            {
                "date": "2021-09-21",
                "denominator": 804.7884,
                "is_predicted": false,
                "numerator": 108.95482
            },
            {
                "date": "2021-09-17",
                "denominator": 599.072,
                "is_predicted": false,
                "numerator": 61.586216
            },
            {
                "date": "2021-10-03",
                "denominator": 1397.4264,
                "is_predicted": false,
                "numerator": 113.781136
            },
            {
                "date": "2021-09-20",
                "denominator": 835.6541,
                "is_predicted": false,
                "numerator": 53.09361
            },
            {
                "date": "2021-10-11",
                "denominator": 1625.4943,
                "is_predicted": false,
                "numerator": 92.330666
            },
            {
                "date": "2021-09-22",
                "denominator": 921.7898,
                "is_predicted": false,
                "numerator": 83.15652
            },
            {
                "date": "2021-10-16",
                "denominator": 1691.69,
                "is_predicted": false,
                "numerator": 74.79373
            },
            {
                "date": "2021-10-05",
                "denominator": 1703.5432,
                "is_predicted": false,
                "numerator": 127.76579
            },
            {
                "date": "2021-09-27",
                "denominator": 1225.9176,
                "is_predicted": false,
                "numerator": 86.04785
            },
            {
                "date": "2021-09-23",
                "denominator": 901.5976,
                "is_predicted": false,
                "numerator": 102.97073
            },
            {
                "date": "2021-09-28",
                "denominator": 1201.7377,
                "is_predicted": false,
                "numerator": 91.82305
            },
            {
                "date": "2021-09-24",
                "denominator": 1000.10016,
                "is_predicted": false,
                "numerator": 32.039597
            },
            {
                "date": "2021-10-14",
                "denominator": 1925.6909,
                "is_predicted": false,
                "numerator": 88.748634
            },
            {
                "date": "2021-09-16",
                "denominator": 613.1949,
                "is_predicted": false,
                "numerator": 46.13926
            },
            {
                "date": "2021-09-29",
                "denominator": 1428.3066,
                "is_predicted": false,
                "numerator": 69.25669
            },
            {
                "date": "2021-09-19",
                "denominator": 729.1448,
                "is_predicted": false,
                "numerator": 49.560867
            },
            {
                "date": "2021-10-06",
                "denominator": 1188.9564,
                "is_predicted": false,
                "numerator": 64.962524
            },
            {
                "date": "2021-10-02",
                "denominator": 1276.2367,
                "is_predicted": false,
                "numerator": 85.05502
            },
            {
                "date": "2021-10-01",
                "denominator": 1274.3988,
                "is_predicted": false,
                "numerator": 78.93271
            },
            {
                "date": "2021-10-09",
                "denominator": 1587.7854,
                "is_predicted": false,
                "numerator": 153.76376
            },
            {
                "date": "2021-10-15",
                "denominator": 1906.4785,
                "is_predicted": false,
                "numerator": 91.782646
            }
        ]



sum_rev = 0
sum_spend = 0

start_Date = '2021-10-09'
end_Date = '2021-10-15'

for i in l1:
    if start_Date <= i.get('date', 0) <= end_Date:
        sum_rev += i.get('numerator', 0)
        sum_spend += i.get('denominator', 0)
print(sum_rev)
print(sum_spend)
#
# 936.29
# 3113.9