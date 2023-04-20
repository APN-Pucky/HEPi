:py:mod:`hepi.plot`
===================

.. py:module:: hepi.plot


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   plot/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.plot.Input



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.plot.get_output_dir
   hepi.plot.replace_macros
   hepi.plot.get_name
   hepi.plot.title
   hepi.plot.energy_plot
   hepi.plot.combined_mass_plot
   hepi.plot.combined_plot
   hepi.plot.mass_plot
   hepi.plot.mass_vplot
   hepi.plot.get_mass
   hepi.plot.plot
   hepi.plot.index_open
   hepi.plot.slha_data
   hepi.plot.slha_plot
   hepi.plot.vplot
   hepi.plot.mass_mapplot
   hepi.plot.mapplot
   hepi.plot.scatterplot
   hepi.plot.err_plt
   hepi.plot.scale_plot
   hepi.plot.central_scale_plot
   hepi.plot.init_double_plot



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.plot.map_vplot
   hepi.plot.scatter_vplot
   hepi.plot.fig
   hepi.plot.axs
   hepi.plot.lines
   hepi.plot.labels


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
