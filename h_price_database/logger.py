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
    def msg_template(type, msg):
        time_string = dt.now()
        return "{}: {} - {}".format(time_string, type, msg)

    def log(self, msg):
        self.write_output(self.msg_template("LOG", msg))

    def err(self, msg):
        self.write_output(self.msg_template("ERR", msg))

    def war(self, msg):
        self.write_output(self.msg_template("WAR", msg))
