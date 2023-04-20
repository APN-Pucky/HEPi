:py:mod:`hepi.util`
===================

.. py:module:: hepi.util

.. autoapi-nested-parse::

   Collection of utility functions for the :mod:`hepi` package.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.util.DictData



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.util.LD2DL
   hepi.util.DL2DF
   hepi.util.namehash
   hepi.util.lhapdf_name_to_id
   hepi.util.lhapdf_id_to_name



.. py:class:: DictData

   .. py:method:: __str__()

      Returns attributes as dict as string



.. py:function:: LD2DL(l, actual_dict=False)

   Convert a list of objects into a dictionary of lists.

   The values of each object are first converted to a `dict` through the `__dict__` attribute.

   :param l: list of objects.
   :type l: List
   :param actual_dict: objects are already dicts
   :type actual_dict: bool

   :returns: dictionary of numpy arrays.
   :rtype: dict

   .. rubric:: Examples

   >>> class Param:
   ...      def __init__(self,a,b,c):
   ...         self.a = a
   ...         self.b = b
   ...         self.c = c
   >>> LD2DL([ Param(1,2,3), Param(4,5,6) , Param(7,8,9) ])
   {'a': array([1, 4, 7]), 'b': array([2, 5, 8]), 'c': array([3, 6, 9])}


.. py:function:: DL2DF(ld)

   Convert a `dict` of `list`s to a `pandas.DataFrame`.


.. py:function:: namehash(n)

   Creates a sha256 hash from the objects string representation.

   :param n: object.
   :type n: any

   :returns: sha256 of object.
   :rtype: str

   .. rubric:: Examples

   >>> p = {'a':1,'b':2}
   >>> str(p)
   "{'a': 1, 'b': 2}"
   >>> namehash(str(p))
   '3dffaea891e5dbadb390da33bad65f509dd667779330e2720df8165a253462b8'
   >>> namehash(p)
   '3dffaea891e5dbadb390da33bad65f509dd667779330e2720df8165a253462b8'


.. py:function:: lhapdf_name_to_id(name)

   Converts a LHAPDF name to the sets id.

   :param name: LHAPDF set name.
   :type name: str

   :returns: id of the LHAPDF set.
   :rtype: int

   .. rubric:: Examples

   >>> lhapdf_name_to_id("CT14lo")
   13200


.. py:function:: lhapdf_id_to_name(lid)
