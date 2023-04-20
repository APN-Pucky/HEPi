:py:mod:`hepi.plot.plot`
========================

.. py:module:: hepi.plot.plot


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hepi.plot.plot.title
   hepi.plot.plot.energy_plot
   hepi.plot.plot.combined_mass_plot
   hepi.plot.plot.combined_plot
   hepi.plot.plot.mass_plot
   hepi.plot.plot.mass_vplot
   hepi.plot.plot.get_mass
   hepi.plot.plot.plot
   hepi.plot.plot.index_open
   hepi.plot.plot.slha_data
   hepi.plot.plot.slha_plot
   hepi.plot.plot.vplot
   hepi.plot.plot.mass_mapplot
   hepi.plot.plot.mapplot
   hepi.plot.plot.scatterplot
   hepi.plot.plot.err_plt
   hepi.plot.plot.scale_plot
   hepi.plot.plot.central_scale_plot
   hepi.plot.plot.init_double_plot



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.plot.plot.map_vplot
   hepi.plot.plot.scatter_vplot
   hepi.plot.plot.fig
   hepi.plot.plot.axs
   hepi.plot.plot.lines
   hepi.plot.plot.labels


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
