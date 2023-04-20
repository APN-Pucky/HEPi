:py:mod:`hepi.run.spheno.run`
=============================

.. py:module:: hepi.run.spheno.run


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.spheno.run.SPhenoRunner




Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.spheno.run.spheno_default_runner
   hepi.run.spheno.run.run
   hepi.run.spheno.run.set_path
   hepi.run.spheno.run.get_path


.. py:class:: SPhenoRunner(path, in_dir = None, out_dir = None, pre=None)

   Bases: :py:obj:`hepi.run.Runner`

   .. py:method:: _check_path()

      Checks if the passed path is valid.


   .. py:method:: run(slhas, **kwargs)

      Run the passed list of parameters for SPheno.

      :param slhas: Input parameters with a SLHA file that can be processed by SPheno.
      :type slhas: :obj:`list` of :class:`Input`

      :returns: :obj:`list` of :class:`Input`



.. py:data:: spheno_default_runner

   Default SPheno Runner to provide backward compatibility

.. py:data:: run

   

.. py:data:: set_path

   

.. py:data:: get_path

   
