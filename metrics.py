import datetime
import platform
from functools import partial


class Metric:
    def __init__(self, update=None):
        self.name = None

        if update is None:
            self.update_interval = None
        else:
            self.update_interval = datetime.timedelta(seconds=update)

        self.command = None
        self.last_updated = None
        self.value = None

    def update(self):
        if self.update_interval is not None:
            if self.last_updated is not None:
                if datetime.datetime.now() - self.last_updated > self.update_interval:
                    self.exec_command()
            else:
                self.exec_command()
            

    def __str__(self):
        return f'{self.name}:{self.value}'

    def get_data(self):
        return (self.name, self.value)

    def exec_command(self):
        self.value = self.command()
        self.last_updated = datetime.datetime.now()

    def close(self):
        pass


class Name(Metric):
    def __init__(self, update=None):
        super().__init__(update)
        self.name = 'name'
        self.command = platform.node
        self.exec_command()


class Time(Metric):
    def __init__(self, update=None):
        super().__init__(update)
        self.name = 'time'
        self.command = lambda:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.exec_command()


class Uptime(Metric):
    def __init__(self, update=None):
        super().__init__(update)
        self.name = 'uptime'
        self.command = self.get_uptime
        self.fd = open('/proc/uptime', 'r')
        self.exec_command()

    def get_uptime(self) -> str:
        raw_sec = int(float(self.fd.readline().split()[0]))
        self.fd.seek(0)
        
        days = raw_sec // 86400
        remainder = raw_sec % 86400
        hours = remainder // 3600
        remainder = remainder % 3600
        minutes = remainder // 60
        seconds = remainder % 60

        return f'{days}d {hours}h {minutes}m {seconds}s'

    def close(self):
        self.fd.close()


class Kernel(Metric):
    def __init__(self, update=None):
        super().__init__(update)
        self.name = 'kernel'
        self.command = self.get_kernel_version
        self.exec_command()

    @staticmethod
    def get_kernel_version():
        version = ''

        with open('/proc/version', 'r') as inf:
            version = inf.readline().split()[2]

        return version


if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    
    kernel = Kernel()
    print(str(kernel))
    kernel.update()
    print(str(kernel))
    kernel.close()
