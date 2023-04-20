:py:mod:`hepi.run.resummino.run`
================================

.. py:module:: hepi.run.resummino.run

.. autoapi-nested-parse::

   Runs Resummino



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.resummino.run.ResumminoRunner




Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.resummino.run.default_resummino_runner
   hepi.run.resummino.run.run
   hepi.run.resummino.run.set_path
   hepi.run.resummino.run.get_path
   hepi.run.resummino.run.get_version


.. py:class:: ResumminoRunner(path, in_dir = None, out_dir = None, pre=None)

   Bases: :py:obj:`hepi.run.Runner`

   .. py:method:: orders()

      List of supported Orders in this runner.


   .. py:method:: get_version()


   .. py:method:: _check_path()

      Checks if the passed path is valid.


   .. py:method:: _check_input(p, **kwargs)


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


   .. py:method:: _parse_file(file)

      Extracts results from an output file.

      :param file: File path to be parsed.
      :type file: str

      :returns: If a value is not found in the file None is used.
      :rtype: :class:`Result`


   .. py:method:: _prepare(p, **kwargs)



.. py:data:: default_resummino_runner

   Default Resummino Runner to provide backward compatibility

.. py:data:: run

   

.. py:data:: set_path

   

.. py:data:: get_path

   

.. py:data:: get_version

   
