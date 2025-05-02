import logging

def set_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    print(name)
    
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # file_error_handler = logging.FileHandler(
    #     'error.log')
    # file_error_handler.setFormatter(formatter)
    # file_error_handler.setLevel(logging.ERROR)

    file_info_handler = logging.FileHandler(
        'logs/info.log')
    file_info_handler.setFormatter(formatter)
    file_info_handler.setLevel(logging.INFO)


    #file_handler.setLevel(logging.ERROR)

    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(formatter)

    #logger.addHandler(file_error_handler)
    logger.addHandler(file_info_handler)

    return logger

def test():
    logger = set_logger(__name__)
    print(logger)
    logger.info('test')
    
if __name__ == '__main__':
    test()
