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

from kerberos import checkPassword

from django.conf import settings
from django.core.validators import EmailValidator
from taiga.base.connectors.exceptions import ConnectorBaseException


class KERBEROSLoginError(ConnectorBaseException):
    pass


REALM = getattr(settings, "KRB5_REALM", "")
ALLOWED_DOMAINS = getattr(settings, "KRB5_DOMAINS", "")

def login(email, password):

    allowed_domains = ALLOWED_DOMAINS + [REALM]

    validate_email = EmailValidator(whitelist=allowed_domains)

    try:
        validate_email(email)
    except ValidationError as err:
        errmsg, _ = err
        raise KERBEROSLoginError({"error_message": errmsg})

    username, domain = email.split('@')[1]

    if domain not in allowed_domains:
        errmsg = "Invalid e-mail: domain not allowed"
        raise KERBEROSLoginError({"error_message": errmsg})

    try:
        checkPassword(email, password, '', REALM)
    except kerberos.BasicAuthError as err:
        errmsg, _ = err
        if errmsg == "Cannot contact any KDC for requested realm":
            errmsg = "Error connecting to KERBEROS server"
            raise KERBEROSLoginError({"error_message": errmsg})
        elif errmsg == "Decrypt integrity check failed":
            errmsg = "KERBEROS account or password incorrect"
            raise KERBEROSLoginError({"error_message": errmsg})
    except Exception:
        errmsg = "KERBEROS authentication failed"
        raise KERBEROSLoginError({"error_message": errmsg})

    return (email, username)
