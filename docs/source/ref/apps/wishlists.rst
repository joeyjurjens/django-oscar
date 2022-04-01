=========
Wishlists
=========

The wishlists app allows signed-in users to create one or more wishlists.  A
user can add a product to their wishlist from the product detail page and manage
their lists in the account section.

A wishlist can be private, public or shared. Private wishlist can only be seen by the owner of the wishlist, where public wishlists can be seen by anyone with the link. Shared wishlists have extra configuration, the owner of the wislist can add emails that are allowed to see the wishlist, this would still require an account with this email.

The wishlists app is wired up as a subapp of :doc:`customer` for the customer wish list related views.

Abstract models
---------------

.. automodule:: oscar.apps.wishlists.abstract_models
    :members:

Views
-----

.. automodule:: oscar.apps.customer.wishlists.views
    :members:
