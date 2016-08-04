# Copyright (C) 2016 <dpasqualin@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import kerberos

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from taiga.base.connectors.exceptions import ConnectorBaseException


class KERBEROSLoginError(ConnectorBaseException):
    pass


REALM = getattr(settings, "KRB5_REALM", "")
ALLOWED_DOMAINS = getattr(settings, "KRB5_DOMAINS", "")
DEFAULT_DOMAIN = getattr(settings, "KRB5_DEFAULT_DOMAIN", REALM)

def login(email, password):

    allowed_domains = ALLOWED_DOMAINS + [REALM]

    validate_email = EmailValidator(whitelist=allowed_domains)

    # user is allowed to type just the username. In this case, the REALM
    # will be appended as the domain to form a complete e-mail address
    if '@' in email:
        try:
            validate_email(email)
        except ValidationError as err:
            raise KERBEROSLoginError({"error_message": str(err)})

        username, domain = email.split('@')
    else:
        username, domain = email, DEFAULT_DOMAIN
        email = username + '@' + domain

    if domain not in allowed_domains:
        errmsg = "Invalid e-mail: domain not allowed"
        raise KERBEROSLoginError({"error_message": errmsg})

    try:
        kerberos.checkPassword(username, password, '', REALM)
    except kerberos.BasicAuthError as err:
        errmsg, _ = err.args
        if errmsg == "Cannot contact any KDC for requested realm":
            errmsg = "Error connecting to KERBEROS server"
            raise KERBEROSLoginError({"error_message": errmsg})
        elif errmsg == "Decrypt integrity check failed":
            errmsg = "KERBEROS account or password incorrect"
            raise KERBEROSLoginError({"error_message": errmsg})
        else:
            raise KERBEROSLoginError({"error_message": errmsg})
    except Exception:
        errmsg = "KERBEROS authentication failed"
        raise KERBEROSLoginError({"error_message": errmsg})

    return (email, username)
