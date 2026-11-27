def to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 2)


def to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 2)
