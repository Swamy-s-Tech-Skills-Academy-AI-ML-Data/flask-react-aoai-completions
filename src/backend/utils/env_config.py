from dotenv import dotenv_values

config_details = dotenv_values(".env")


def get_config_value(key):
    return config_details.get(key, None)
