from .models import DialplanContext


def context_ael(ctx: DialplanContext):
    result = f'context {ctx.name}' + ' { \n'
    for extension in ctx.extensions.all().order_by('ext'):
        result += f'    {extension.ext} =>'+' { \n'
        dialplan = extension.dialplan.split('\n')
        for line in dialplan:
            result += f'        {line}'+'\n'

        result += '    }\n'

    result += '} \n'
    return result


def make_extensions_ael():
    '''
    Read the contexts and extensions from the database and generate AEL file.
    '''
    result = ''

    ctxs = DialplanContext.objects.all().order_by('name')
    for ctx in ctxs:
        result += context_ael(ctx)

    return result
