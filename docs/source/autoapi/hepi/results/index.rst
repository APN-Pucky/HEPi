:py:mod:`hepi.results`
======================

.. py:module:: hepi.results

.. autoapi-nested-parse::

   Results and postprocessing for the :mod:`hepi` package.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.results.Result



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.results.pdf_errors
   hepi.results._pdf_error_single
   hepi.results.pdf_error
   hepi.results.scale_errors
   hepi.results._scale_error_single
   hepi.results.scale_error
   hepi.results.combine_errors
   hepi.results.combine_error



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.results.required_numerical_uncertainty_factor
   hepi.results.unv
   hepi.results.usd


.. py:data:: required_numerical_uncertainty_factor
   :value: 5

   

.. py:data:: unv

   

.. py:data:: usd

   

.. py:class:: Result(lo=None, nlo=None, nlo_plus_nll=None, annlo_plus_nnll=None)

   Bases: :py:obj:`hepi.util.DictData`

   General result class. All uncertainties are of numerical origin.

   :ivar LO: Leading Order result. Defaults to None.
   :vartype LO: :obj:`double`
   :ivar NLO: Next-to-Leading Order result. Defaults to None.
   :vartype NLO: :obj:`double`
   :ivar NLO_PLUS_NLL: Next-to-Leading Order plus Next-to-Leading Logarithm result. Defaults to None.
   :vartype NLO_PLUS_NLL: :obj:`double`
   :ivar K_LO: LO divided by LO.
   :vartype K_LO: :obj:`double`
   :ivar K_NLO: NLO divided by LO result.
   :vartype K_NLO: :obj:`double`
   :ivar K_NLO_PLUS_NLL: NLO+NLL divided by LO.
   :vartype K_NLO_PLUS_NLL: :obj:`double`
   :ivar K_aNNLO_PLUS_NNLL: aNNLO+NNLL divided by LO.
   :vartype K_aNNLO_PLUS_NNLL: :obj:`double`
   :ivar NLO_PLUS_NLL_OVER_NLO: NLO+NLL divided by NLO.
   :vartype NLO_PLUS_NLL_OVER_NLO: :obj:`double`
   :ivar aNNLO_PLUS_NNLL_OVER_NLO: aNNLO+NNLL divided by NLO.

   :vartype aNNLO_PLUS_NNLL_OVER_NLO: :obj:`double`

   Sets given and computes dependent ``Attributes``.

   :param lo: corresponds to :attr:`LO`.
   :type lo: :obj:`double`
   :param nlo: corresponds to :attr:`NLO`.
   :type nlo: :obj:`double`
   :param nlo_plus_nll: corresponds to :attr:`NLO_PLUS_NLL`.
   :type nlo_plus_nll: :obj:`double`
   :param annlo_plus_nnll: corresponds to :attr:`aNNLO_PLUS_NNLL`.
   :type annlo_plus_nnll: :obj:`double`


.. py:function:: pdf_errors(li, dl, ordernames=None, confidence_level=90, n_jobs=None)

   Just like `pdf_error` but over a list of ordernames.


.. py:function:: _pdf_error_single(members, i, dl, ordername, confidence_level=90)


.. py:function:: pdf_error(li, dl, ordername='LO', confidence_level=90, n_jobs=None)

   Computes Parton Density Function (PDF) uncertainties through :func:`lhapdf.set.uncertainty`.

   :param li: Input list.
   :type li: :obj:`list` of :class:`Input`
   :param dl: :class:`Result` dictionary with lists per entry.
   :type dl: :obj:`dict`
   :param ordername: Name of the order.
   :type ordername: `str`
   :param confidence_level: Confidence Level for PDF uncertainty
   :type confidence_level: :obj:`double`

   :returns:

             Modified `dl` with new `ordername_{PDF,PDF_CENTRAL,PDF_ERRPLUS,PDF_ERRMINUS,PDF_ERRSYM}` entries.
                 - (`ordername`)_`PDF` contains a symmetrized :mod:`uncertainties` object.
   :rtype: :obj:`dict`


.. py:function:: scale_errors(li, dl, ordernames=None, n_jobs=None)

   Just like `scale_error` but over a list of ordernames.


.. py:function:: _scale_error_single(members, i, dl, ordername='LO')


.. py:function:: scale_error(li, dl, ordername='LO', n_jobs=None)

   Computes seven-point scale uncertainties from the results where the renormalization and factorization scales are varied by factors of 2 and  relative factors of four are excluded (cf. :meth:`seven_point_scan`).

   :param li: Input list.
   :type li: :obj:`list` of :class:`Input`
   :param dl: :class:`Result` dictionary with lists per entry.
   :type dl: :obj:`dict`

   :returns:

             Modified `dl` with new `ordername_{SCALE,SCALE_ERRPLUS,SCALE_ERRMINUS}` entries.
                 - `ordername_SCALE` contains a symmetrized :mod:`uncertainties` object.
   :rtype: :obj:`dict`


.. py:function:: combine_errors(dl, ordernames=None)

   Just like `combine_error` but over a list of ordernames.


.. py:function:: combine_error(dl, ordername='LO')

   Combines seven-point scale uncertainties and pdf uncertainties from the results by Pythagorean addition.

   .. note:: Running :func:`scale_errors` and :func:`pdf_errors` before is necessary.

   :param dl: :class:`Result` dictionary with lists per entry.
   :type dl: :obj:`dict`

   :returns:

             Modified `dl` with new `ordername_{COMBINED,ERRPLUS,ERRMINUS}` entries.
                 - `ordername_COMBINED` contains a symmetrized :mod:`uncertainties` object.
   :rtype: :obj:`dict`
