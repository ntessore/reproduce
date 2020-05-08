import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import io

from astroquery.sdss import SDSS
from skypy.galaxy.ellipticity import ryden04


# SDSS sample
# ===========

# selection as described in Section 2
query = '''
SELECT
    p.mE1_i AS e1,
    p.mE2_i AS e2
FROM
    PhotoObj AS p
    JOIN SpecObj AS s ON s.bestobjid = p.objid
WHERE
    s.specClass = 2
    AND p.lnLExp_r > p.lnLDev_r + log(2)
    AND p.lnLExp_r > p.lnLStar_r + log(2)
    AND p.expRad_i > 5*sqrt(mRrCcPSF_i)*0.396
    AND (p.flags_i & 0x0020000000000000) = 0
    AND (p.flags_i & 0x0040000000000000) = 0
    AND (p.flags_i & 0x0080000000000000) = 0
    AND s.z < 0.1
    AND s.z > 0.002
    AND s.zWarning = 0
'''

response = SDSS.query_sql_async(query, data_release=1, timeout=300, cache=True)
result = np.genfromtxt(io.StringIO(response.text), delimiter=',', names=True)

Ngal = len(result)

print('selected %d galaxies' % Ngal)

e = np.hypot(result['e1'], result['e2'])

print('ellipticity range %.2f to %.2f' % (np.min(e), np.max(e)))

q_am = np.sqrt((1 - e)/(1 + e))  # (9)



# model
# =====

# binning scheme of Fig. 1
bins = np.linspace(0, 1, 41)

# bin centres
mid = (bins[:-1]+bins[1:])/2

# mean and variance of sampling
mean = np.zeros(len(bins)-1)
var = np.zeros(len(bins)-1)

# best-fit parameters of Fig. 1
mu_gamma, sigma_gamma, mu, sigma = 0.222, 0.057, -1.85, 0.89

# create 16,000 realisations
print('simulate')
for i in range(16000):
    # sample
    e = ryden04(mu_gamma, sigma_gamma, mu, sigma, size=Ngal)

    # recover q from e
    q = (1 - e)/(1 + e)

    # bin
    n, _ = np.histogram(q, bins=bins)

    # update mean and variance
    x = n - mean
    mean += x/(i+1)
    y = n - mean
    var += x*y

# finalise variance
var = var/i

# standard deviation
std = np.sqrt(var)


# figures
# =======

# create the formatter
formatter = lambda x, pos: '{:g}'.format(x).lstrip('0') or '0'

# Fig. 1
plt.figure(figsize=(4.0, 2.8), dpi=600)
plt.hist(q_am, range=[0, 1], bins=40, histtype='step', ec='k', lw=0.5)
plt.errorbar(mid, mean, yerr=std, fmt='.k', ms=4, capsize=3, lw=0.5, mew=0.5)
plt.xlim(0, 1)
plt.ylim(0, 650)
plt.xlabel(r'${\rm q}_{\rm am}$')
plt.ylabel(r'N')
plt.yticks([0, 200, 400, 600])
plt.tick_params(axis='both', which='both', direction='in', width=0.5)
plt.tick_params(axis='both', pad=4, labelsize='small')
plt.tick_params(axis='both', which='major', length=8)
plt.tick_params(axis='both', which='minor', length=4)
plt.minorticks_on()
plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))
plt.savefig('fig_1.pdf', bbox_inches='tight')
plt.savefig('fig_1.svg', bbox_inches='tight')
