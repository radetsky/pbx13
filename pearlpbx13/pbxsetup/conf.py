from .models import SIPTransport, SIPUser, Settings


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


def make_pjsip_conf_uplinks():
    result = '; ==== Uplinks section ====\n'

    return result


def make_pjsip_conf_users_template():
    result = '; ==== Users template ====\n'
    result += '[user-template](!)\n'
    settings = Settings.objects.first()
    result += settings.user_template
    result += '\n\n'
    return result


def make_pjsip_conf_users():
    result = '; ==== Users section ====\n'
    users = SIPUser.objects.all()
    for user in users:
        comment = '; ' + user.name + '\n'
        section = f'[{user.username}](user-template)\n'
        auth = f'auth = {user.username}\n'
        aors = f'aors = {user.username}\n'
        callerid = f'callerid = {user.name} <{user.extension}>\n'
        custom_settings = user.custom_settings + '\n'

        type_auth = f'[{user.username}]\ntype = auth\nauth_type = userpass\n'
        type_auth += f'password = {user.secret}\nusername = {user.username}\n\n'

        type_aor = f'[{user.username}]\ntype = aor\nmax_contacts = 1\nremove_existing = yes\n\n'

        result += comment + section + auth + aors + callerid + custom_settings
        result += '\n' + type_auth + type_aor
        result += '\n'

    return result


def make_pjsip_conf():

    plaintext = "; === This is auto generated file. Do not edit it. Use PBX13 admin panel! ===\n"
    plaintext += make_pjsip_conf_transports()
    plaintext += make_pjsip_conf_uplinks()
    plaintext += make_pjsip_conf_users_template()
    plaintext += make_pjsip_conf_users()

    return plaintext
