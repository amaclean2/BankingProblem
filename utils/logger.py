LOGGING_ACTIVE = True

def logger(message, *options):
    if LOGGING_ACTIVE:
        print(message)
        if len(options) != 0:
            for option in options:
                print(option)