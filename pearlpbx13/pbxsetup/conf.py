from .models import SIPTransport


def make_pjsip_conf_transports():
    result = '; ==== Transports section ====\n'
    transports = SIPTransport.objects.all()
    for transport in transports:
        description = '; ' + transport.description + '\n'
        section_name = '[transport-' + \
            transport.name.replace(' ', '').replace('+', '-').lower() + ']\n'
        type = 'type = transport\n'
        protocol = 'protocol = ' + transport.protocol + '\n'
        bind = 'bind = ' + transport.bind + '\n'
        comment_nat = '; NAT Settings\n'

        external_media_address = ''
        if transport.external_media_address is not None:
            external_media_address = 'external_media_address = ' + \
                transport.external_media_address + '\n'

        external_signaling_address = ''
        if transport.external_signaling_address is not None:
            external_signaling_address = 'external_signaling_address = ' + \
                transport.external_signaling_address + '\n'

        local_nets = ''
        if transport.local_nets is not None:
            nets = transport.local_nets.replace(' ', '').split(',')
            for net in nets:
                local_nets += 'local_net = ' + net + '\n'

        result += description + section_name + type + \
            protocol + bind + comment_nat + external_media_address + \
            external_signaling_address + local_nets

        result += '\n'

    return result


def make_pjsip_conf():

    plaintext = "; === This is auto generated file. Do not edit it. Use PBX13 admin panel! ===\n"
    plaintext += make_pjsip_conf_transports()

    return plaintext
