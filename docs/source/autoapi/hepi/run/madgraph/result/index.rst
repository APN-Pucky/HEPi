:py:mod:`hepi.run.madgraph.result`
==================================

.. py:module:: hepi.run.madgraph.result


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.madgraph.result.MadgraphResult



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.run.madgraph.result.is_valid
   hepi.run.madgraph.result.parse_single



.. py:class:: MadgraphResult(lo, nlo)

   Bases: :py:obj:`hepi.run.Result`

   MadGraph Result Data.

   Sets LO and NLO result. NLO+NLL is set to None.


.. py:function:: is_valid(file, p, d)

   Verifies that an file is a complete output.

   :param file: File path to be parsed.
   :type file: str
   :param p: Input parameters.
   :type p: :class:`hepi.Input`
   :param d: Param dictionary.
   :type d: :obj:`dict`

   :returns: True if `file` could be parsed.
   :rtype: bool


.. py:function:: parse_single(file)

   Extracts Result from MadGraph output file.

   .. note:: This is only the result of one order. Therefore LO and NLO result in the return value are the same.

   :param file: File path to be parsed.
   :type file: str

   :returns: If a value is not found in the file None is used.
   :rtype: :class:`MadGraphResult`
