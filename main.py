from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.contrib.shortcuts import get_input
from prompt_toolkit.interface import Abort
import pyorient
from tabulate import tabulate
from pygments.style import Style
from pygments.token import Token
from pygments.styles import get_style_by_name
from pygments.lexers import SqlLexer


odb_completer = WordCompleter([
    'select',
    'from'
], ignore_case=True)

class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#005f87 #ffffff',
        Token.Menu.Completions.Completion: 'bg:#303030 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#f6f6f6',
    }
    coloritos = get_style_by_name('fruity').styles
    styles.update(coloritos)

def main():
    while True:
        db_name = 'frente'
        client = pyorient.OrientDB('localhost', 2424)
        client.connect('root', 'root')
        client.db_open(db_name, 'admin', 'admin')
        try:
            text = get_input('> ', lexer=SqlLexer, completer=odb_completer, style=DocumentStyle, raise_exception_on_abort=True)
        except Abort:
            break

        try:
            result = client.query(text.encode('utf-8'))
            new_result = map(lambda x: map(lambda y: y.decode('utf-8') if isinstance(y, str) else y,x.oRecordData.values()), result)
            print tabulate(new_result, result[0].oRecordData.keys(), tablefmt='psql')
        except Exception as err:
            print err.message
    print('chau!')
    client.db_close()


if __name__ == '__main__':
    main()
