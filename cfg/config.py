from configparser import ConfigParser


def config(section):
    assert isinstance(section, str)

    parser = ConfigParser()
    parser.read("config.ini")

    output = {}
    filename = "../config.ini"
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            output[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return output
