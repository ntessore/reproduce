import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
import io

from astroquery.sdss import SDSS


# SDSS sample
# ===========

query = '''
SELECT TOP 50000
    p.objID as id,
    p.petroR50_r AS R50_r,
    p.petroMag_r-p.extinction_r AS r,
    s.z AS z
FROM
    PhotoObj AS p
    JOIN SpecObj AS s ON s.bestobjid = p.objid
WHERE
    p.objID > {}
    AND s.mjd < 52365
    AND (s.primTarget & 0x00000040)+(s.primTarget & 0x00000080) > 0
    AND s.zWarning = 0
    AND (p.flags_r & 0x0000000000000100) = 0
ORDER BY
    p.objID ASC
'''

last_id = -1
result = None
while True:
    response = SDSS.query_sql_async(query.format(last_id), data_release=2,
                                    timeout=300, cache=True)
    batch = np.genfromtxt(io.StringIO(response.text), delimiter=',', names=True)
    if batch.size == 0:
        break
    if result is None:
        result = batch
    else:
        result = np.concatenate([result, batch])
    last_id = batch['id'][-1]

Ngal = len(result)

print('selected %d galaxies' % Ngal)

R50_r, r, z = result['R50_r'], result['r'], result['z']
mu50_r = r + 2.5*np.log10(2*np.pi*R50_r**2)


# figures
# =======

# Fig. 1
fig, ax = plt.subplots(2, 2, figsize=(4.0, 4.0), dpi=600)

ax[0, 0].hist(R50_r, range=[0, 12], bins=30, histtype='step', ec='k', lw=0.5,
              density=True)
ax[0, 0].set_xlim(0, 12)
ax[0, 0].set_ylim(0, 0.65)
ax[0, 0].set_xlabel(r'$R_{50,r}$ [arcsec]', size='small')
ax[0, 0].set_ylabel(r'Frac', size='small')
ax[0, 0].tick_params(axis='both', which='both', direction='in', width=0.5,
                     top=True, right=True)
ax[0, 0].tick_params(axis='both', pad=5, labelsize='small')
ax[0, 0].tick_params(axis='both', which='major', length=6)
ax[0, 0].tick_params(axis='both', which='minor', length=3)
ax[0, 0].xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[0, 0].xaxis.set_major_locator(MultipleLocator(5))
ax[0, 0].xaxis.set_minor_locator(MultipleLocator(1))
ax[0, 0].yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[0, 0].yaxis.set_major_locator(MultipleLocator(0.2))
ax[0, 0].yaxis.set_minor_locator(MultipleLocator(0.1))

ax[0, 1].hist(r, range=[14, 19], bins=50, histtype='step', ec='k', lw=0.5,
              density=True)
ax[0, 1].set_xlim(14, 19)
ax[0, 1].set_ylim(0, 1.4)
ax[0, 1].set_xlabel(r'$r$ [mag]', size='small')
ax[0, 1].set_ylabel(r'Frac', size='small')
ax[0, 1].tick_params(axis='both', which='both', direction='in', width=0.5,
                     top=True, right=True)
ax[0, 1].tick_params(axis='both', pad=5, labelsize='small')
ax[0, 1].tick_params(axis='both', which='major', length=6)
ax[0, 1].tick_params(axis='both', which='minor', length=3)
ax[0, 1].xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[0, 1].xaxis.set_major_locator(MultipleLocator(2))
ax[0, 1].xaxis.set_minor_locator(MultipleLocator(0.5))
ax[0, 1].yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[0, 1].yaxis.set_major_locator(MultipleLocator(0.4))
ax[0, 1].yaxis.set_minor_locator(MultipleLocator(0.2))

ax[1, 0].hist(mu50_r, range=[18, 24], bins=50, histtype='step', ec='k', lw=0.5,
              density=True)
ax[1, 0].set_xlim(18, 24)
ax[1, 0].set_ylim(0, 0.65)
ax[1, 0].set_xlabel(r'$\mu_{50,r}$ [magarcsec$^{-2}$]', size='small')
ax[1, 0].set_ylabel(r'Frac', size='small')
ax[1, 0].tick_params(axis='both', which='both', direction='in', width=0.5,
                     top=True, right=True)
ax[1, 0].tick_params(axis='both', pad=5, labelsize='small')
ax[1, 0].tick_params(axis='both', which='major', length=6)
ax[1, 0].tick_params(axis='both', which='minor', length=3)
ax[1, 0].xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[1, 0].xaxis.set_major_locator(MultipleLocator(2))
ax[1, 0].xaxis.set_minor_locator(MultipleLocator(0.5))
ax[1, 0].yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[1, 0].yaxis.set_major_locator(MultipleLocator(0.2))
ax[1, 0].yaxis.set_minor_locator(MultipleLocator(0.1))

ax[1, 1].hist(z, range=[0, 0.35], bins=35, histtype='step', ec='k', lw=0.5,
              density=True)
ax[1, 1].set_xlim(0, 0.35)
ax[1, 1].set_ylim(0, 10)
ax[1, 1].set_xlabel(r'$z$', size='small')
ax[1, 1].set_ylabel(r'Frac', size='small')
ax[1, 1].tick_params(axis='both', which='both', direction='in', width=0.5,
                     top=True, right=True)
ax[1, 1].tick_params(axis='both', pad=5, labelsize='small')
ax[1, 1].tick_params(axis='both', which='major', length=6)
ax[1, 1].tick_params(axis='both', which='minor', length=3)
ax[1, 1].xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[1, 1].xaxis.set_major_locator(MultipleLocator(0.1))
ax[1, 1].xaxis.set_minor_locator(MultipleLocator(0.05))
ax[1, 1].yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax[1, 1].yaxis.set_major_locator(MultipleLocator(4))
ax[1, 1].yaxis.set_minor_locator(MultipleLocator(2))

fig.subplots_adjust(wspace=0.55, hspace=0.55)

fig.savefig('fig_1.pdf', bbox_inches='tight')
fig.savefig('fig_1.svg', bbox_inches='tight')
