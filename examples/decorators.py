import codebots
import time
# from codebots.decorators import monitor


@codebots.telemonitor
def example_function(seconds):
    print('hello, in {} seconds you will get a message on telegram'.format(str(seconds)))
    time.sleep(seconds)
    print("...ok...a bit more...!")


example_function(2)
