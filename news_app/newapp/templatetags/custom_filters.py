from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает,

# заменяет слова "жесть", "афигенно", "круто" на слово "здорово" (для рабочего примера: первая стать, 10 слово)
@register.filter(name='Censor')
def Censor(value, arg):
    value = value.replace("жесть", "ЗДОРОВО")
    value = value.replace("афигенно", "ЗДОРОВО")
    value = value.replace("круто", "ЗДОРОВО")
    return value


'''
# прошлая версия, не используется
@register.filter(name='Censor1')
def Censor1(value, arg):  # первый аргумент здесь это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|multiply:arg
    if ("жесть" in value) or ("афигенно" in value) or ("круто" in value):
        arg = 'ВНИМАНИЕ, ВНИМАНИЕ!!! Говорит Москва!!! В тексте используется неформальная лексика, применен ценз (замена слов)'
        return arg   # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    else:
        return value

'''