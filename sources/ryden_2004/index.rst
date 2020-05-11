.. index:: Ryden (2004)

The Ellipticity of the Disks of Spiral Galaxies
===============================================

:Author: Ryden, Barbara S.

:Abstract: The disks of spiral galaxies are generally elliptical rather than
    circular. The distribution of ellipticities can be fitted with a lognormal
    distribution. For a sample of 12,764 galaxies from the Sloan Digital Sky
    Survey Data Release 1 (SDSS DR1), the distribution of apparent axis ratios
    in the i band is best fit by a lognormal distribution of intrinsic
    ellipticities with :math:`{\rm ln} \epsilon = -1.85 \pm 0.89`. For a sample
    of nearly face-on spiral galaxies analyzed by Andersen & Bershady using both
    photometric and spectroscopic data, the best-fitting distribution of
    ellipticities has :math:`{\rm ln} \epsilon = -2.29 \pm 1.04`. Given the
    small size of the Andersen & Bershady sample, the two distributions are not
    necessarily inconsistent with each other. If the ellipticity of the
    potential were equal to that of the light distribution of the SDSS DR1
    galaxies, it would produce 1.0 mag of scatter in the Tully-Fisher relation,
    greater than is observed. The Andersen & Bershady results, however, are
    consistent with a scatter as small as 0.25 mag in the Tully-Fisher relation.

:Publication: The Astrophysical Journal, Volume 601, Issue 1, pp. 214-220.
:Pubdate: January 2004
:DOI: 10.1086/380437
:arXiv: astro-ph/0310097
:Bibcode: 2004ApJ...601..214R
:Keywords: Galaxies: Fundamental Parameters; Galaxies: Photometry; Galaxies:
    Spiral; Astrophysics

Figures
-------

.. _ryden_2004_fig_1:
.. figure:: ryden_2004_fig_1.*
   :width: 60%

   Ryden (2004), Fig. 1

   *Histogram*: Distribution of axis ratio :math:`q_{\rm am}`, using
   adaptive moments in the *i* band, for exponential galaxies in the SDSS DR1.
   *Points with error bars*: Best-fitting model, assuming a Gaussian
   distribution of disk thickness and a lognormal distribution of intrinsic
   disk ellipticity. The best-fitting model has thickness :math:`\gamma = 0.222
   \pm 0.057` and ellipticity :math:`\log\epsilon = -1.85 \pm 0.89`.

   Source: :source:`sources/ryden_2004/fig_1.py`

:ref:`ryden_2004_fig_1` reproduced by :func:`skypy.galaxy.ellipticity.ryden04`.
The selection follows everything specified in Section 2 but returns 12,953
galaxies in the *i*-band instead of the quoted 12,764 galaxies in the paper.
