from importlib import import_module


def monitor(bot_name, **dec_kwargs):
    def decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
            cls = getattr(import_module('codebots.bots.{}'.format(bot_name.lower())), bot_name)
            bot = cls()
            if 'message' not in dec_kwargs.keys():
                dec_kwargs['message'] = "{} is done!".format(str(function.__name__))
            bot.send_message(**dec_kwargs)
        return wrapper
    return decorator
