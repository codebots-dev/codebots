from codebots.bots import TeleBot


def telemonitor(function):
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        bot = TeleBot()
        bot.send_message("{} is done!".format(str(function.__name__)))

    return wrapper
