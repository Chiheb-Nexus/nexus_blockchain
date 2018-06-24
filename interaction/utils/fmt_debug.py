#
# utils
#
#

from datetime import datetime 

def fmt_debug(**msg):
    message = ' - '.join(
        map(lambda x: ': '.join(x), msg.items())
    )
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    fmt = '-> [{0}] {1}'.format(date, message)
    print(fmt + '\n')