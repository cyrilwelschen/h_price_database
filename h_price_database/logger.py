"""
File containing class Logger to help keep track of what is happening. The idea is to have a universal logging command,
which can be easily changed, e.g. from printing to console to printing to a log file.
"""

from datetime import datetime as dt


class Logger:

    def __init__(self, output_method="print"):
        self.output_method = output_method

    def write_output(self, msg):
        if self.output_method == "print":
            print(msg)
        else:
            raise TypeError("Output method '{}' not yet implemented.".format(self.output_method))

    @staticmethod
    def msg_template(typ, msg, tag=None):
        time_string = dt.now()
        if tag:
            return "{}: {} [{}] - {}".format(time_string, tag, typ, msg)
        else:
            return "{}: {} - {}".format(time_string, typ, msg)

    def log(self, msg, t=None):
        self.write_output(self.msg_template("LOG", msg, tag=t))

    def err(self, msg, t=None):
        self.write_output(self.msg_template("ERR", msg, tag=t))

    def war(self, msg, t=None):
        self.write_output(self.msg_template("WAR", msg, tag=t))
