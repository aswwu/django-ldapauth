"""
TODO
====

* django_user_set_for_ldap_group doesn't return users from a group within a group

"""
import re
from django.contrib.auth.models import Group, User
from django.db.models import Q
from ldapauth import LDAP


cn_re = re.compile(r'CN=(.*?),')
def get_common_name(distinguished_name):
    """
    Parse out the common name (CN) of an LDAP distinguished name (DN).

    Here are some examples of what LDAP distinguished names look like:

    "CN=Lafayette Something,OU=employees,..."
    "CN=fitzgen,OU=students,..."
    """
    return cn_re.findall(distinguished_name)[0]


def get_users_by_distinguished_name(distinguished_names):
    """
    Takes a list of LDAP distinguished names (DNs) and returns a Django User
    queryset for all of those group members.
    """
    # TODO: create Django instances for members who don't have one.
    members = map(get_common_name, distinguished_names)
    full_names = set([m for m in members if len(m.split(" ")) == 2])
    user_names = set(members).difference(full_names)
    full_names = [m.split(" ") for m in full_names]

    def join_one_query(query_obj, name_pair):
        """
        Join one [first, last] name pair queryset to the query object.
        """
        first = name_pair[0]
        last = name_pair[1]
        return query_obj | Q(first_name=first, last_name=last)

    return User.objects.filter(reduce(join_one_query,
                                      full_names,
                                      Q(username__in=user_names)))


def django_user_set_for_ldap_group(group):
    """
    Return a django User model's queryset representing all the users in `group`.

    `group` can be either a string that is the name of a group, or a Django
    Group model instance.
    """
    if isinstance(group, basestring):
        group_name = group
    elif isinstance(group, Group):
        group_name = group.name
    else:
        raise TypeError("""\
The `group` argument must be either a string that is the name of a group, or a
Django Group model instance. Found: %s\
""" % type(group))

    group = LDAP("wwu").search_groups(
        group_name,
        ["member"]
    )[0]

    # Attribute "member" won't exist if there are no users in the group.
    if hasattr(group, "member"):
        return get_users_by_distinguished_name(group.member)
    else:
        return User.objects.none()

def is_member(user, group_list=[]):
    person = LDAP("wwu").get_person_by_username(user)
    return bool(set(group_list).intersection(set(person.groups)))

def get_user_groups(user):
    person = LDAP("wwu").get_person_by_username(user)
    return getattr(person, "groups", [])
