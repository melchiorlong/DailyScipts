import abc


class GetServerTime(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_time_now(self):
        pass
