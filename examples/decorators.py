import codebots
import time

# Simply add the `monitor` decorator before your funcion (Note the capital letters!)
# currently only `SlakBot` and `TeleBot` are supported.


@codebots.monitor("SlackBot", channel="topopt")
# @codebots.monitor("TeleBot", message="this is a personalized message")  # would send the message through slack instead
def example_function(seconds):
    print('hello, in {} second(s) you will get a message on telegram'.format(str(seconds)))
    time.sleep(seconds)
    print("...ok...a bit more...! :)")


example_function(3)
