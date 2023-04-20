:py:mod:`hepi.run.nllfast.result`
=================================

.. py:module:: hepi.run.nllfast.result


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.nllfast.result.NLLFastResult




.. py:class:: NLLFastResult(lo, nlo, nlo_plus_nll, scale_err_up, scale_err_down, pdf_err_up, pdf_err_down)

   Bases: :py:obj:`hepi.results.Result`

   (N)NLL-fast Result Data.

   Sets given and computes dependent ``Attributes``.

   :param lo: corresponds to :attr:`LO`.
   :type lo: :obj:`double`
   :param nlo: corresponds to :attr:`NLO`.
   :type nlo: :obj:`double`
   :param nlo_plus_nll: corresponds to :attr:`NLO_PLUS_NLL`.
   :type nlo_plus_nll: :obj:`double`
   :param annlo_plus_nnll: corresponds to :attr:`aNNLO_PLUS_NNLL`.
   :type annlo_plus_nnll: :obj:`double`
