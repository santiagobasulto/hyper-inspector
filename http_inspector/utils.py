"""
This code was stolen from Requests:
https://github.com/psf/requests/blob/2c2138e811487b13020eb331482fb991fd399d4e/requests/utils.py
"""


def _parse_content_type_header(content_type):
    """Returns content type and parameters from given header
    :param header: string
    :return: tuple containing content type and dictionary of
         parameters
    """

    tokens = content_type.split(";")
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = "\"' "

    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find("=")
            if index_of_equals != -1:
                key = param[:index_of_equals].strip(items_to_strip)
                value = param[index_of_equals + 1 :].strip(items_to_strip)
            params_dict[key.lower()] = value
    return content_type, params_dict


def get_encoding_from_headers(content_type):
    """Returns encodings from given HTTP Header Dict.
    :param headers: dictionary to extract encoding from.
    :rtype: str
    """

    if not content_type:
        return None

    content_type, params = _parse_content_type_header(content_type)

    if "charset" in params:
        return params["charset"].strip("'\"")

    if "text" in content_type:
        return "ISO-8859-1"

    if "application/json" in content_type:
        # Assume UTF-8 based on RFC 4627: https://www.ietf.org/rfc/rfc4627.txt since the charset was unset
        return "utf-8"
