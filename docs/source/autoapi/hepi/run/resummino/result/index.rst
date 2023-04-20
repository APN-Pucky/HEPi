:py:mod:`hepi.run.resummino.result`
===================================

.. py:module:: hepi.run.resummino.result


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.resummino.result.ResumminoResult



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.run.resummino.result.is_valid
   hepi.run.resummino.result.parse_single



.. py:class:: ResumminoResult(lo, nlo, nlo_plus_nll, annlo_plus_nnll, vnlo, p_plus_k, rnlog, rnloq)

   Bases: :py:obj:`hepi.run.Result`

   Resummino Result Data.

   :ivar VNLO: virtual NLO result.
   :vartype VNLO: double
   :ivar RNLO: real NLO result.
   :vartype RNLO: double
   :ivar P_PLUS_K: collineare remainders P+K NLO result.
   :vartype P_PLUS_K: double
   :ivar RNLOG: real NLO gluon result.
   :vartype RNLOG: double
   :ivar RNLOQ: real NLO quark result.
   :vartype RNLOQ: double
   :ivar VNLO_PLUS_P_PLUS_K: VNLO+P+K result.
   :vartype VNLO_PLUS_P_PLUS_K: double
   :ivar RNLO_PLUS_VNLO_PLUS_P_PLUS_K: RNLO+VNLO+P+K result.

   :vartype RNLO_PLUS_VNLO_PLUS_P_PLUS_K: double

   Sets given and computes dependent ``Attributes``.

   :param lo: corresponds to :attr:`LO`.
   :type lo: :obj:`double`
   :param nlo: corresponds to :attr:`NLO`.
   :type nlo: :obj:`double`
   :param nlo_plus_nll: corresponds to :attr:`NLO_PLUS_NLL`.
   :type nlo_plus_nll: :obj:`double`
   :param vnlo: corresponds to :attr:`VNLO`.
   :type vnlo: :obj:`double`
   :param p_plus_k: corresponds to :attr:`P_PLUS_K`.
   :type p_plus_k: :obj:`double`
   :param rnlog: corresponds to :attr:`RNLOG`.
   :type rnlog: :obj:`double`
   :param rnloq: corresponds to :attr:`RNLOQ`.
   :type rnloq: :obj:`double`


.. py:function:: is_valid(file, p, d, **kwargs)

   Verifies that an file is a complete output.

   :param file: File path to be parsed.
   :type file: str
   :param p: Onput parameters.
   :type p: :class:`hepi.Input`
   :param d: Param dictionary.
   :type d: :obj:`dict`

   :returns: True if `file` could be parsed.
   :rtype: bool


.. py:function:: parse_single(file)

   Extracts LO, NLO and NLO+NLL from Resummino output file.

   :param file: File path to be parsed.
   :type file: str

   :returns: If a value is not found in the file None is used.
   :rtype: :class:`ResumminoResult`
