"""Functions to generate the reference files.
"""
import copy
import os

import matplotlib.pyplot as plt
import numpy as np

from .context import petitRADTRANS
from .utils import radtrans_parameters, reference_filenames, temperature_guillot_2010, temperature_isothermal, version


# Save functions
def __save_contribution_function(filename, atmosphere, mode='emission', plot_figure=False, figure_title=None,
                                 prt_version=version):
    wavelength = np.asarray(petitRADTRANS.nat_cst.c / atmosphere.freq * 1e4)

    if mode == 'emission':
        contribution = np.asarray(atmosphere.contr_em)
    elif mode == 'transmission':
        contribution = np.asarray(atmosphere.contr_tr)
    else:
        raise ValueError(f"unknown contribution mode '{mode}', available modes are 'emission' or 'transmission'")

    np.savez_compressed(
        os.path.join(filename),
        wavelength=wavelength,
        contribution=contribution,
        header=f'File generated by tests.utils function\n'
               f'wavelength units: um\n'
               f'spectral radiosity units: erg.cm-2.s-1.Hz-1',
        prt_version=f'{prt_version}'
    )

    if plot_figure:
        plt.figure()
        x, y = np.meshgrid(wavelength, atmosphere.press * 1e-6)
        plt.contourf(x, y, contribution, 30, cmap='bone_r')

        plt.yscale('log')
        plt.xscale('log')
        plt.ylim([1e2, 1e-6])
        plt.xlim([np.min(wavelength), np.max(wavelength)])

        plt.xlabel(r'Wavelength ($\mu$m)')
        plt.ylabel(r'Pressure (bar)')
        plt.title(figure_title)


def __save_emission_spectrum(filename, atmosphere, plot_figure=False, figure_title=None, prt_version=version):
    wavelength = np.asarray(petitRADTRANS.nat_cst.c / atmosphere.freq * 1e4)

    np.savez_compressed(
        os.path.join(filename),
        wavelength=wavelength,
        spectral_radiosity=np.asarray(atmosphere.flux),
        header=f'File generated by tests.utils function\n'
               f'wavelength units: um\n'
               f'spectral radiosity units: erg.cm-2.s-1.Hz-1',
        prt_version=f'{prt_version}'
    )

    if plot_figure:
        plt.figure()
        plt.semilogx(wavelength, atmosphere.flux)
        plt.xlabel(r'Wavelength ($\mu$m)')
        plt.ylabel(r'Spectral radiosity (erg$\cdot$s$^{-1}\cdot$cm$^{-2}\cdot$Hz$^{-1}$)')
        plt.title(figure_title)


def __save_mass_fractions(filename, mass_fractions, plot_figure=False, y_axis=None, y_label='', y_lim=None,
                          figure_title=None, prt_version=version):
    np.savez_compressed(
        file=os.path.join(filename),
        header=f'File generated by tests.utils function\n'
               f'wavelength units: um\n'
               f'spectral radiosity units: erg.cm-2.s-1.Hz-1',
        prt_version=f'{prt_version}',
        **mass_fractions  # pass mass fractions as keyword arguments to avoid the need of pickle
    )

    if plot_figure:
        if y_axis is None:
            axis_length = np.size(mass_fractions(list(mass_fractions.keys())[0]))
            y_axis = np.linspace(0, axis_length, axis_length)

        # Mass fractions figure
        plt.figure()

        for species in mass_fractions.keys():
            if species not in ['MMW', 'nabla_ad']:
                plt.loglog(mass_fractions[species], y_axis, label=species)

        plt.ylim(y_lim)
        plt.xlim([1e-10, 1])
        plt.xlabel(r'Mass fraction')
        plt.ylabel(y_label)
        plt.title('Mass fractions' + figure_title)

        # Nabla figure
        plt.figure()
        plt.loglog(mass_fractions['nabla_ad'], y_axis)

        plt.ylim(y_lim)
        plt.xlabel(r'Moist adiabatic temperature gradient $\nabla_{\rm ad}$')
        plt.ylabel(y_label)
        plt.title(r'$\nabla_{\rm ad}$' + figure_title)

        # Mean molar mass figure
        plt.figure()
        plt.loglog(mass_fractions['MMW'], y_axis)

        plt.ylim(y_lim)
        plt.xlabel(r'Mean molar mass')
        plt.ylabel(y_label)
        plt.title('Mean molar mass' + figure_title)


def __save_temperature_profile(filename, temperature, plot_figure=False, figure_title=None, prt_version=version):
    np.savez_compressed(
        os.path.join(filename),
        temperature=np.asarray(temperature),
        pressure=np.asarray(radtrans_parameters['pressures']),
        header=f'File generated by tests.utils function\n'
               f'temperature units: K\n'
               f'pressure units: bar',
        prt_version=f'{prt_version}'
    )

    if plot_figure:
        plt.figure()
        plt.semilogy(temperature, radtrans_parameters['pressures'])
        plt.ylim([1e2, 1e-6])
        plt.xlabel('Temperature (K)')
        plt.ylabel('Pressure (bar)')
        plt.title(figure_title)


def __save_transmission_spectrum(filename, atmosphere, plot_figure=False, figure_title=None, prt_version=version):
    wavelength = np.asarray(petitRADTRANS.nat_cst.c / atmosphere.freq * 1e4)
    transit_radius = np.asarray(atmosphere.transm_rad / petitRADTRANS.nat_cst.r_jup_mean)

    np.savez_compressed(
        os.path.join(filename),
        wavelength=wavelength,
        transit_radius=transit_radius,
        header=f'File generated by tests.utils function\n'
               f'wavelength units: um\n'
               f'transit_radius units: R_jup',
        prt_version=f'{prt_version}'
    )

    if plot_figure:
        plt.figure()
        plt.semilogx(wavelength, transit_radius)
        plt.xlabel(r'Wavelength ($\mu$m)')
        plt.ylabel(r'Transit radius (R$_{\rm{Jup}}$)')
        plt.title(figure_title)


def npz2dat(file, new_resolution_power=60.0, relative_error=0.05, mode='transmission'):
    """Converts a .npz spectrum file into a .dat file suitable for the petitRADTRANS.retrieval Data class.

    The .dat file is outputted in the same directory than the .npz file.

    Args:
        file:
            The .npz file to convert.
        new_resolution_power:
            The resolution power of the .dat file. It should be lower than the one in the original file.
        relative_error:
            Mock observation uncertainty to add.
        mode:
            How to read the .npz file ('emission'|'transmission')
    """
    # from petitRADTRANS.ccf.mock_observation import convolve_rebin
    from petitRADTRANS.nat_cst import convolve_rebin, radiosity_erg_hz2radiosity_erg_cm

    npz_data = np.load(file)

    wavelength = npz_data['wavelength']

    if mode == 'emission':
        # flux = petitRADTRANS.ccf.spectra_utils.radiosity_erg_hz2radiosity_erg_cm(
        #     npz_data['spectral_radiosity'],
        #     petitRADTRANS.nat_cst.c * 1e4 / wavelength  # um to Hz
        # )  # future
        flux = radiosity_erg_hz2radiosity_erg_cm(
            npz_data['spectral_radiosity'],
            petitRADTRANS.nat_cst.c * 1e4 / wavelength  # um to Hz
        )
        flux *= 1e-7  # erg.s-1.cm-2/cm to W.m-2/um

        flux_str = 'spectral_radiosity units: W.m-2/um\n'
    elif mode == 'transmission':
        flux = (
            npz_data['transit_radius'] * petitRADTRANS.nat_cst.r_jup_mean
            / (radtrans_parameters['stellar_parameters']['radius'] * petitRADTRANS.nat_cst.r_sun)
        ) ** 2
        flux_str = 'transit_radius units: (R_p/R_star)^2\n'
    else:
        raise ValueError(f"mode must be 'emission' or 'transmission', but was '{mode}'")

    dump, wavelength, flux = convolve_rebin(
        input_wavelengths=wavelength,
        input_flux=flux,
        instrument_resolving_power=new_resolution_power,
        pixel_sampling=1,
        instrument_wavelength_range=(wavelength[1], wavelength[-1])
    )

    error = relative_error * np.max(flux)

    flux += np.random.default_rng().normal(
        loc=0.,
        scale=error,
        size=np.size(flux)
    )

    error *= np.ones_like(wavelength)

    np.savetxt(
        fname=file.rsplit('.', 1)[0] + '.dat',
        X=np.transpose((wavelength, flux, error)),
        header='wavelength flux error\n'
               f'File generated by tests.utils function\n'
               f'wavelength units: um\n'
               f'error and {flux_str}'
               f'resolution power {new_resolution_power}\n'
               f'relative error {relative_error}\n'
               f'original file: {file}'
    )


# Data files generation functions
def create_guillot_2010_temperature_profile_ref(plot_figure=False):
    # temperature_guillot = petitRADTRANS.physics.guillot_global(
    #     pressure=radtrans_parameters['pressures'],
    #     kappa_ir=radtrans_parameters['temperature_guillot_2010_parameters']['infrared_mean_opacity'],
    #     gamma=radtrans_parameters['temperature_guillot_2010_parameters']['gamma'],
    #     grav=radtrans_parameters['planetary_parameters']['surface_gravity'],
    #     t_int=radtrans_parameters['temperature_guillot_2010_parameters']['intrinsic_temperature'],
    #     t_equ=radtrans_parameters['temperature_guillot_2010_parameters']['equilibrium_temperature']
    # )  # future
    temperature_guillot = petitRADTRANS.physics.guillot_global(P=radtrans_parameters['pressures'],
        kappa_IR=radtrans_parameters['temperature_guillot_2010_parameters']['infrared_mean_opacity'],
        gamma=radtrans_parameters['temperature_guillot_2010_parameters']['gamma'],
        grav=radtrans_parameters['planetary_parameters']['surface_gravity'],
        T_int=radtrans_parameters['temperature_guillot_2010_parameters']['intrinsic_temperature'],
        T_equ=radtrans_parameters['temperature_guillot_2010_parameters']['equilibrium_temperature']
    )

    __save_temperature_profile(
        reference_filenames['guillot_2010'], temperature_guillot, plot_figure, 'Guillot 2010 temperature profile'
    )


def create_mock_observation_transmission_spectrum(plot_figure=False):
    npz2dat(
        file=reference_filenames['correlated_k_transmission_cloud_calculated_radius_scattering'],
        new_resolution_power=radtrans_parameters['mock_observation_parameters']['resolution_power'],
        relative_error=radtrans_parameters['mock_observation_parameters']['relative_error'],
        mode='transmission'
    )

    if plot_figure:
        data = np.loadtxt(reference_filenames['mock_observation_transmission'])
        wavelength = data[:, 0]
        transit_radius = data[:, 1]
        error = data[:, 2]

        plt.figure()
        plt.errorbar(wavelength, transit_radius, yerr=error, ls='', marker='+', capsize=2)
        plt.xlabel(r'Wavelength ($\mu$m)')
        plt.ylabel(r'Transit radius (R$_{\rm{Jup}}$)')
        plt.title('Mock observed spectrum')


def create_radtrans_correlated_k_emission_spectrum_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    atmosphere_ck.calc_flux(
        temp=temperature_guillot_2010,
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
    )

    __save_emission_spectrum(
        reference_filenames['correlated_k_emission'], atmosphere_ck, plot_figure, 'Correlated-k emission spectrum'
    )


def create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck.calc_flux(
        temp=temperature_guillot_2010,
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
        fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
        sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal'],
        contribution=True
    )

    __save_emission_spectrum(
        reference_filenames['correlated_k_emission_cloud_calculated_radius'], atmosphere_ck, plot_figure,
        'Correlated-k emission spectrum, with non-gray cloud using Hansen radius',
        prt_version=version
    )

    __save_contribution_function(
        reference_filenames['correlated_k_emission_contribution_cloud_calculated_radius'],
        atmosphere_ck,
        mode='emission',
        plot_figure=plot_figure,
        figure_title='Correlated-k emission contribution function, '
                     'with non-gray cloud using calculated radius',
        prt_version=version
    )


def create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_stellar_scattering_ref(plot_figure=False):
    from .test_radtrans_correlated_k_scattering import atmosphere_ck_scattering

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    geometries = [
        'planetary_ave',
        'dayside_ave',
        'non-isotropic'
    ]

    for geometry in geometries:
        atmosphere_ck_scattering.calc_flux(
            temp=temperature_guillot_2010,
            abunds=mass_fractions,
            gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
            mmw=radtrans_parameters['mean_molar_mass'],
            Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
            fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
            sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal'],
            geometry=geometry,
            Tstar=radtrans_parameters['stellar_parameters']['effective_temperature'],
            Rstar=radtrans_parameters['stellar_parameters']['radius'] * petitRADTRANS.nat_cst.r_sun,
            semimajoraxis=radtrans_parameters['planetary_parameters']['orbit_semi_major_axis'],
            theta_star=radtrans_parameters['stellar_parameters']['incidence_angle']
        )

        __save_emission_spectrum(
            reference_filenames[f'correlated_k_emission_cloud_calculated_radius_scattering_{geometry}'],
            atmosphere_ck_scattering, plot_figure,
            f'Correlated-k transmission spectrum, '
            f'with non-gray cloud using calculated radius and scattering ({geometry})',
            prt_version=version
        )


def create_radtrans_correlated_k_emission_spectrum_cloud_hansen_radius_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck.calc_flux(
        temp=temperature_guillot_2010,
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
        fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
        b_hans=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['b_hansen'],
        dist='hansen'
    )

    __save_emission_spectrum(
        reference_filenames['correlated_k_emission_cloud_hansen_radius'], atmosphere_ck, plot_figure,
        'Correlated-k emission spectrum, with non-gray cloud using Hansen radius',
        prt_version=petitRADTRANS.version.version
    )


def create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_scattering_ref(plot_figure=False):
    from .test_radtrans_correlated_k_scattering import atmosphere_ck_scattering

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck_scattering.calc_flux(
        temp=temperature_guillot_2010,
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
        fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
        sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal'],
        add_cloud_scat_as_abs=True
    )

    __save_emission_spectrum(
        reference_filenames['correlated_k_emission_cloud_calculated_radius_scattering'],
        atmosphere_ck_scattering,
        plot_figure,
        'Correlated-k emission spectrum, with non-gray cloud using calculated radius and scattering',
        prt_version=version
    )


def create_radtrans_correlated_k_emission_spectrum_surface_scattering_ref(plot_figure=False):
    from .test_radtrans_correlated_k_surface_scattering import atmosphere_ck_surface_scattering

    # Copy atmosphere so that change in reflectance is not carried outside the function
    atmosphere = copy.deepcopy(atmosphere_ck_surface_scattering)

    atmosphere.reflectance = radtrans_parameters['planetary_parameters']['surface_reflectance'] * \
        np.ones_like(atmosphere.freq)

    atmosphere.calc_flux(
        temp=temperature_guillot_2010,
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        geometry='non-isotropic',
        Tstar=radtrans_parameters['stellar_parameters']['effective_temperature'],
        Rstar=radtrans_parameters['stellar_parameters']['radius'] * petitRADTRANS.nat_cst.r_sun,
        semimajoraxis=radtrans_parameters['planetary_parameters']['orbit_semi_major_axis'],
        theta_star=radtrans_parameters['stellar_parameters']['incidence_angle']
    )

    __save_emission_spectrum(
        reference_filenames['correlated_k_emission_surface_scattering'],
        atmosphere, plot_figure, 'Correlated-k emission spectrum with surface scattering'
    )


def create_radtrans_correlated_k_transmission_spectrum_cloud_calculated_radius_scattering_ref(plot_figure=False):
    from .test_radtrans_correlated_k_scattering import atmosphere_ck_scattering

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck_scattering.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
        fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
        sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_cloud_calculated_radius_scattering'],
        atmosphere_ck_scattering,
        plot_figure,
        'Correlated-k transmission spectrum, with non-gray cloud using calculated radius and scattering',
        prt_version=version
    )


def create_radtrans_correlated_k_transmission_spectrum_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission'], atmosphere_ck, plot_figure,
        'Correlated-k transmission spectrum'
    )


def create_radtrans_correlated_k_transmission_spectrum_cloud_power_law_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        kappa_zero=radtrans_parameters['cloud_parameters']['kappa_zero'],
        gamma_scat=radtrans_parameters['cloud_parameters']['gamma_scattering']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_cloud_power_law'],
        atmosphere_ck, plot_figure, 'Correlated-k transmission spectrum, with power law cloud'
    )


def create_radtrans_correlated_k_transmission_spectrum_gray_cloud_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        Pcloud=radtrans_parameters['cloud_parameters']['cloud_pressure']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_gray_cloud'],
        atmosphere_ck, plot_figure, 'Correlated-k transmission spectrum, with gray cloud'
    )


def create_radtrans_correlated_k_transmission_spectrum_rayleigh_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        haze_factor=radtrans_parameters['cloud_parameters']['haze_factor']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_rayleigh'],
        atmosphere_ck, plot_figure, 'Correlated-k transmission spectrum, with hazes'
    )


def create_radtrans_correlated_k_transmission_spectrum_cloud_fixed_radius_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        radius={'Mg2SiO4(c)': radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['radius']},
        sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal']
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_cloud_fixed_radius'], atmosphere_ck, plot_figure,
        'Correlated-k transmission spectrum, with non-gray cloud using fixed radius'
    )


def create_radtrans_correlated_k_transmission_spectrum_cloud_calculated_radius_ref(plot_figure=False):
    from .test_radtrans_correlated_k import atmosphere_ck

    mass_fractions = copy.deepcopy(radtrans_parameters['mass_fractions'])
    mass_fractions['Mg2SiO4(c)'] = \
        radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['mass_fraction']

    atmosphere_ck.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=mass_fractions,
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure'],
        Kzz=radtrans_parameters['planetary_parameters']['eddy_diffusion_coefficient'],
        fsed=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['f_sed'],
        sigma_lnorm=radtrans_parameters['cloud_parameters']['cloud_species']['Mg2SiO4(c)_cd']['sigma_log_normal'],
        contribution=True
    )

    __save_transmission_spectrum(
        reference_filenames['correlated_k_transmission_cloud_calculated_radius'], atmosphere_ck, plot_figure,
        'Correlated-k transmission spectrum, with non-gray cloud using calculated radius'
    )

    __save_contribution_function(
        reference_filenames['correlated_k_transmission_contribution_cloud_calculated_radius'],
        atmosphere_ck,
        mode='transmission',
        plot_figure=plot_figure,
        figure_title='Correlated-k transmission contribution function, '
                     'with non-gray cloud using calculated radius',
        prt_version=version
    )


def create_radtrans_line_by_line_downsampled_emission_spectrum_ref(plot_figure=False):
    from .test_radtrans_line_by_line_sampling import atmosphere_lbl_downsampled

    atmosphere_lbl_downsampled.calc_flux(
        temp=temperature_guillot_2010,
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
    )

    __save_emission_spectrum(
        reference_filenames['line_by_line_downsampled_emission'],
        atmosphere_lbl_downsampled, plot_figure, 'Line-by-line downsampled emission spectrum'
    )


def create_radtrans_line_by_line_downsampled_transmission_spectrum_ref(plot_figure=False):
    from .test_radtrans_line_by_line_sampling import atmosphere_lbl_downsampled

    atmosphere_lbl_downsampled.calc_transm(
        temp=temperature_isothermal,
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure']
    )

    __save_transmission_spectrum(
        reference_filenames['line_by_line_downsampled_transmission'],
        atmosphere_lbl_downsampled, plot_figure, 'Line-by-line downsampled transmission spectrum'
    )


def create_radtrans_line_by_line_emission_spectrum_ref(plot_figure=False):
    from .test_radtrans_line_by_line import atmosphere_lbl

    atmosphere_lbl.calc_flux(
        temp=temperature_guillot_2010,
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
    )

    __save_emission_spectrum(
        reference_filenames['line_by_line_emission'],
        atmosphere_lbl, plot_figure, 'Line-by-line emission spectrum'
    )


def create_radtrans_line_by_line_transmission_spectrum_ref(plot_figure=False):
    from .test_radtrans_line_by_line import atmosphere_lbl

    atmosphere_lbl.calc_transm(
        temp=radtrans_parameters['temperature_isothermal'] * np.ones_like(radtrans_parameters['pressures']),
        abunds=radtrans_parameters['mass_fractions'],
        gravity=radtrans_parameters['planetary_parameters']['surface_gravity'],
        mmw=radtrans_parameters['mean_molar_mass'],
        R_pl=radtrans_parameters['planetary_parameters']['radius'] * petitRADTRANS.nat_cst.r_jup_mean,
        P0_bar=radtrans_parameters['planetary_parameters']['reference_pressure']
    )

    __save_transmission_spectrum(
        reference_filenames['line_by_line_transmission'],
        atmosphere_lbl, plot_figure, 'Line-by-line transmission spectrum'
    )


def create_radtrans_mass_fractions_atmosphere_ref(plot_figure=False):
    c_o_ratios = radtrans_parameters['chemical_parameters']['c_o_ratios'][1] \
        * np.ones_like(radtrans_parameters['pressures'])
    metallicities = radtrans_parameters['chemical_parameters']['metallicities'][1] \
        * np.ones_like(radtrans_parameters['pressures'])

    mass_fractions = petitRADTRANS.poor_mans_nonequ_chem.interpol_abundances(
        COs_goal_in=c_o_ratios,
        FEHs_goal_in=metallicities,
        temps_goal_in=temperature_guillot_2010,
        pressures_goal_in=radtrans_parameters['pressures']
    )

    __save_mass_fractions(
        filename=reference_filenames['mass_fractions_atmosphere'],
        mass_fractions=mass_fractions,
        plot_figure=plot_figure,
        y_axis=radtrans_parameters['pressures'],
        y_label='Pressure (bar)',
        y_lim=[np.max(radtrans_parameters['pressures']), np.min(radtrans_parameters['pressures'])],
        figure_title=' for a Guillot 2010 temperature profile',
        prt_version=version
    )


def create_radtrans_mass_fractions_atmosphere_quench_ref(plot_figure=False):
    c_o_ratios = radtrans_parameters['chemical_parameters']['c_o_ratios'][1] \
        * np.ones_like(radtrans_parameters['pressures'])
    metallicities = radtrans_parameters['chemical_parameters']['metallicities'][1] \
        * np.ones_like(radtrans_parameters['pressures'])

    mass_fractions = petitRADTRANS.poor_mans_nonequ_chem.interpol_abundances(
        COs_goal_in=c_o_ratios,
        FEHs_goal_in=metallicities,
        temps_goal_in=temperature_guillot_2010,
        pressures_goal_in=radtrans_parameters['pressures'],
        Pquench_carbon=radtrans_parameters['chemical_parameters']['pressure_quench_carbon']
    )

    __save_mass_fractions(
        filename=reference_filenames['mass_fractions_atmosphere_quench'],
        mass_fractions=mass_fractions,
        plot_figure=plot_figure,
        y_axis=radtrans_parameters['pressures'],
        y_label='Pressure (bar)',
        y_lim=[np.max(radtrans_parameters['pressures']), np.min(radtrans_parameters['pressures'])],
        figure_title=' for a Guillot 2010 temperature profile',
        prt_version=version
    )


def create_radtrans_mass_fractions_c_o_ratios_ref(plot_figure=False):
    c_o_ratios = np.asarray(radtrans_parameters['chemical_parameters']['c_o_ratios'])
    metallicities = radtrans_parameters['chemical_parameters']['metallicities'][1] * np.ones_like(c_o_ratios)
    pressures = radtrans_parameters['chemical_parameters']['pressure'] * np.ones_like(c_o_ratios)
    temperatures = radtrans_parameters['chemical_parameters']['temperature'] * np.ones_like(c_o_ratios)

    mass_fractions = petitRADTRANS.poor_mans_nonequ_chem.interpol_abundances(
        COs_goal_in=c_o_ratios,
        FEHs_goal_in=metallicities,
        temps_goal_in=temperatures,
        pressures_goal_in=pressures
    )

    __save_mass_fractions(
        filename=reference_filenames['mass_fractions_c_o_ratios'],
        mass_fractions=mass_fractions,
        plot_figure=plot_figure,
        y_axis=c_o_ratios,
        y_label='C/O',
        y_lim=[np.min(c_o_ratios), np.max(c_o_ratios)],
        figure_title=' for different C/O',
        prt_version=version
    )


def create_radtrans_mass_fractions_metallicities_ref(plot_figure=False):
    metallicities = np.asarray(radtrans_parameters['chemical_parameters']['metallicities'])
    c_o_ratios = radtrans_parameters['chemical_parameters']['c_o_ratios'][1] * np.ones_like(metallicities)
    pressures = radtrans_parameters['chemical_parameters']['pressure'] * np.ones_like(metallicities)
    temperatures = radtrans_parameters['chemical_parameters']['temperature'] * np.ones_like(metallicities)

    mass_fractions = petitRADTRANS.poor_mans_nonequ_chem.interpol_abundances(
        COs_goal_in=c_o_ratios,
        FEHs_goal_in=metallicities,
        temps_goal_in=temperatures,
        pressures_goal_in=pressures,
    )

    __save_mass_fractions(
        filename=reference_filenames['mass_fractions_metallicities'],
        mass_fractions=mass_fractions,
        plot_figure=plot_figure,
        y_axis=10 ** metallicities,
        y_label='[Fe/H]',
        y_lim=[10 ** np.min(metallicities), 10 ** np.max(metallicities)],
        figure_title=' for different metallicities',
        prt_version=version
    )


def create_all_comparison_files(plot_figure=False):
    create_guillot_2010_temperature_profile_ref(plot_figure)

    create_radtrans_correlated_k_emission_spectrum_ref(plot_figure)
    create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_ref(plot_figure)
    create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_scattering_ref(plot_figure)
    create_radtrans_correlated_k_emission_spectrum_cloud_calculated_radius_stellar_scattering_ref(plot_figure)
    create_radtrans_correlated_k_emission_spectrum_cloud_hansen_radius_ref(plot_figure)
    create_radtrans_correlated_k_emission_spectrum_surface_scattering_ref(plot_figure)

    create_radtrans_correlated_k_transmission_spectrum_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_cloud_power_law_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_rayleigh_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_gray_cloud_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_cloud_fixed_radius_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_cloud_calculated_radius_ref(plot_figure)
    create_radtrans_correlated_k_transmission_spectrum_cloud_calculated_radius_scattering_ref(plot_figure)

    create_radtrans_line_by_line_downsampled_emission_spectrum_ref(plot_figure)
    create_radtrans_line_by_line_downsampled_transmission_spectrum_ref(plot_figure)
    create_radtrans_line_by_line_emission_spectrum_ref(plot_figure)
    create_radtrans_line_by_line_transmission_spectrum_ref(plot_figure)

    create_radtrans_mass_fractions_atmosphere_ref(plot_figure)
    create_radtrans_mass_fractions_atmosphere_quench_ref(plot_figure)
    create_radtrans_mass_fractions_c_o_ratios_ref(plot_figure)
    create_radtrans_mass_fractions_metallicities_ref(plot_figure)

    create_mock_observation_transmission_spectrum(plot_figure)
