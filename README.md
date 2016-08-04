Taiga contrib kerberos auth
=======================

The Taiga plugin for kerberos authentication.

Installation
------------

### Taiga Back

In your Taiga back, first install `libkrb5-dev` with the following command:

```bash
  sudo apt-get install libkrb5-dev
```

Then, in the python virtualenv install the pip package:
`taiga-contrib-kerberos-auth` with:

```bash
  pip install taiga-contrib-kerberos-auth
```

Finally, modify your `settings/local.py` and include it on `INSTALLED_APPS` and add your
KERBEROS configuration:

```python
  INSTALLED_APPS += ['taiga_contrib_kerberos_auth']

  # kerberos realm
  KRB5_REALM = 'EXAMPLE.COM'

  # Allow users from any of these domains to connect to KRB5_REALM
  # If empty, only e-mails such as user@EXAMPLE.COM will be allowed
  KRB5_DOMAINS = ['example.com']

  # When the user provide only username, assume this domain.
  # This is useful when REALM is not a valid e-mail. Leave blank to use
  # KRB5_REALM as the default domain
  KRB5_DEFAULT_DOMAIN = ""

```

### Taiga Front

Change in your `dist/js/conf.json` the `loginFormType` setting to `"kerberos"`:

```json
...
    "loginFormType": "kerberos",
...
```


### Credits:

Based on ldap code fom [enskylin](https://github.com/ensky/taiga-contrib-ldap-auth)
