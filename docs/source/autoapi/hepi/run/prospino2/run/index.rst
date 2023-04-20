:py:mod:`hepi.run.prospino2.run`
================================

.. py:module:: hepi.run.prospino2.run


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.prospino2.run.ProspinoResult
   hepi.run.prospino2.run.ProspinoRunner




Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.prospino2.run.default_prospino_runner
   hepi.run.prospino2.run.run
   hepi.run.prospino2.run.set_path
   hepi.run.prospino2.run.get_path


.. py:class:: ProspinoResult(lo=None, nlo=None, nlo_plus_nll=None, annlo_plus_nnll=None)

   Bases: :py:obj:`hepi.results.Result`

   Prospino Result Data.

   Sets given and computes dependent ``Attributes``.

   :param lo: corresponds to :attr:`LO`.
   :type lo: :obj:`double`
   :param nlo: corresponds to :attr:`NLO`.
   :type nlo: :obj:`double`
   :param nlo_plus_nll: corresponds to :attr:`NLO_PLUS_NLL`.
   :type nlo_plus_nll: :obj:`double`
   :param annlo_plus_nnll: corresponds to :attr:`aNNLO_PLUS_NNLL`.
   :type annlo_plus_nnll: :obj:`double`


.. py:class:: ProspinoRunner(path, in_dir = None, out_dir = None, pre=None)

   Bases: :py:obj:`hepi.run.Runner`

   .. py:attribute:: weakino_map

      

   .. py:attribute:: squark_map

      

   .. py:attribute:: slepton_map

      

   .. py:method:: _get_ps_proc(p)


   .. py:method:: _get_ps_input(p)


   .. py:method:: orders()

      List of supported Orders in this runner.


   .. py:method:: _check_input(p, **kwargs)

      Checks input parameter for compatibility with Prospino


   .. py:method:: _is_valid(file, p, d)

      Verifies that a file is a complete output.

      :param file: File path to be parsed.
      :type file: str
      :param p: Onput parameters.
      :type p: :class:`hepi.Input`
      :param d: Param dictionary.
      :type d: :obj:`dict`

      :returns: True if `file` could be parsed.
      :rtype: bool


   .. py:method:: _parse_file(file)

      Extracts results from an output file.

      :param file: File path to be parsed.
      :type file: str

      :returns: If a value is not found in the file None is used.
      :rtype: :class:`Result`


   .. py:method:: _prepare(p, **kwargs)



.. py:data:: default_prospino_runner

   Default Prospino Runner to provide backward compatibility

.. py:data:: run

   

.. py:data:: set_path

   

.. py:data:: get_path

   
