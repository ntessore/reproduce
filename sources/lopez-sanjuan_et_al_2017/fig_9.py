import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.cosmology import FlatLambdaCDM
from astropy.table import Table
from astropy.utils.data import download_file

from skypy.pipeline import Pipeline

# survey parameters
cosmology = FlatLambdaCDM(Om0=0.3, H0=70)
survey_area = u.Quantity('2.38 deg2')

# download catalogue
alhambra = download_file(
    'http://svo2.cab.inta-csic.es/vocats/alhambra/download/alhambra.csv.gz',
    cache=True)

# simulate with SkyPy
sim = Pipeline.read('fig_9.yml')
sim.execute()

# the model
def schechter_SF(M, z):
    M_star = -21.00 - 1.03*(z - 0.5)
    phi_star = 10.**(-2.51 - 0.01*(z - 0.5))
    alpha = -1.29
    M = np.reshape(M, (-1, 1))
    return 0.4*np.log(10)*phi_star*10.**(-0.4*(M - M_star)*(alpha+1))*np.exp(-10.**(-0.4*(M - M_star)))

# four redshift bins
zbins = [(0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]

# magnitude bins for histograms in each redshift bin
data_bins_bin = [
    -np.arange(15.6, 23.001, 0.3)[::-1],
    -np.arange(17.3, 23.401, 0.3)[::-1],
    -np.arange(18.2, 23.301, 0.3)[::-1],
    -np.arange(18.8, 23.401, 0.3)[::-1],
]

# magnitude bins for simulation
sim_bins = -np.arange(14, 24.501, 0.3)[::-1]

# read the catalogue
data = Table.read(alhambra, format='ascii.csv')

# the probability that a galaxy is SF in the T = (5, 6) transition zone
SF_prob_T = [5.00, 5.06, 5.17, 5.28, 5.39, 5.5 , 5.61, 5.72, 5.83, 5.94, 6.00]
SF_prob_P = [0.56, 0.56, 0.55, 0.56, 0.66, 0.72, 0.74, 0.82, 0.91, 0.94, 0.94]

# assign probabilities for being SF to catalogue
P_SF = np.interp(data['tb_1'], SF_prob_T, SF_prob_P, left=0, right=1)

# Bernoulli draw whether objects are SF
SF_flag = np.random.binomial(1, P_SF)

# select SF galaxies from catalogue
data_good = (data['Stellar_Flag'] <= 0.5) & (data['Satur_Flag'] == 0) & (SF_flag == 1)

print('selected {}/{} galaxies from catalogue'.format(np.sum(data_good), len(data)))

# set up plot
plt.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage[T1]{fontenc}',
    'font.family': 'serif',
    'legend.frameon': False,
    'legend.handlelength': 1.5,
})
fig = plt.figure(figsize=(6.0, 4.0), dpi=600)

# plot histograms and model for each bin
for i, ((za, zb), data_bins) in enumerate(zip(zbins, data_bins_bin)):
    # compute comoving volume for redshift slice
    dz = np.linspace(za, zb, 1000)
    dV_dz = cosmology.differential_comoving_volume(dz)*survey_area
    dV = np.trapz(dV_dz.to_value('Mpc3'), dz)

    # compute model average over redshift bin
    M_model = np.arange(-24.5, -14, 0.1)
    phi_model_z = schechter_SF(M_model, dz)
    phi_model = np.log10(np.median(phi_model_z, axis=-1))

    # get data distribution
    M_data = data['M_ABS_1'][data_good & (za <= data['zb_1']) & (data['zb_1'] < zb)]
    n_data, b_data = np.histogram(M_data, bins=data_bins)
    phi_data = np.log10(n_data/dV/np.diff(b_data) + 1e-100)

    # get simulated distribution
    M_sim = sim['SF']['M'][(za <= sim['SF']['z']) & (sim['SF']['z'] < zb)]
    n_sim, b_sim = np.histogram(M_sim, bins=sim_bins)
    phi_sim = np.log10(n_sim/dV/np.diff(b_sim) + 1e-100)

    # plot model curve and histograms
    plt.subplot(2, 2, i+1)
    plt.step(b_sim, np.concatenate([phi_sim, [-np.inf]]), 'r', where='post', lw=1.0, zorder=2, label='SkyPy')
    plt.plot((b_data[1:]+b_data[:-1])/2, phi_data, 's', ms=3, mec='black', mew=0.8, mfc='turquoise', zorder=1, label='This work')
    plt.plot(M_model, phi_model, '-', lw=2, c='royalblue', alpha=0.9, zorder=0, label='Model')

    # style plot
    plt.xlim(-14, -24.5)
    plt.ylim(-6.5, -1.5)
    plt.xticks([-14, -16, -18, -20, -22, -24])
    plt.yticks([-2, -3, -4, -5, -6])
    plt.tick_params(axis='both', direction='in', width=0.5, left=True, right=True, top=True, bottom=True)
    plt.xlabel(r'$M_B$')
    plt.ylabel(r'$\log_{10} \Phi \, [\mathrm{Mpc}^{-3} \, \mathrm{mag}^{-1}]$')
    plt.title(r'${:.2f} \le z < {:.2f}$'.format(za, zb), position=(0.22, 0.02), size=8)
    if i == 0:
        plt.legend(loc=(0.05, 0.17), fontsize=5)

# produce plots
plt.tight_layout()
plt.savefig('lopez-sanjuan_et_al_2017_fig_9.pdf', bbox_inches='tight')
plt.savefig('lopez-sanjuan_et_al_2017_fig_9.svg', bbox_inches='tight')
plt.close()
