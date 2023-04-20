:py:mod:`hepi.particles`
========================

.. py:module:: hepi.particles


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hepi.particles.get_name
   hepi.particles.get_LR_partner



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


.. py:function:: get_LR_partner(pid)

   Transforms a PDG id to it's left-right partner.

   :param pid: PDG Monte Carlo identifier for the particle.
   :type pid: int

   :returns: First int is -1 for Left and 1 for Right. Second int is the PDG id.
   :rtype: tuple

   .. rubric:: Examples

   >>> get_LR_partner(1000002)
   (-1, 2000002)
