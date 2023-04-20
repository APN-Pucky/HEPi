:py:mod:`hepi.order`
====================

.. py:module:: hepi.order


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.order.Order



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.order.replace_macros
   hepi.order.xsec_to_order
   hepi.order.order_to_string



.. py:class:: Order

   Bases: :py:obj:`enum.IntEnum`

   Computation orders.

   Initialize self.  See help(type(self)) for accurate signature.

   .. py:attribute:: LO
      :value: 0

      Leading Order

   .. py:attribute:: NLO
      :value: 1

      Next-to-Leading Order

   .. py:attribute:: NLO_PLUS_NLL
      :value: 2

      Next-to-Leading Order plus Next-to-Leading Logarithms

   .. py:attribute:: aNNLO_PLUS_NNLL
      :value: 3

      Approximate Next-to-next-to-Leading Order plus Next-to-next-to-Leading Logarithms


.. py:function:: replace_macros(s)


.. py:function:: xsec_to_order(s)


.. py:function:: order_to_string(o, json_style=False, no_macros=False)
