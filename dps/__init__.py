from ._version import __version__

__all__ = ['__version__', 'get_checkout_inlines']


def get_checkout_inlines():
    from .admin import TransactionInlineAdmin
    return [TransactionInlineAdmin]
