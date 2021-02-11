import logging

logger = logging.getLogger(__name__)


def validate_ldap_base_dn(ldap_base_dn):
    from account_manager.models import LdapUser
    LdapUser.creation_test(ldap_base_dn)
