import setup
from gettext import gettext as _

if __name__ == '__main__':
    setup.set_up()
    print( _('''
        Не установлена переменная TOKEN
        для ее установки Набери
        export TOKEN=TOKEN_VALUE
        и попробуй запустить снова.
        ''' ))
