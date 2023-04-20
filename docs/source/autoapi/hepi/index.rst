:py:mod:`hepi`
==============

.. py:module:: hepi

.. autoapi-nested-parse::

   The HEPi package aims to automize cluster computations for parameter scans with the option to produce plots.



Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   data/index.rst
   plot/index.rst
   run/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   fast/index.rst
   input/index.rst
   interpolate/index.rst
   load/index.rst
   order/index.rst
   output/index.rst
   particles/index.rst
   results/index.rst
   util/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.Order
   hepi.DictData
   hepi.Input
   hepi.Input
   hepi.Order
   hepi.Input
   hepi.DictData
   hepi.Result
   hepi.Input
   hepi.Order
   hepi.Result
   hepi.DictData
   hepi.RunParam
   hepi.Runner
   hepi.DictData



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.order_to_string
   hepi.replace_macros
   hepi.xsec_to_order
   hepi.lhapdf_name_to_id
   hepi.get_input_dir
   hepi.get_output_dir
   hepi.get_pre
   hepi.set_input_dir
   hepi.set_output_dir
   hepi.set_pre
   hepi.is_gluino
   hepi.is_neutralino
   hepi.is_chargino
   hepi.is_weakino
   hepi.is_squark
   hepi.is_slepton
   hepi.update_slha
   hepi.scan
   hepi.scan_multi
   hepi.scan_scale
   hepi.scan_seven_point
   hepi.keep_where
   hepi.remove_where
   hepi.change_where
   hepi.scan_invariant_mass
   hepi.slha_write
   hepi.masses_scan
   hepi.mass_scan
   hepi.slha_scan
   hepi.slha_scan_rel
   hepi.scan_pdf
   hepi.interpolate_1d
   hepi.interpolate_2d
   hepi.order_to_string
   hepi.xsec_to_order
   hepi.DL2DF
   hepi.LD2DL
   hepi.load_json_with_metadata
   hepi.load_json
   hepi.order_to_string
   hepi.DL2DF
   hepi.write_latex_table_transposed_header
   hepi.write_latex_table_transposed
   hepi.write_latex
   hepi.write_csv
   hepi.write_json
   hepi.get_output_dir
   hepi.replace_macros
   hepi.get_name
   hepi.title
   hepi.energy_plot
   hepi.combined_mass_plot
   hepi.combined_plot
   hepi.mass_plot
   hepi.mass_vplot
   hepi.get_mass
   hepi.plot
   hepi.index_open
   hepi.slha_data
   hepi.slha_plot
   hepi.vplot
   hepi.mass_mapplot
   hepi.mapplot
   hepi.scatterplot
   hepi.err_plt
   hepi.scale_plot
   hepi.central_scale_plot
   hepi.init_double_plot
   hepi.pdf_errors
   hepi._pdf_error_single
   hepi.pdf_error
   hepi.scale_errors
   hepi._scale_error_single
   hepi.scale_error
   hepi.combine_errors
   hepi.combine_error
   hepi.get_input_dir
   hepi.get_output_dir
   hepi.get_pre
   hepi.DL2DF
   hepi.LD2DL
   hepi.namehash
   hepi.LD2DL
   hepi.DL2DF
   hepi.namehash
   hepi.lhapdf_name_to_id
   hepi.lhapdf_id_to_name



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.in_dir
   hepi.out_dir
   hepi.pre
   hepi.multi_scan
   hepi.scale_scan
   hepi.seven_point_scan
   hepi.pdf_scan
   hepi.load
   hepi.unv
   hepi.usd
   hepi.tex_table
   hepi.map_vplot
   hepi.scatter_vplot
   hepi.fig
   hepi.axs
   hepi.lines
   hepi.labels
   hepi.required_numerical_uncertainty_factor
   hepi.unv
   hepi.usd
   hepi.package
   hepi.__version__


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


.. py:function:: order_to_string(o, json_style=False, no_macros=False)


.. py:function:: replace_macros(s)


.. py:function:: xsec_to_order(s)


.. py:class:: DictData

   .. py:method:: __str__()

      Returns attributes as dict as string



.. py:function:: lhapdf_name_to_id(name)

   Converts a LHAPDF name to the sets id.

   :param name: LHAPDF set name.
   :type name: str

   :returns: id of the LHAPDF set.
   :rtype: int

   .. rubric:: Examples

   >>> lhapdf_name_to_id("CT14lo")
   13200


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

   

.. py:function:: interpolate_1d(df, x, y, xrange, only_interpolation=True)

   Last key is the value to be interpolated, while the rest are cooridnates.

   :param df: results
   :type df: pandas.DataFrame


.. py:function:: interpolate_2d(df, x, y, z, xrange, yrange, only_interpolation=True, **kwargs)

   Last key is the value to be interpolated, while the rest are cooridnates.

   :param df: results
   :type df: pandas.DataFrame


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



.. py:function:: order_to_string(o, json_style=False, no_macros=False)


.. py:function:: xsec_to_order(s)


.. py:function:: DL2DF(ld)

   Convert a `dict` of `list`s to a `pandas.DataFrame`.


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


.. py:function:: load_json_with_metadata(file)

   Load xsec data from json in to something that works within hepi's plotting.

   :param f: readable object, e.g. `open(filepath:str)`.
   :param dimensions: 1 or 2 currently supported.
   :type dimensions: int


.. py:function:: load_json(f, dimensions=1)


.. py:data:: load

   

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


.. py:function:: order_to_string(o, json_style=False, no_macros=False)


.. py:function:: DL2DF(ld)

   Convert a `dict` of `list`s to a `pandas.DataFrame`.


.. py:data:: unv

   

.. py:data:: usd

   

.. py:function:: write_latex_table_transposed_header(dict_list, t, fname, key, yscale=1.0)


.. py:function:: write_latex_table_transposed(dict_list, t, fname, scale=True, pdf=True, yscale=1.0, max_rows=None)


.. py:function:: write_latex(dict_list, t, key, fname, scale=True, pdf=True, yscale=1.0)

   Saves a `dict` of `list`s to `filename` as latex table.


.. py:data:: tex_table

   

.. py:function:: write_csv(dict_list, filename)

   Saves a `dict` of `list`s to `filename` as csv table.

   .. rubric:: Examples

   >>> import hepi
   >>> import urllib.request
   >>> dl = hepi.load(urllib.request.urlopen(
   ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
   ... ),dimensions=2)
   >>> hepi.write_csv(dl, open("test.csv", 'w'))
   >>> with open('test.csv', 'r') as f:
   ...     print(f.read())
   order,energy,energyhalf,particle1,particle2,slha,pdf_lo,pdfset_lo,pdf_nlo,pdfset_nlo,pdf_lo_id,pdf_nlo_id,mu_f,mu_r,precision,max_iters,invariant_mass,pt,result,id,model,mu,runner,N2,N1,NLO_PLUS_NLL_NOERR,NLO_PLUS_NLL_COMBINED
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,81.5,80.0,7.746232,7.746+/-0.023
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,82.0,80.0,7.646339,7.646+/-0.024
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,83.0,80.0,7.450843,7.451+/-0.024
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,85.0,80.0,7.079679,7.080+/-0.024
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,90.0,80.0,6.248933,6.249+/-0.025
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,95.0,80.0,5.53691,5.537+/-0.025
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,100.0,60.0,7.613015,7.613+/-0.024
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,100.0,80.0,4.924686,4.925+/-0.025
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,101.5,100.0,3.201246,3.201+/-0.026
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,102.0,100.0,3.169948,3.170+/-0.027
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,103.0,100.0,3.109625,3.110+/-0.027
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,105.0,100.0,2.993584,2.994+/-0.027
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,110.0,100.0,2.725548,2.726+/-0.027
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,110.0,80.0,3.933723,3.934+/-0.026
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,115.0,100.0,2.485705,2.486+/-0.028
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,120.0,100.0,2.271269,2.271+/-0.028
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,120.0,60.0,4.504708,4.505+/-0.025
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,120.0,80.0,3.180276,3.180+/-0.027
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,126.5,125.0,1.383578,1.384+/-0.030
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,127.0,125.0,1.373155,1.373+/-0.030
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,128.0,125.0,1.352257,1.352+/-0.031
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,130.0,100.0,1.905211,1.905+/-0.029
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,130.0,125.0,1.3128,1.313+/-0.031
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,135.0,125.0,1.219904,1.220+/-0.031
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,140.0,100.0,1.608394,1.608+/-0.029
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,140.0,125.0,1.134614,1.135+/-0.031
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,140.0,80.0,2.142151,2.142+/-0.028
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,145.0,125.0,1.056242,1.056+/-0.032
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,152.0,150.0,0.699925,0.700+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,153.0,150.0,0.691281,0.691+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,155.0,125.0,0.917808,0.918+/-0.032
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,155.0,150.0,0.674484,0.674+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,160.0,100.0,1.165897,1.166+/-0.031
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,160.0,150.0,0.6345,0.634+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,165.0,125.0,0.800281,0.800+/-0.033
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,165.0,150.0,0.597167,0.597+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,170.0,150.0,0.562441,0.562+/-0.035
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,178.0,175.0,0.391649,0.39+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,180.0,150.0,0.499633,0.500+/-0.035
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,180.0,175.0,0.383418,0.38+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,185.0,125.0,0.614697,0.615+/-0.034
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,185.0,175.0,0.363707,0.36+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,190.0,150.0,0.444892,0.44+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,190.0,175.0,0.345126,0.35+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,195.0,175.0,0.327625,0.33+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,202.0,200.0,0.2403,0.24+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,203.0,200.0,0.238047,0.24+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,205.0,200.0,0.233619,0.23+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,210.0,150.0,0.354984,0.35+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,210.0,200.0,0.222947,0.22+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,215.0,200.0,0.212818,0.21+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,220.0,200.0,0.203209,0.20+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,230.0,200.0,0.18536,0.19+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,230.0,225.0,0.150189,0.15+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,235.0,225.0,0.14399,0.14+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,240.0,200.0,0.169381,0.17+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,240.0,225.0,0.138083,0.14+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,252.0,250.0,0.102807,0.10+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,253.0,250.0,0.102017,0.10+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,255.0,250.0,0.100453,0.10+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,260.0,200.0,0.141817,0.14+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,260.0,250.0,0.096658,0.10+/-0.04
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,265.0,250.0,0.092955,0.09+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,270.0,250.0,0.089536,0.09+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,280.0,250.0,0.082931,0.08+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,290.0,250.0,0.076979,0.08+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,302.0,300.0,0.050316,0.05+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,303.0,300.0,0.049985,0.05+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,305.0,300.0,0.049326,0.05+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,310.0,250.0,0.066363,0.07+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,310.0,300.0,0.047719,0.05+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,315.0,300.0,0.046111,0.05+/-0.05
   2,13000.0,6500.0,-1,-1,$\tilde\chi_2^0\tilde\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.01,50,auto,auto,total,,,0.0,Resummino,320.0,300.0,0.044674,0.04+/-0.05
   <BLANKLINE>


.. py:function:: write_json(dict_list, o, parameters, output, error=True, error_sym=None, scale=True, pdf=True)

   Saves a `dict` of `list`s to `filename` as json.


   Cf. https://github.com/fuenfundachtzig/xsec


   :param output: Should support a function `.write()`.
   :type output: writeable or file name str

   .. rubric:: Examples

   >>> import hepi
   >>> import urllib.request
   >>> dl = hepi.load(urllib.request.urlopen(
   ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
   ... ),dimensions=2)
   >>> with open("test.json", "w") as f:
   ...     hepi.write_json(dl, Order.NLO_PLUS_NLL,["N1"],f,error=False)
   >>> with open('test.json', 'r') as f:
   ...     print(f.read())
   {
       "initial state": "pp",
       "order": "NLO+NLL",
       "source": "hepi-...",
       "contact": "...",
       "tool": "Resummino",
       "process_latex": "$\\overline{d}\\overline{d}$",
       "comment": "",
       "reference": "?",
       "Ecom [GeV]": "13000.0",
       "process_id": "pp_13000.0_-1_-1",
       "PDF set": "CTEQ6.6 and MSTW2008nlo90cl",
       "parameters": [
           [
               "N1"
           ]
       ],
       "data": {
           "80.0": {
               "xsec_pb": 2.142151
           },
           "60.0": {
               "xsec_pb": 4.504708
           },
           "100.0": {
               "xsec_pb": 1.165897
           },
           "125.0": {
               "xsec_pb": 0.614697
           },
           "150.0": {
               "xsec_pb": 0.354984
           },
           "175.0": {
               "xsec_pb": 0.327625
           },
           "200.0": {
               "xsec_pb": 0.141817
           },
           "225.0": {
               "xsec_pb": 0.138083
           },
           "250.0": {
               "xsec_pb": 0.066363
           },
           "300.0": {
               "xsec_pb": 0.044674
           }
       }
   }


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



.. py:function:: get_output_dir()

   Get the input directory.

   :returns: :attr:`out_dir`
   :rtype: str


.. py:function:: replace_macros(s)


.. py:function:: get_name(pid)

   Get the latex name of a particle.

   :param pid: PDG Monte Carlo identifier for the particle.
   :type pid: int

   :returns: Latex name.
   :rtype: str

   .. rubric:: Examples

   >>> get_name(21)
   'g'
   >>> get_name(1000022)
   '\\tilde{\\chi}_{1}^{0}'


.. py:function:: title(i, axe=None, scenario=None, diff_L_R=None, extra='', cms_energy=True, pdf_info=True, id=False, **kwargs)

   Sets the title on axis `axe`.


.. py:function:: energy_plot(dict_list, y, yscale=1.0, xaxis='E [GeV]', yaxis='$\\sigma$ [pb]', label=None, **kwargs)

   Plot energy on the x-axis.


.. py:function:: combined_mass_plot(dict_list, y, part, label=None, **kwargs)


.. py:function:: combined_plot(dict_list, x, y, label=None, **kwargs)


.. py:function:: mass_plot(dict_list, y, part, logy=True, yaxis='$\\sigma$ [pb]', yscale=1.0, label=None, xaxis=None, **kwargs)


.. py:function:: mass_vplot(dict_list, y, part, logy=True, yaxis='$\\sigma$ [pb]', yscale=1.0, label=None, mask=None, **kwargs)


.. py:function:: get_mass(l, iid)

   Get the mass of particle with id `iid` out of the list in the "slha" element in the dict.

   Returns
       :obj:`list` of float : masses of particles in each element of the dict list.



.. py:function:: plot(dict_list, x, y, label=None, xaxis='M [GeV]', yaxis='$\\sigma$ [pb]', ratio=False, K=False, K_plus_1=False, logy=True, yscale=1.0, mask=None, **kwargs)

   Creates a plot based on the entries `x`and `y` in `dict_list`.

   Examples

   .. plot::
       :include-source:

       >>> import urllib.request
       >>> import hepi
       >>> dl = hepi.load(urllib.request.urlopen(
       ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hino_NLO%2BNLL.json"
       ... ))
       >>> hepi.plot(dl,"N1","NLO_PLUS_NLL_COMBINED",xaxis="$m_{\\tilde{\\chi}_1^0}$ [GeV]")


.. py:function:: index_open(var, idx)


.. py:function:: slha_data(li, index_list)


.. py:function:: slha_plot(li, x, y, **kwargs)


.. py:function:: vplot(x, y, label=None, xaxis='E [GeV]', yaxis='$\\sigma$ [pb]', logy=True, yscale=1.0, interpolate=True, plot_data=True, data_color=None, mask=-1, fill=False, data_fmt='.', fmt='-', print_area=False, sort=True, **kwargs)

   Creates a plot based on the values in `x`and `y`.



.. py:function:: mass_mapplot(dict_list, part1, part2, z, logz=True, zaxis='$\\sigma$ [pb]', zscale=1.0, label=None)


.. py:function:: mapplot(dict_list, x, y, z, xaxis=None, yaxis=None, zaxis=None, **kwargs)

   Examples

   .. plot::
       :include-source:

       >>> import urllib.request
       >>> import hepi

       >>> dl = hepi.load(urllib.request.urlopen(
       ... "https://raw.githubusercontent.com/APN-Pucky/xsec/master/json/pp13_SGmodel_GGxsec_NLO%2BNLL.json"
       ... ),dimensions=2)
       >>> hepi.mapplot(dl,"gl","sq","NLO_PLUS_NLL_COMBINED",xaxis="$m_{\\tilde{g}}$ [GeV]",yaxis="$m_{\\tilde{q}}$ [GeV]" , zaxis="$\\sigma_{\\mathrm{NLO+NLL}}$ [pb]")


.. py:data:: map_vplot

   

.. py:data:: scatter_vplot

   

.. py:function:: scatterplot(dict_list, x, y, z, xaxis=None, yaxis=None, zaxis=None, **kwargs)

   Scatter map 2d.
   Central color is the central value, while the inner and outer ring are lower and upper bounds of the uncertainty interval.

   Examples

   .. plot::
       :include-source:

       >>> import urllib.request
       >>> import hepi
       >>> dl = hepi.load(urllib.request.urlopen(
       ... "https://raw.githubusercontent.com/APN-Pucky/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
       ... ),dimensions=2)
       >>> hepi.scatterplot(dl,"N1","N2","NLO_PLUS_NLL_COMBINED",xaxis="$m_{\\tilde{\\chi}_1^0}$ [GeV]",yaxis="$m_{\\tilde{\\chi}_2^0}$ [GeV]" , zaxis="$\\sigma_{\\mathrm{NLO+NLL}}$ [pb]")



.. py:data:: fig

   

.. py:data:: axs

   

.. py:data:: lines
   :value: []

   

.. py:data:: labels
   :value: []

   

.. py:function:: err_plt(axes, x, y, label=None, error=False)


.. py:function:: scale_plot(dict_list, vl, seven_point_band=False, cont=False, error=True, li=None, plehn_color=False, yscale=1.0, unit='pb', yaxis=None, **kwargs)

   Creates a scale variance plot with 5 panels (xline).


.. py:function:: central_scale_plot(dict_list, vl, cont=False, error=True, yscale=1.0, unit='pb', yaxis=None)

   Creates a scale variance plot with 3 panels (ystacked).


.. py:function:: init_double_plot(figsize=(6, 8), sharex=True, sharey=False, gridspec_kw={'height_ratios': [3, 1]})

   Initialze subplot for Ratio/K plots with another figure below.


.. py:class:: DictData

   .. py:method:: __str__()

      Returns attributes as dict as string



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


.. py:function:: DL2DF(ld)

   Convert a `dict` of `list`s to a `pandas.DataFrame`.


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


.. py:class:: DictData

   .. py:method:: __str__()

      Returns attributes as dict as string



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


.. py:class:: RunParam(skip = False, in_file = None, out_file = None, execute = None, name = None)

   Bases: :py:obj:`hepi.util.DictData`

   Abstract class that is similar to a dictionary but with fixed keys.


.. py:class:: Runner(path, in_dir = None, out_dir = None, pre=None)

   .. py:method:: orders()

      List of supported Orders in this runner.


   .. py:method:: get_name()

      Returns the name of the runner.


   .. py:method:: get_version()


   .. py:method:: _sub_run(coms)


   .. py:method:: _check_path()

      Checks if the passed path is valid.


   .. py:method:: _prepare(p, skip=False, assume_valid=False, **kwargs)


   .. py:method:: _check_input(param, **kwargs)


   .. py:method:: _prepare_all(params, skip=True, n_jobs=None, **kwargs)

      Prepares all parameters for execution.

      :param params: List of input parameters.
      :type params: List[:class:`hepi.Input`]
      :param skip: If True, the runner will check if the output file already exists and skip the execution if it does. Defaults to True.
      :type skip: bool, optional
      :param n_jobs: Number of parallel jobs. If None, use all available cores.
      :type n_jobs: int


   .. py:method:: run(params, skip=True, parse=True, parallel=True, sleep=0, run=True, ignore_error=False, n_jobs=None, **kwargs)

          Run the passed list of parameters.

          Args:
              params (:obj:`list` of :class:`hepi.Input`): All parameters that should be executed/queued.
              skip (bool): True means stored runs will be skipped. Else the are overwritten.
              parse (bool): Parse the results.
                  This is not the prefered cluster/parallel mode, as there the function only queues the job.
              parallel (bool): Run jobs in parallel.
              sleep (int): Sleep seconds after starting job.
      run (bool): Actually start/queue runner.
      ignore_error (bool): Continue instead of raising Exceptions. Also ignores hash collisions.
      n_jobs (int): Number of parallel jobs. If None, use all available cores.

          Returns:
              :obj:`pd.DataFrame` : combined dataframe of results and parameters. The dataframe is empty if `parse` is set to False.



   .. py:method:: _run(rps, wait=True, parallel=True, sleep=0, n_jobs=None, **kwargs)

          Runs Runner per :class:`RunParams`.

          Args:
              rps (:obj:`list` of :class:`RunParams`): Extended run parameters.
              bar (bool): Enable info bar.
              wait (bool): Wait for parallel runs to finish.
              sleep (int): Sleep seconds after starting subprocess.
              parallel (bool): Run jobs in parallel.
      n_jobs (int): Number of parallel jobs. If None, use all available cores.

          Returns:
              :obj:`list` of int: return codes from jobs if `no_parse` is False.


   .. py:method:: _is_valid(file, p, d, **kwargs)

      Verifies that a file is a complete output.

      :param file: File path to be parsed.
      :type file: str
      :param p: Onput parameters.
      :type p: :class:`hepi.Input`
      :param d: Param dictionary.
      :type d: :obj:`dict`

      :returns: True if `file` could be parsed.
      :rtype: bool


   .. py:method:: parse(outputs, n_jobs=None)

          Parses Resummino output files and returns List of Results.

          Args:
              outputs (:obj:`list` of `str`): List of the filenames to be parsed.
      n_jobs (int): Number of parallel jobs. If None, use all available cores.

          Returns:
              :obj:`list` of :class:`hepi.resummino.result.ResumminoResult`



   .. py:method:: _parse_file(file)

      Extracts results from an output file.

      :param file: File path to be parsed.
      :type file: str

      :returns: If a value is not found in the file None is used.
      :rtype: :class:`Result`


   .. py:method:: get_path()

      Get the Runner path.

      :returns: current Runner path.
      :rtype: str


   .. py:method:: get_input_dir()

      Get the input directory.

      :returns: :attr:`in_dir`
      :rtype: str


   .. py:method:: get_output_dir()

      Get the input directory.

      :returns: :attr:`out_dir`
      :rtype: str


   .. py:method:: get_pre()

      Gets the command prefix.

      :returns: :attr:`pre`
      :rtype: str


   .. py:method:: set_path(p)

      Set the path to the Runner folder containing the binary in './bin' or './build/bin'.

      :param p: new path.
      :type p: str


   .. py:method:: set_input_dir(indir)

      Sets the input directory.

      :param indir: new input directory.
      :type indir: str


   .. py:method:: set_output_dir(outdir, create = True)

      Sets the output directory.

      :param outdir: new output directory.
                     create (bool): create directory if not existing.
      :type outdir: str


   .. py:method:: set_pre(ppre)

      Sets the command prefix.

      :param ppre: new command prefix.
      :type ppre: str



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


.. py:data:: package
   :value: 'hepi'

   

.. py:data:: __version__

   
