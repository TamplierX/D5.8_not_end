from django import template


register = template.Library()


CENSOR_WORDS = [
    'First', 'first',
    'Second', 'second',
    'Third', 'third'
]


@register.filter()
def censor(text):
    if type(text) is not str:
        raise TypeError('Фильтр "censor" предназначен только для переменных строкового типа ')

    ln = len(CENSOR_WORDS)
    censor_text = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in text:
        string += i

        count = 0
        for j in CENSOR_WORDS:
            if string not in j:
                count += 1
            if string == j:
                censor_text += j[0] + pattern * (len(string) - 1)
                count -= 1
                string = ''

        if count == ln:
            censor_text += string
            string = ''

    if string != '' and string not in CENSOR_WORDS:
        censor_text += string
    elif string != '':
        censor_text += pattern * len(string)

    return censor_text
