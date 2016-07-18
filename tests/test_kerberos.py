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

import pytest
import sys

sys.path.append("../taiga-back/")

from unittest.mock import patch, Mock
from taiga_contrib_kerberos_auth import connector

def test_kerberos_login_success():
    with patch("taiga_contrib_kerberos_auth.connector.checkPassword") as m_checkPassword:

        m_checkPassword.return_value = Mock()

        email = "**user@example.com**"
        password = "**password**"
        (email, username) = connector.login(email, password)
        assert username == email.split('@')[0]


def test_kerberos_login_fail():
    with pytest.raises(connector.KERBEROSLoginError) as e:
        email = "**user@example.com**"
        password = "**password**"
        auth_info = connector.login(email, password)

    assert e.value.status_code == 400
    assert "error_message" in e.value.detail
