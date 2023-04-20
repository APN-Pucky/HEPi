:py:mod:`hepi.run.madgraph.run`
===============================

.. py:module:: hepi.run.madgraph.run

.. autoapi-nested-parse::

   Runs MadGraph.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.madgraph.run.MadGraphRunParams
   hepi.run.madgraph.run.MadGraphRunner




Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.madgraph.run.default_madgraph_runner
   hepi.run.madgraph.run.run
   hepi.run.madgraph.run.set_path
   hepi.run.madgraph.run.get_path


.. py:class:: MadGraphRunParams(dic, skip=False, madstr=True)

   Bases: :py:obj:`hepi.run.RunParam`

   Parameters for MadGraph.


.. py:class:: MadGraphRunner(path, in_dir = None, out_dir = None, pre=None)

   Bases: :py:obj:`hepi.run.Runner`

   .. py:method:: orders()

      List of supported Orders in this runner.


   .. py:method:: _check_path()

      Checks if the passed path is valid.


   .. py:method:: _check_input(param, **kwargs)

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


   .. py:method:: _run(rps, wait=True, parallel=True, sleep=0, **kwargs)

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


   .. py:method:: _prepare(p, **kwargs)



.. py:data:: default_madgraph_runner

   Default MadGraph Runner to provide backward compatibility

.. py:data:: run

   

.. py:data:: set_path

   

.. py:data:: get_path

   
