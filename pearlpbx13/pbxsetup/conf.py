from .models import SIPPeer, SIPTransport, SIPUser, Settings


def make_pjsip_conf_transports():
    result = '; ==== Transports section ====\n'
    transports = SIPTransport.objects.all()
    for transport in transports:
        description = '; ' + transport.description + '\n'
        section_name = f'[{transport.name}]\n'  # FIXME validate it
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


def __section_trunk_remote_registration(trunk: SIPPeer):
    result = '; Registration\n'
    result += f'[{trunk.name}]\n'
    result += 'type=registration\n'
    result += f'outbound_auth={trunk.name}\n'
    result += f'server_uri=sip:{trunk.host_port}\n'
    result += f'client_uri=sip:{trunk.username}@{trunk.host_port}\n'
    result += 'retry_interval=60\n'
    result += '\n'

    return result


def __section_trunk_auth_userpass(trunk: SIPPeer):
    result = '; Authentication\n'
    result += f'[{trunk.name}]\n'
    result += 'type=auth\n'
    result += 'auth_type=userpass\n'
    result += f'username={trunk.username}\n'
    result += f'password={trunk.secret}\n'
    result += '\n'

    return result


def __section_trunk_aor(trunk: SIPPeer):
    result = '; AOR\n'
    result += f'[{trunk.name}]\n'
    result += 'type=aor\n'
    result += f'contact=sip:{trunk.host_port}\n'
    result += '\n'

    return result


def __section_trunk_endpoint(trunk: SIPPeer):
    result = '; Endpoint\n'
    result += f'[{trunk.name}]\n'
    result += 'type=endpoint\n'
    result += f'transport={trunk.transport.name}\n'
    result += f'context=from-{trunk.name}\n'
    result += 'disallow=all\n'
    result += 'allow=ulaw,alaw\n'  # TODO list ALLOWED codecs
    if trunk.registrationThere == True:
        result += f'outbound_auth={trunk.name}\n'

    if trunk.registrationHere == True or trunk.registrationThere == False:
        result += f'auth={trunk.name}\n'

    result += f'aors={trunk.name}\n'
    result += '\n'

    return result


def __section_trunk_identify(trunk: SIPPeer):
    result = '; Identify\n'
    result += f'[{trunk.name}]\n'
    result += 'type=identify\n'
    result += f'endpoint={trunk.name}\n'
    result += f'match={trunk.host_port}\n'
    result += '\n'

    return result


def make_pjsip_conf_uplinks():
    result = '; ==== Uplinks section ====\n'

    trunks = SIPPeer.objects.all()
    for trunk in trunks:
        comment = '; ' + trunk.name + '\n'
        result += comment
        # registration
        result += __section_trunk_remote_registration(
            trunk) if trunk.registrationThere else '; do not register on the remote side\n'

        # auth
        result += __section_trunk_auth_userpass(trunk)
        # aor
        result += __section_trunk_aor(trunk)
        # endpoint
        result += __section_trunk_endpoint(trunk)
        # identify
        result += __section_trunk_identify(trunk)

        result += '\n'

    result += '\n'
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
        section += f'transport={user.transport.name}\n'
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
