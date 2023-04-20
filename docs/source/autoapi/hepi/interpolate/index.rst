:py:mod:`hepi.interpolate`
==========================

.. py:module:: hepi.interpolate


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hepi.interpolate.interpolate_1d
   hepi.interpolate.interpolate_2d



.. py:function:: interpolate_1d(df, x, y, xrange, only_interpolation=True)

   Last key is the value to be interpolated, while the rest are cooridnates.

   :param df: results
   :type df: pandas.DataFrame


.. py:function:: interpolate_2d(df, x, y, z, xrange, yrange, only_interpolation=True, **kwargs)

   Last key is the value to be interpolated, while the rest are cooridnates.

   :param df: results
   :type df: pandas.DataFrame
