import codebots
# from codebots.decorators import monitor


@codebots.telemonitor
def example_function(name):
    return 'hello {}'.format(name)


example_function('frankie')
