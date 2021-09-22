def forward(data):
    print('FORWARD')
    msg = data['data']
    if(msg == 'pressed'):
        print('Start')
    elif(msg == 'released'):
        print('Stop')

def backward(data):
    print('BACK')
    msg = data['data']
    if(msg == 'pressed'):
        print('Start')
    elif(msg == 'released'):
        print('Stop')

def left(data):
    print('LEFT')
    msg = data['data']
    if(msg == 'pressed'):
        print('Start')
    elif(msg == 'released'):
        print('Stop')


def right(data):
    print('RIGHT')
    msg = data['data']
    if(msg == 'pressed'):
        print('Start')
    elif(msg == 'released'):
        print('Stop')