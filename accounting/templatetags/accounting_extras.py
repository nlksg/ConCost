from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='in_groups')
def in_groups(user, group_names):
    """Check if a user is in any of the given group names (comma-separated)."""
    if user.is_authenticated:
        group_list = [g.strip() for g in group_names.split(',')]
        return user.groups.filter(name__in=group_list).exists() or user.is_superuser
    return False

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def startswith(text, starts):
    """Returns True if the value starts with the given argument."""
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.simple_tag(takes_context=True)
def render_account_tree(context, account, level=0):
    output = []
    output.append('<tr{}>'.format(' class="table-secondary"' if not account.active else ''))
    output.append('<td><span style="display:inline-block; width:{}px;"></span>{}</td>'.format(level*20, account.account_code))
    output.append('<td>{}</td>'.format(account.name))
    output.append('<td>{}</td>'.format(account.get_type_display()))
    output.append('<td>{}</td>'.format(account.parent.name if account.parent else '-'))
    output.append('<td>{}</td>'.format('<span class="badge bg-success">Active</span>' if account.active else '<span class="badge bg-danger">Inactive</span>'))
    output.append('<td><a href="{}" class="btn btn-sm btn-outline-primary">View Ledger</a></td>'.format(account.get_ledger_url()))
    output.append('<td>')
    output.append('<a href="{}" class="btn btn-sm btn-outline-secondary">Edit</a> '.format(context['request'].build_absolute_uri('/accounts/{}/edit/'.format(account.pk))))
    output.append('<a href="{}" class="btn btn-sm btn-outline-success">Add Subaccount</a>'.format(context['request'].build_absolute_uri('/accounts/new/?parent={}'.format(account.pk))))
    output.append('</td></tr>')
    for child in getattr(account, '_children', []):
        output.append(render_account_tree(context, child, level+1))
    return mark_safe(''.join(output))

@register.filter(name='is_accountant_or_admin')
def is_accountant_or_admin(user):
    return user.groups.filter(name__in=['Accountant', 'Admin']).exists()
