#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, message, separator):
    pattern = r'=(.*)'

    content = message.split(separator)
    new_content = []
    for i in content:
        # print(i)
        v = i.split("=")
        # print(v)
        if i:
            if v[0] in fields:
                new_content.append(re.sub(pattern, "="+redaction, i))
            else:
                new_content.append(i)
    # print(new_content)
    res_string = separator.join(new_content)
    # print(res_string)
    return (res_string)
