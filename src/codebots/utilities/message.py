

def format_message(message, to_replace=["_", "*", "[", "`"]):
    for symbol in to_replace:
        message.replace(symbol, '\\' + symbol)
        message.rp
    return message
