import abc


class GetTimezone(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_time_zone(self, timezone):
        pass
