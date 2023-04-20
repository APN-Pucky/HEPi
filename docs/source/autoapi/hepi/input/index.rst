:py:mod:`hepi.input`
====================

.. py:module:: hepi.input


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.input.Input



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.input.get_input_dir
   hepi.input.get_output_dir
   hepi.input.get_pre
   hepi.input.set_input_dir
   hepi.input.set_output_dir
   hepi.input.set_pre
   hepi.input.is_gluino
   hepi.input.is_neutralino
   hepi.input.is_chargino
   hepi.input.is_weakino
   hepi.input.is_squark
   hepi.input.is_slepton
   hepi.input.update_slha
   hepi.input.scan
   hepi.input.scan_multi
   hepi.input.scan_scale
   hepi.input.scan_seven_point
   hepi.input.keep_where
   hepi.input.remove_where
   hepi.input.change_where
   hepi.input.scan_invariant_mass
   hepi.input.slha_write
   hepi.input.masses_scan
   hepi.input.mass_scan
   hepi.input.slha_scan
   hepi.input.slha_scan_rel
   hepi.input.scan_pdf



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.input.in_dir
   hepi.input.out_dir
   hepi.input.pre
   hepi.input.multi_scan
   hepi.input.scale_scan
   hepi.input.seven_point_scan
   hepi.input.pdf_scan


.. py:data:: in_dir
   :value: './input/'

   Input directory.

.. py:data:: out_dir
   :value: './output/'

   Output directory.

.. py:data:: pre
   :value: 'nice -n 5'

   Prefix for run commands.

.. py:function:: get_input_dir()

   Get the input directory.

   :returns: :attr:`in_dir`
   :rtype: str


.. py:function:: get_output_dir()

   Get the input directory.

   :returns: :attr:`out_dir`
   :rtype: str


.. py:function:: get_pre()

   Gets the command prefix.

   :returns: :attr:`pre`
   :rtype: str


.. py:function:: set_input_dir(ind)

   Sets the input directory.

   :param ind: new input directory.
   :type ind: str


.. py:function:: set_output_dir(outd, create = True)

   Sets the output directory.

   :param outd: new output directory.
                create (bool): create directory if not existing
   :type outd: str


.. py:function:: set_pre(ppre)

   Sets the command prefix.

   :param ppre: new command prefix.
   :type ppre: str


.. py:class:: Input(order, energy, particle1, particle2, slha, pdf_lo, pdf_nlo, mu_f=1.0, mu_r=1.0, pdfset_lo=0, pdfset_nlo=0, precision=0.01, max_iters=50, invariant_mass='auto', result='total', pt='auto', id='', model='', update=True)

   Bases: :py:obj:`hepi.util.DictData`

   Input for computation and scans.

   :ivar order: LO, NLO or NLO+NLL computation.
   :vartype order: :class:`Order`
   :ivar energy: CMS energy in GeV.
   :vartype energy: int
   :ivar energyhalf: Halfed `energy`.
   :vartype energyhalf: int
   :ivar particle1: PDG identifier of the first final state particle.
   :vartype particle1: int
   :ivar particle2: PDG identifier of the second final state particle.
   :vartype particle2: int
   :ivar slha: File path of for the base slha.
               Modified slha files will be used if a scan requires a change of the input.
   :vartype slha: str
   :ivar pdf_lo: LO PDF name.
   :vartype pdf_lo: str
   :ivar pdf_nlo: NLO PDF name.
   :vartype pdf_nlo: str
   :ivar pdfset_lo: LO PDF member/set id.
   :vartype pdfset_lo: int
   :ivar pdfset_nlo: NLO PDF member/set id.
   :vartype pdfset_nlo: int
   :ivar pdf_lo_id: LO PDF first member/set id.
   :vartype pdf_lo_id: int
   :ivar pdf_nlo_id: NLO PDF first member/set id.
   :vartype pdf_nlo_id: int
   :ivar mu: central scale factor.
   :vartype mu: double
   :ivar mu_f: Factorization scale factor.
   :vartype mu_f: double
   :ivar mu_r: Renormalization scale factor.
   :vartype mu_r: double
   :ivar precision: Desired numerical relative precision.
   :vartype precision: double
   :ivar max_iters: Upper limit on integration iterations.
   :vartype max_iters: int
   :ivar invariant_mass: Invariant mass mode 'auto = sqrt((p1+p2)^2)' else value.
   :vartype invariant_mass: str
   :ivar pt: Transverse Momentum mode 'auto' or value.
   :vartype pt: str
   :ivar result: Result type 'total'/'pt'/'ptj'/'m'.
   :vartype result: str
   :ivar id: Set an id of this run.
   :vartype id: str
   :ivar model: Path for MadGraph model.
   :vartype model: str
   :ivar update: Update dependent `mu` else set to zero.

   :vartype update: bool

   .. py:method:: has_gluino()


   .. py:method:: has_neutralino()


   .. py:method:: has_charginos()


   .. py:method:: has_weakino()


   .. py:method:: has_squark()


   .. py:method:: has_slepton()



.. py:function:: is_gluino(iid)


.. py:function:: is_neutralino(iid)


.. py:function:: is_chargino(iid)


.. py:function:: is_weakino(iid)


.. py:function:: is_squark(iid)


.. py:function:: is_slepton(iid)


.. py:function:: update_slha(i)

   Updates dependent parameters in Input `i`.

   Mainly concerns the `mu` value used by `madgraph`.


.. py:function:: scan(input_list, var, rrange)

   Scans a variable `var` over `rrange` in `input_list`.

   .. note:: This function does not ensure that dependent vairables are updated (see `energyhalf` in Examples).

   :param input_list: Input parameters that get scanned each.
   :type input_list: :obj:`list` of :class:`Input`
   :param var: Scan variable name.
   :type var: str
   :param rrange: Range of `var` to be scanned.
   :type rrange: Iterable

   :returns: Modified list with scan runs added.
   :rtype: :obj:`list` of :class:`Input`

   .. rubric:: Examples

   >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
   >>> li = scan(li,"energy",range(10000,13000,1000))
   >>> for e in li:
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   >>> for e in scan(li,"order",[Order.LO,Order.NLO,Order.NLO_PLUS_NLL]):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:function:: scan_multi(li, **kwargs)

   Magically scans the variables passed to this function.

   :param \*\*kwargs:

   .. rubric:: Examples

   >>> oli = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
   >>> li = scan_multi(oli,energy=range(10000,13000,1000))
   >>> for e in li:
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   >>> for e in scan_multi(oli,energy=range(10000,13000,1000),order=[Order.LO,Order.NLO,Order.NLO_PLUS_NLL]):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:data:: multi_scan

   

.. py:function:: scan_scale(l, rrange=3, distance=2.0)

   Scans scale by varying `mu_f` and `mu_r`.

   They take `rrange` values from 1/`distance` to `distance` in lograthmic spacing.
   Only points with `mu_f`=`mu_r` or `mu_r/f`=1 or `mu_r/f`=`distance` or `mu_r/f`=1/`distance` are returned.

   .. rubric:: Examples

   >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
   >>> for e in scan_scale(li):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:data:: scale_scan

   

.. py:function:: scan_seven_point(input_list)

   Scans scale by varying `mu_f` and `mu_r` by factors of two excluding relative factors of 4.

   .. rubric:: Examples

   >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
   >>> for e in scan_seven_point(li):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:data:: seven_point_scan

   

.. py:function:: keep_where(input_list, condition)

   Only keep the inputs where the condition is true.

   Inversion of the `remove_where` function.

   :param input_list: List[Input]
                      The list of inputs to filter.
   :param condition: Callable[[Input.__dict__], bool]
                     The condition to filter on.


.. py:function:: remove_where(input_list, condition, **kwargs)

   Remove elements in list which satisfy condition.

   :param input_list: List[Input]
                      The list of inputs to filter.
   :param condition: Callable[[Input.__dict__], bool]
                     The condition to filter on.

   .. rubric:: Examples

   >>> li = scan_multi([Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)],energy=range(10000,13000,1000))
   >>> for e in remove_where(li,lambda dict : (dict["energy"] == 10000 or dict["energy"] == 11000)):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:function:: change_where(input_list, dicts, **kwargs)

   Applies the values of `dicts` if the key value pairs in `kwargs` agree with a member of the list `input_list`.

   The changes only applied to the matching list members.

   .. rubric:: Examples

   >>> li = scan_multi([Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)],energy=range(10000,13000,1000))
   >>> for e in change_where(li,{'order':Order.NLO},energy=11000):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   >>> li = scan_multi([Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)],energy=range(10000,12000,1000),mu_f=range(1,3))
   >>> for e in change_where(li,{'order':Order.NLO},energy=11000,mu_f=1):
   ...     print(e)
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:function:: scan_invariant_mass(input_list, diff, points, low=0.001)

   Logarithmic `invariant_mass` scan close to the production threshold.


.. py:function:: slha_write(newname, d)


.. py:function:: masses_scan(input_list, varis, rrange, diff_L_R=None, negate=None)

   Scans the PDG identified masses in `varis` over `rrange` in the list `input_list`.
   `diff_L_R` allows to set a fixed difference between masses of left- and right-handed particles.


.. py:function:: mass_scan(input_list, var, rrange, diff_L_R=None)

   Scans the PDG identified mass `var` over `rrange` in the list `l`.
   `diff_L_R` allows to set a fixed difference between masses of left- and right-handed particles.


.. py:function:: slha_scan(input_list, block, var, rrange)

   Scan a generic


.. py:function:: slha_scan_rel(input_list, lambdas, rrange)

   Scan a generic slha variable.


.. py:function:: scan_pdf(input_list)

   Scans NLO PDF sets.

   The PDF sets are infered from `lhapdf.getPDFSet` with the argument of `pdfset_nlo`.

   .. rubric:: Examples

   >>> li = [Input(Order.NLO, 13000,  1000022,1000022, "None", "CT14lo","CT14nlo",update=False)]
   >>> for e in scan_pdf(li):
   ...     print(e)
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 1, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 2, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 3, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 4, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 5, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 6, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 7, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 8, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 9, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 10, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 11, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 12, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 13, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 14, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 15, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 16, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 17, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 18, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 19, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 20, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 21, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 22, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 23, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 24, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 25, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 26, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 27, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 28, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 29, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 30, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 31, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 32, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 33, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 34, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 35, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 36, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 37, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 38, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 39, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 40, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 41, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 42, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 43, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 44, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 45, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 46, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 47, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 48, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 49, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 50, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 51, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 52, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 53, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 54, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 55, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}
   {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 56, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model': '', 'mu': 0.0}


.. py:data:: pdf_scan

   
