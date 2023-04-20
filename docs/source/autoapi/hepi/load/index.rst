:py:mod:`hepi.load`
===================

.. py:module:: hepi.load


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hepi.load.load_json_with_metadata
   hepi.load.load_json



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.load.load


.. py:function:: load_json_with_metadata(file)

   Load xsec data from json in to something that works within hepi's plotting.

   :param f: readable object, e.g. `open(filepath:str)`.
   :param dimensions: 1 or 2 currently supported.
   :type dimensions: int


.. py:function:: load_json(f, dimensions=1)


.. py:data:: load

   
