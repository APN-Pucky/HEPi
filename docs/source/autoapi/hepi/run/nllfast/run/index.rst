:py:mod:`hepi.run.nllfast.run`
==============================

.. py:module:: hepi.run.nllfast.run


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.nllfast.run.NLLfastRunner




Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.nllfast.run.default_nllfast_runner
   hepi.run.nllfast.run.run
   hepi.run.nllfast.run.set_path
   hepi.run.nllfast.run.get_path


.. py:class:: NLLfastRunner(path, in_dir = None, out_dir = None, pre=None)

   Bases: :py:obj:`hepi.run.Runner`

   .. py:method:: orders()

      List of supported Orders in this runner.


   .. py:method:: _get_nf_proc(p)


   .. py:method:: _get_nf_input(p)


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



.. py:data:: default_nllfast_runner

   Default Prospino Runner to provide backward compatibility

.. py:data:: run

   

.. py:data:: set_path

   

.. py:data:: get_path

   
