from pyspark import SparkContext


class HelloWorld:

    def get_sc(self, app_name):
        sc = SparkContext(master='local', appName=app_name).getOrCreate()
        return sc

    def sc_close(self, sc: SparkContext):
        sc.stop()

    def test(self):
        sc = self.get_sc('fisrtApp')

        rdd1 = sc.parallelize(list[1, 2, 3])
        rdd2 = rdd1.map(lambda x: x * 2)
        self.sc_close(sc)
