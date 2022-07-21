# HELPER13

This module helps to configure local asterisk.
Listens on port XXXX with HTTP handler.
Wait for POST with the key
Executes the command received from allowed source with allowed key
For example, generates the asterisk configs, check the syntax of config files and restart asterisk.

I understand that this is not secure way, but I think if I can configure the allowed source (IP), allowed key (base64/HEX encoded Themis symmetric key), we can apply the command from executor and reply with the result.

