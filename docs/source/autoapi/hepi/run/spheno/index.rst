:py:mod:`hepi.run.spheno`
=========================

.. py:module:: hepi.run.spheno

.. autoapi-nested-parse::

   :mod:`hepi` interface to spheno.

   SPheno stands for S(upersymmetric) Pheno(menology) find it here https://spheno.hepforge.org/.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   run/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   hepi.run.spheno.Input
   hepi.run.spheno.Runner
   hepi.run.spheno.SPhenoRunner



Functions
~~~~~~~~~

.. autoapisummary::

   hepi.run.spheno.update_slha



Attributes
~~~~~~~~~~

.. autoapisummary::

   hepi.run.spheno.spheno_default_runner
   hepi.run.spheno.run
   hepi.run.spheno.set_path
   hepi.run.spheno.get_path


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



.. py:function:: update_slha(i)

   Updates dependent parameters in Input `i`.

   Mainly concerns the `mu` value used by `madgraph`.


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

   
