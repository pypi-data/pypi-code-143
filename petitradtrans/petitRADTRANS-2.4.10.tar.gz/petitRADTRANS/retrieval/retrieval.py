# Input / output, general run definitions
import sys
import os
# To not have numpy start parallelizing on its own
os.environ["OMP_NUM_THREADS"] = "1"
# Read external packages
import numpy as np
import copy as cp

import json
import logging
from scipy.stats import binned_statistic
# Plotting
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter
# Read own packages
from petitRADTRANS import Radtrans
from petitRADTRANS import nat_cst as nc
from .parameter import Parameter
from .data import Data
from .plotting import plot_specs,plot_data,contour_corner
from .rebin_give_width import rebin_give_width as rgw
from .util import bin_species_exok

class Retrieval:
    """
    This class implements the retrieval method using petitRADTRANS and pymultinest.
    A RetrievalConfig object is passed to this class to describe the retrieval data, parameters
    and priors. The run() method then uses pymultinest to sample the parameter space, producing
    posterior distributions for parameters and bayesian evidence for models.
    Various useful plotting functions have also been included, and can be run once the retrieval is
    complete.

    Args:
        run_definition : RetrievalConfig
            A RetrievalConfig object that describes the retrieval to be run. This is the user
            facing class that must be setup for every retrieval.
        output_dir : Str
            The directory in which the output folders should be written
        test_plotting : Bool
            Only use when running locally. A boolean flag that will produce plots
            for each sample when pymultinest is run.
        sample_spec : Bool
            Produce plots and data files for 100 randomly sampled outputs from pymultinest.
        ultranest : bool
            If true, use Ultranest sampling rather than pymultinest. This is still a work
            in progress, so use with caution!
        bayes_factor_species : Str
            A pRT species that should be removed to test for the bayesian evidence for it's presence.
        corner_plot_names : List(Str)
            List of additional retrieval names that should be included in the corner plot.
        short_names : List(Str)
            For each corner_plot_name, a shorter name to be included when plotting.
        pRT_plot_style : Bool
            Use the petitRADTRANS plotting style as described in plot_style.py. Recommended to
            turn this parameter to false if you want to use interactive plotting, or if the
            test_plotting parameter is True.
    """

    def __init__(self,
                 run_definition,
                 output_dir = "",
                 test_plotting = False,
                 sample_spec = False,
                 ultranest = False,
                 sampling_efficiency = None,\
                 const_efficiency_mode = None, \
                 n_live_points = None,
                 resume = None,
                 bayes_factor_species = None,
                 corner_plot_names = None,
                 short_names = None,
                 pRT_plot_style = True):

        self.rd = run_definition
        print(f"Starting retrieval {self.rd.retrieval_name}")
        if len(self.rd.line_species) < 1:
            logging.warning("There are no line species present in the run definition!")

        # Maybe inherit from retrieval config class?
        self.retrieval_name = self.rd.retrieval_name
        self.data = self.rd.data
        self.run_mode = self.rd.run_mode
        self.parameters = self.rd.parameters
        self.ultranest = ultranest

        self.output_dir = output_dir
        if self.output_dir != "" and not self.output_dir.endswith("/"):
            self.output_dir += "/"

        self.remove_species = bayes_factor_species
        self.corner_files = corner_plot_names
        if self.corner_files is None:
            self.corner_files = [self.retrieval_name]
        self.short_names = short_names

        # Plotting variables
        self.best_fit_specs = {}
        self.best_fit_params = {}
        self.chi2 = None
        self.posterior_sample_specs = {}
        self.plotting = test_plotting
        self.PT_plot_mode = False
        self.evaluate_sample_spectra = sample_spec

        # Pymultinest stuff
        self.sampling_efficiency = sampling_efficiency
        self.const_efficiency_mode = const_efficiency_mode
        self.n_live_points = n_live_points
        self.resume = resume
        self.analyzer = None

        self.samples = {} #: The samples produced by pymultinest.
        self.param_dict = {}
        # Set up pretty plotting
        if pRT_plot_style:
            import petitRADTRANS.retrieval.plot_style
        self.prt_plot_style =pRT_plot_style
        # Path to input opacities
        self.path = os.environ.get("pRT_input_data_path")
        if self.path is None:
            raise OSError(f"Path to input data not specified!\n"
                          f"Please set pRT_input_data_path variable in .bashrc / .bash_profile or specify path via\n"
                          f">>> import os"
                          f">>> os.environ['pRT_input_data_path'] = 'absolute/path/of/the/folder/input_data'\n"
                          f"before creating a Radtrans object or loading the nat_cst module.\n"
                          f"(this will become unnecessary in a future update)"
                          )
        if not self.path.endswith("/"):
            self.path += "/"
        # Setup Directories
        if not os.path.isdir(self.output_dir + 'out_PMN/'):
            os.makedirs(self.output_dir + 'out_PMN', exist_ok=True)
        if not os.path.isdir(self.output_dir + 'evaluate_' + self.retrieval_name +'/'):
            os.makedirs(self.output_dir + 'evaluate_' + self.retrieval_name, exist_ok=True)

        # Setup pRT Objects for each data structure.
        print("Setting up PRT Objects")
        self.setup_data()
        try:
            self.generate_retrieval_summary()
        except:
            print("Could not generate summary file!")


    def run(self,
            sampling_efficiency = 0.8,
            const_efficiency_mode = False,
            n_live_points = 4000,
            log_z_convergence = 0.5,
            step_sampler = False,
            warmstart_max_tau=0.5,
            n_iter_before_update=50,
            resume = True,
            max_iters = 0,
            frac_remain=0.1,
            Lepsilon=0.3):
        """
        Run mode for the class. Uses pynultinest to sample parameter space
        and produce standard PMN outputs.

        Args:
            sampling_efficiency : Float
                pymultinest sampling efficiency. If const efficiency mode is true, should be set to around
                0.05. Otherwise, it should be around 0.8 for parameter estimation and 0.3 for evidence
                comparison.
            const_efficiency_mode : Bool
                pymultinest constant efficiency mode
            n_live_points : Int
                Number of live points to use in pymultinest, or the minimum number of live points to
                use for the Ultranest reactive sampler.
            log_z_convergence : float
                If ultranest is being used, the convergence criterion on log z.
            step_sampler : bool
                Use a step sampler to improve the efficiency in ultranest.
            warmstart_max_tau : float
                Warm start allows accelerated computation based on a different but similar UltraNest run.
            resume : bool
                Continue existing retrieval. If FALSE THIS WILL OVERWRITE YOUR EXISTING RETRIEVAL.
        """
        if self.sampling_efficiency is not None:
            logging.warning("Setting sampling_efficiency as a class variable will be deprecated. Use the run method arguments.")
            sampling_efficiency = self.sampling_efficiency
        if self.n_live_points:
            logging.warning("Setting n_live_points as a class variable will be deprecated. Use the run method arguments.")
            n_live_points = self.n_live_points
        if self.resume is not None:
            logging.warning("Setting resume as a class variable will be deprecated. Use the run method arguments.")
            resume = self.resume
        if self.const_efficiency_mode is not None:
            logging.warning("Setting const_efficiency_mode as a class variable will be deprecated. Use the run method arguments.")
            const_efficiency_mode = self.const_efficiency_mode
        if self.ultranest:
            self._run_ultranest(n_live_points = n_live_points,
                                log_z_convergence = log_z_convergence,
                                step_sampler = step_sampler,
                                warmstart_max_tau = warmstart_max_tau,
                                resume = resume,
                                max_iters = max_iters,
                                frac_remain = frac_remain,
                                Lepsilon =Lepsilon)
            return


        import pymultinest
        if const_efficiency_mode and sampling_efficiency > 0.1:
            logging.warning("Sampling efficiency should be ~ 0.05 if you're using constant efficiency mode!")
        prefix = self.output_dir + 'out_PMN/'+self.retrieval_name+'_'

        if len(self.output_dir + 'out_PMN/') > 100:
            logging.error("PyMultinest requires output directory names to be <100 characters.")
            sys.exit(3)

        # How many free parameters?
        n_params = 0
        free_parameter_names = []
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                free_parameter_names.append(self.parameters[pp].name)
                n_params += 1
        if self.run_mode == 'retrieval':
            print("Starting retrieval: " + self.retrieval_name+'\n')
            json.dump(free_parameter_names, \
                    open(self.output_dir + 'out_PMN/'+self.retrieval_name+'_params.json', 'w'))
            pymultinest.run(self.log_likelihood,
                            self.prior,
                            n_params,
                            outputfiles_basename=prefix,
                            resume = resume,
                            verbose = True,
                            sampling_efficiency = sampling_efficiency,
                            const_efficiency_mode = const_efficiency_mode,
                            evidence_tolerance = log_z_convergence,
                            n_live_points = n_live_points,
                            n_iter_before_update = n_iter_before_update,
                            max_iter = max_iters)
        self.analyzer = pymultinest.Analyzer(n_params = n_params,
                                             outputfiles_basename = prefix)
        s = self.analyzer.get_stats()
        self.run_mode = 'evaluate'
        self.generate_retrieval_summary(s)
        json.dump(s, open(prefix + 'stats.json', 'w'), indent=4)
        print('  marginal likelihood:')
        print('    ln Z = %.1f +- %.1f' % (s['global evidence'], s['global evidence error']))
        print('  parameters:')


        for p, m in zip(free_parameter_names, s['marginals']):
            lo, hi = m['1sigma']
            med = m['median']
            sigma = (hi - lo) / 2
            if sigma == 0:
                i = 3
            else:
                i = max(0, int(-np.floor(np.log10(sigma))) + 1)
            fmt = '%%.%df' % i
            fmts = '\t'.join(['    %-15s' + fmt + " +- " + fmt])
            print(fmts % (p, med, sigma))

    def _run_ultranest(self,
                       n_live_points,
                       log_z_convergence,
                       step_sampler,
                       warmstart_max_tau,
                       resume,
                       max_iters,
                       frac_remain,
                       Lepsilon):
        """
        Run mode for the class. Uses ultranest to sample parameter space
        and produce standard outputs.

        Args:
            n_live_points : Int
                The minimum number of live points to
                use for the Ultranest reactive sampler.
            log_z_convergence : float
                The convergence criterion on log z.
            step_sampler : bool
                Use a step sampler to improve the efficiency in ultranest.
            resume : bool
                Continue existing retrieval. If FALSE THIS WILL OVERWRITE YOUR EXISTING RETRIEVAL.
        """

        logging.warning("ultranest mode is still in development. Proceed with caution")
        try:
            import ultranest as un
            from ultranest.mlfriends import RobustEllipsoidRegion
        except ImportError:
            logging.error("Could not import ultranest. Exiting.")
            sys.exit(1)
        if self.run_mode == 'retrieval':
            print("Starting retrieval: " + self.retrieval_name+'\n')
            # How many free parameters?
            n_params = 0
            free_parameter_names = []
            for pp in self.parameters:
                if self.parameters[pp].is_free_parameter:
                    free_parameter_names.append(self.parameters[pp].name)
                    n_params += 1

            if max_iters == 0:
                max_iters = None
            sampler = un.ReactiveNestedSampler(free_parameter_names,
                                               self.log_likelihood,
                                               self.prior_ultranest,
                                               log_dir=self.output_dir + "out_" + self.retrieval_name,
                                               warmstart_max_tau=warmstart_max_tau,
                                               resume=resume)
            if step_sampler:
                #try:
                import ultranest.stepsampler
                #    #sampler.run(min_num_live_points=400,
                #    #        max_n_calls = 400000,
                #    #        region_class =  RobustEllipsoidRegion)
                sampler.stepsampler = ultranest.stepsampler.SliceSampler(nsteps=50,
                                                                         adaptive_nsteps='move-distance',
                                                                         generate_direction=ultranest.stepsampler.generate_mixture_random_direction)
                #except:
                #    logging.error("Could not use step sampling!")
                #    sys.exit(13)
            sampler.run(min_num_live_points = n_live_points,
                       dlogz = log_z_convergence,
                       max_iters = max_iters,
                       frac_remain = frac_remain,
                       Lepsilon = Lepsilon,
                       region_class =  RobustEllipsoidRegion)
            sampler.print_results()
            sampler.plot_corner()


    def generate_retrieval_summary(self,stats = None):
        """
        This function produces a human-readable text file describing the retrieval.
        It includes all of the fixed and free parameters, the limits of the priors (if uniform),
        a description of the data used, and if the retrieval is complete, a summary of the
        best fit parameters and model evidence.

        Args:
            stats : dict
                A Pymultinest stats dictionary, from Analyzer.get_stats().
                This contains the evidence and best fit parameters.
        """

        with open(self.output_dir + "evaluate_" + self.retrieval_name + "/" + self.retrieval_name +\
                  "_ret_summary.txt", "w+") as summary:
            from datetime import datetime
            summary.write(self.retrieval_name + '\n')
            summary.write(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + '\n')
            summary.write(self.output_dir + '\n\n')
            summary.write("Fixed Parameters\n")
            for key,value in self.parameters.items():
                if key in ['pressure_simple', 'pressure_width', 'pressure_scaling']:
                    continue
                if not value.is_free_parameter:
                    try:
                        summary.write(f"    {key} = {value.value:.3f}\n")
                    except TypeError:
                        summary.write(f"    {key} = is function!")
            summary.write('\n')
            summary.write("Free Parameters, Prior^-1(0), Prior^-1(1)\n")
            for key,value in self.parameters.items():
                if value.is_free_parameter:
                    low = value.transform_prior_cube_coordinate(0.0000001)
                    high = value.transform_prior_cube_coordinate(0.9999999)
                    if value.corner_transform is not None:
                        low = value.corner_transform(low)
                        high = value.corner_transform(high)
                    summary.write(f"    {key} = {low:3f}, {high:3f}\n")
            summary.write('\n')
            summary.write("Data\n")
            for name,dd in self.data.items():
                summary.write(name+'\n')
                summary.write("    " + dd.path_to_observations + '\n')
                if dd.model_generating_function is not None:
                    summary.write(f"    Model Function = {dd.model_generating_function.__name__}\n")
                if dd.scale:
                    summary.write(f"    scale factor = {dd.scale_factor:.2f}\n")
                if dd.data_resolution is not None:
                    summary.write(f"    data resolution = {dd.data_resolution}\n")
                if dd.model_resolution is not None:
                    summary.write(f"    model resolution = {dd.model_resolution}\n")
                if dd.photometry:
                    summary.write(f"    photometric width = {dd.photometry_range[0]:.4f}" + \
                                  f"--{dd.photometry_range[1]:.4f} um\n")
                    summary.write("    Photometric transform function = " + \
                                  dd.photometric_transformation_function.__name__+ '\n')
            summary.write('\n')

            if stats is not None:
                summary.write("Multinest Outputs\n")
                summary.write('  marginal evidence:\n')
                summary.write('    log Z = %.1f +- %.1f\n' % \
                             (stats['global evidence']/np.log(10), stats['global evidence error']/np.log(10)))
                summary.write('    ln Z = %.1f +- %.1f\n' % (stats['global evidence'], \
                              stats['global evidence error']))
                summary.write("  Statistical Fit Parameters\n")

                free_params = []
                for key,value in self.parameters.items():
                    if value.is_free_parameter:
                        free_params.append(key)

                for p, m in zip(free_params, stats['marginals']):
                    lo, hi = m['1sigma']
                    med = m['median']
                    sigma = (hi - lo) / 2
                    if sigma == 0:
                        i = 3
                    else:
                        i = max(0, int(-np.floor(np.log10(sigma))) + 1)
                    fmt = '%%.%df' % i
                    fmts = '\t'.join(['    %-15s' + fmt + " +- " + fmt])
                    summary.write(fmts % (p, med, sigma) + '\n')
                summary.write('\n')
            if self.run_mode == 'evaluate':
                summary.write("Best Fit Parameters\n")
                if not self.best_fit_params:
                    self.get_samples(self.output_dir)
                    samples_use = self.samples[self.retrieval_name]
                    parameters_read = self.param_dict[self.retrieval_name]
                    # Get best-fit index
                    logL ,best_fit_index = self.get_best_fit_likelihood(samples_use)
                    self.get_best_fit_params(samples_use[best_fit_index,:-1],parameters_read)
                summary.write(f"    chi^{2} = {self.chi2}\n")
                for key,value in self.best_fit_params.items():
                    if key in ['pressure_simple', 'pressure_width', 'pressure_scaling', 'FstarWlenMicron']:
                        continue
                    out = value.value
                    if self.parameters[key].corner_transform is not None:
                        out = self.parameters[key].corner_transform(out)
                    if out is None:
                        continue
                    summary.write(f"    {key} = {out:.3f}\n")

    def setup_data(self,scaling=10,width = 3):
        """
        Creates a pRT object for each data set that asks for a unique object.
        Checks if there are low resolution c-k models from exo-k, and creates them if necessary.
        The scaling and width parameters adjust the AMR grid as described in RetrievalConfig.setup_pres
        and models.fixed_length_amr. It is recommended to keep the defaults.

        Args:
            scaling : int
                A multiplicative factor that determines the size of the full high resolution pressure grid,
                which will have length self.p_global.shape[0] * scaling.
            width : int
                The number of cells in the low pressure grid to replace with the high resolution grid.
        """
        exo_k_check = False
        for name,dd in self.data.items():
            # Only create if there's no other data
            # object using the same pRT object
            if dd.external_pRT_reference is None:
                if dd.opacity_mode == 'c-k' and dd.model_resolution is not None:
                    # Use ExoK to have low res models.
                    species = []
                    # Check if low res opacities already exist
                    for line in self.rd.line_species:
                        if not os.path.isdir(self.path + "opacities/lines/corr_k/" +\
                                                line + "_R_" + \
                                                str(dd.model_resolution)):
                            species.append(line)
                    # If not, setup low-res c-k tables
                    if len(species)>0:
                        exo_k_check = True
                        print("Exo-k should only be run on a single thread.")
                        print("The retrieval should be run once on a single core to build the c-k\ntables, and then again with multiple cores for the remainder of the retrieval.")
                        # Automatically build the entire table
                        bin_species_exok(species,dd.model_resolution)
                    species = []
                    for spec in self.rd.line_species:
                        species.append(spec + "_R_" + str(dd.model_resolution))
                else:
                    # Otherwise for 'lbl' or no model_resolution binning,
                    # we just use the default species.
                    species = cp.copy(self.rd.line_species)
                lbl_samp = None
                if dd.opacity_mode == 'lbl' and dd.model_resolution is not None:
                    lbl_samp = int(1e6/dd.model_resolution)

                # Setup the pRT objects for the given dataset
                rt_object = Radtrans(line_species = cp.copy(species), \
                                    rayleigh_species= cp.copy(self.rd.rayleigh_species), \
                                    continuum_opacities = cp.copy(self.rd.continuum_opacities), \
                                    cloud_species = cp.copy(self.rd.cloud_species), \
                                    mode=dd.opacity_mode, \
                                    wlen_bords_micron = dd.wlen_range_pRT,
                                    do_scat_emis = self.rd.scattering,
                                    lbl_opacity_sampling = lbl_samp)
                # Create random P-T profile to create RT arrays of the Radtrans object.
                if self.rd.AMR:
                    p = self.rd._setup_pres(scaling,width)
                else:
                    p = self.rd.p_global
                rt_object.setup_opa_structure(p)
                dd.pRT_object = rt_object
        if exo_k_check:
            # Sorry that we have to do this, not sure how to use mpi4py to run the
            # exo-k in a single thread.
            print("c-k tables have been binned with exo-k. Exiting single-core process.")
            print("Please restart the retrieval.")
            sys.exit(12)

    def prior(self, cube, ndim=0, nparams=0):
        """
        pyMultinest Prior function. Transforms unit hypercube into physical space.
        """

        i_p = 0
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                cube[i_p] = self.parameters[pp].get_param_uniform(cube[i_p])
                i_p += 1
    def prior_ultranest(self, cube):
        """
        pyMultinest Prior function. Transforms unit hypercube into physical space.
        """
        params = cube.copy()
        i_p = 0
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                params[i_p] = self.parameters[pp].get_param_uniform(cube[i_p])
                i_p += 1
        return params

    def log_likelihood(self,cube,ndim=0,nparam=0):
        """
        pyMultiNest required likelihood function.

        This function wraps the model computation and log-likelihood calculations
        for pyMultiNest to sample. If PT_plot_mode is True, it will return the
        calculate only the pressure and temperature arrays rather than the wavlength
        and flux. If run_mode is evaluate, it will save the provided sample to the
        best-fit spectrum file, and add it to the best_fit_specs dictionary.
        If evaluate_sample_spectra is true, it will store the spectrum in
        posterior_sample_specs.

        Args:
            cube : numpy.ndarray
                The transformed unit hypercube, providing the parameter values
                to be passed to the model_generating_function.
            ndim : int
                The number of dimensions of the problem
            nparam : int
                The number of parameters in the fit.

        Returns:
            log_likelihood : float
                The (negative) log likelihood of the model given the data.
        """

        log_likelihood = 0.
        log_prior      = 0.

        i_p = 0 # parameter count
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                self.parameters[pp].set_param(cube[i_p])
                i_p += 1

        for name,dd in self.data.items():
            # Only calculate spectra within a given
            # wlen range once
            if dd.scale:
                dd.scale_factor = self.parameters[name + "_scale_factor"].value
            if dd.external_pRT_reference is None:
                if not self.PT_plot_mode:
                    # Compute the model
                    wlen_model, spectrum_model = \
                        dd.model_generating_function(dd.pRT_object,
                                                    self.parameters,
                                                    self.PT_plot_mode,
                                                    AMR = self.rd.AMR)
                    # Sanity checks on outputs
                    if spectrum_model is None:
                        return -1e98
                    if np.isnan(spectrum_model).any():
                        return -1e98
                    log_likelihood += dd.get_chisq(wlen_model,
                                            spectrum_model,
                                            self.plotting,
                                            self.parameters)
                else:
                    # Get the PT profile
                    if name == self.rd.plot_kwargs["take_PTs_from"]:
                        pressures, temperatures = \
                            dd.model_generating_function(dd.pRT_object,
                                                         self.parameters,
                                                         self.PT_plot_mode,
                                                         AMR = self.rd.AMR)
                        return pressures, temperatures
                    else:
                        continue
                # Save sampled outputs if necessary.
                if self.run_mode == 'evaluate':
                    if self.evaluate_sample_spectra:
                        self.posterior_sample_specs[name] = [wlen_model, \
                                                spectrum_model]
                    else:
                        np.savetxt(self.output_dir + 'evaluate_' + self.retrieval_name + \
                                   '/model_spec_best_fit_'+
                                   name.replace('/','_').replace('.','_')+'.dat',
                                   np.column_stack((wlen_model,
                                                    spectrum_model)))

                        self.best_fit_specs[name] = [wlen_model, \
                                                spectrum_model]

            # Check for data using the same pRT object,
            # calculate log_likelihood
            for de_name,dede in self.data.items():
                if dede.external_pRT_reference is not None:
                    if dede.scale:
                        dd.scale_factor = self.parameters[de_name + "_scale_factor"].value
                    if dede.external_pRT_reference == name:
                        if spectrum_model is None:
                            return -1e99
                        if np.isnan(spectrum_model).any():
                            return -1e99
                        log_likelihood += dede.get_chisq(wlen_model, \
                                        spectrum_model, \
                                        self.plotting,
                                        self.parameters)
        #print(f"LL: {log_likelihood+log_prior}")
        if log_likelihood + log_prior < -9e98:
            return -1e98
        if np.abs(log_likelihood + log_prior) < 1e-98:
            return -1e-98
        if self.ultranest and np.isinf(log_likelihood+log_prior):
            return -1e98
        return log_likelihood + log_prior

    def get_samples(self, output_dir = None, ret_names = []):
        """
        This function looks in the given output directory and finds the post_equal_weights
        file associated with the current retrieval name.

        Args:
            output_dir : str
                Parent directory of the out_PMN/RETRIEVALNAME_post_equal_weights.dat file
            ret_names : List(str)
                A list of retrieval names to add to the sample and parameter dictionary.
                Functions the same as setting corner_files during initialisation.

        Returns:
            sample_dict : dict
                A dictionary with keys being the name of the retrieval, and values are a numpy
                ndarray containing the samples in the post_equal_weights file
            parameter_dict : dict
                A dictionary with keys being the name of the retrieval, and values are a list of names
                of the parameters used in the retrieval. The first name corresponds to the first column
                of the samples, and so on.
        """

        if output_dir is None:
            output_dir = self.output_dir
        if self.ultranest:
            for name in self.corner_files:
                samples = np.genfromtxt(output_dir +'out_' + name + '/chains/equal_weighted_post.txt')
                #TODO formatting of paramname file
                parameters_read = open(output_dir +'out_' + name + '/chains/weighted_post.paramnames')
                self.samples[name] = samples
                self.param_dict[name] = parameters_read
            for name in ret_names:
                samples = np.genfromtxt(output_dir +'out_' + name + '/chains/qual_weighted_post.txt')
                parameters_read = open(output_dir +'out_' + name + '/chains/weighted_post.paramnames')
                self.samples[name] = samples
                self.param_dict[name] = parameters_read
            return self.samples, self.param_dict

        # pymultinest
        for name in self.corner_files:
            samples = np.genfromtxt(output_dir +'out_PMN/'+ \
                                    name+ \
                                    '_post_equal_weights.dat')

            parameters_read = json.load(open(output_dir + 'out_PMN/'+ \
                                        name+ \
                                        '_params.json'))
            self.samples[name] = samples
            self.param_dict[name] = parameters_read
        for name in ret_names:
            samples = np.genfromtxt(output_dir +'out_PMN/'+ \
                                    name+ \
                                    '_post_equal_weights.dat')

            parameters_read = json.load(open(output_dir + 'out_PMN/'+ \
                                        name+ \
                                        '_params.json'))
            self.samples[name] = samples
            self.param_dict[name] = parameters_read
        return self.samples, self.param_dict

    def get_best_fit_params(self,best_fit_params,parameters_read):
        """
        This function converts the sample from the post_equal_weights file with the maximum
        log likelihood, and converts it into a dictionary of Parameters that can be used in
        a model function.

        Args:
            best_fit_params : numpy.ndarray
                An array of the best fit parameter values (or any other sample)
            parameters_read : list
                A list of the free parameters as read from the output files.
        """
        self.best_fit_params = self.build_param_dict(best_fit_params,parameters_read)
        return self.best_fit_params

    def get_full_range_model(self,
                             parameters,
                             model_generating_func = None,
                             ret_name = None,
                             contribution = False,
                             pRT_object = None):
        # Find the boundaries of the wavelength range to calculate
        wmin = 99999.0
        wmax = 0.0
        for name,dd in self.data.items():
            if dd.wlen_range_pRT[0] < wmin:
                wmin = dd.wlen_range_pRT[0]
            if dd.wlen_range_pRT[1] > wmax:
                wmax = dd.wlen_range_pRT[1]
        # Set up parameter dictionary
        #parameters = self.build_param_dict(params,parameters_read)
        parameters["contribution"] = Parameter("contribution", False, value = contribution)

        # Setup the pRT object
        if pRT_object is not None:
            atmosphere = pRT_object
        else:
            atmosphere = Radtrans(line_species = cp.copy(self.rd.line_species), \
                                rayleigh_species= cp.copy(self.rd.rayleigh_species), \
                                continuum_opacities = cp.copy(self.rd.continuum_opacities), \
                                cloud_species = cp.copy(self.rd.cloud_species), \
                                mode='c-k', \
                                wlen_bords_micron = [wmin*0.98,wmax*1.02],
                                do_scat_emis = self.rd.scattering)
        if self.rd.AMR:
            p = self.rd._setup_pres()
            parameters["pressure_scaling"] = self.parameters["pressure_scaling"]
            parameters["pressure_width"] = self.parameters["pressure_width"]
            parameters["pressure_simple"] = self.parameters["pressure_simple"]
        else:
            p = self.rd.p_global
        atmosphere.setup_opa_structure(p)

        # Check what model function we're using
        if model_generating_func is None:
            mg_func = self.data[self.rd.plot_kwargs["take_PTs_from"]].model_generating_function
        else:
            mg_func = model_generating_func

        # get the spectrum
        return mg_func(atmosphere, parameters, PT_plot_mode= False, AMR = self.rd.AMR)


    def get_best_fit_model(self,best_fit_params,parameters_read,ret_name = None, contribution = False):
        """
        This function uses the best fit parameters to generate a pRT model that spans the entire wavelength
        range of the retrieval, to be used in plots.

        Args:
            best_fit_params : numpy.ndarray
                A numpy array containing the best fit parameters, to be passed to get_best_fit_params
            parameters_read : list
                A list of the free parameters as read from the output files.
            model_generating_fun : method
                A function that will take in the standard 'model' arguments
                (pRT_object, params, pt_plot_mode, AMR, resolution)
                and will return the wavlength and flux arrays as calculated by petitRadTrans.
                If no argument is given, it uses the method of the dataset given in the take_PTs_from kwarg.
            ret_name : str
                If plotting a fit from a different retrieval, input the retrieval name to be included.

        Returns:
            bf_wlen : numpy.ndarray
                The wavelength array of the best fit model
            bf_spectrum : numpy.ndarray
                The emission or transmission spectrum array, with the same shape as bf_wlen
        """

        print("Computing Best Fit Model, this may take a minute...")
        if ret_name is None:
            ret_name = self.retrieval_name
        # Check if the files already exist so that we don't have to recalculate


        if not self.retrieval_name in self.best_fit_specs.keys():
            self.get_best_fit_params(best_fit_params,parameters_read)

        if self.rd.AMR:
            p = self.rd._setup_pres()
            self.best_fit_params["pressure_scaling"] = self.parameters["pressure_scaling"]
            self.best_fit_params["pressure_width"] = self.parameters["pressure_width"]
            self.best_fit_params["pressure_simple"] = self.parameters["pressure_simple"]
        if contribution:
            if os.path.exists(self.output_dir + "evaluate_" + \
                              self.retrieval_name + "/" + \
                              ret_name + "_best_fit_model_contribution.npy"):
                print("Loading best fit spectrum and contribution from file")
                bf_contribution = np.load(self.output_dir + "evaluate_" + \
                                          self.retrieval_name + "/" + \
                                          ret_name + "_best_fit_model_contribution.npy")
                bf_wlen,bf_spectrum = np.load(self.output_dir + "evaluate_" + \
                                          self.retrieval_name + "/" + \
                                          ret_name + "_best_fit_model_full.npy").T
                return bf_wlen, bf_spectrum, bf_contribution
            bf_wlen, bf_spectrum, bf_contribution = self.get_full_range_model(self.best_fit_params,
                                                                              model_generating_func = None,
                                                                              ret_name = ret_name,
                                                                              contribution = contribution)
            np.save(self.output_dir + "evaluate_" + \
                self.retrieval_name + "/" + \
                ret_name + "_best_fit_model_contribution",
                bf_contribution)
        else:
            if os.path.exists(self.output_dir + "evaluate_" + \
                          self.retrieval_name + "/" + \
                          ret_name + "_best_fit_model_full.npy"):
                print("Loading best fit spectrum from file")
                bf_wlen,bf_spectrum = np.load(self.output_dir + "evaluate_" + \
                                            self.retrieval_name + "/" + \
                                            ret_name + "_best_fit_model_full.npy").T
                return bf_wlen,bf_spectrum
            bf_wlen, bf_spectrum = self.get_full_range_model(self.best_fit_params,
                                                             model_generating_func = None,
                                                             ret_name = ret_name,
                                                             contribution = contribution)

        # Add to the dictionary.
        self.best_fit_specs[ret_name]= [bf_wlen,bf_spectrum]
        np.save(self.output_dir + "evaluate_" + \
                self.retrieval_name + "/" + \
                ret_name + "_best_fit_model_full",
                np.column_stack([bf_wlen,bf_spectrum]))
        if contribution:
            return bf_wlen, bf_spectrum, bf_contribution
        return bf_wlen, bf_spectrum

    def get_abundances(self,sample,parameters_read=None):
        """
        This function returns the abundances of each species as a function of pressure

        Args:
            sample : numpy.ndarray
                A sample from the pymultinest output, the abundances returned will be
                computed for this set of parameters.
        Returns:
            abundances : dict
                A dictionary of abundances. The keys are the species name,
                the values are the mass fraction abundances at each pressure
            MMW : numpy.ndarray
                The mean molecular weight at each pressure level in the atmosphere.
        """
        from petitRADTRANS.retrieval.chemistry import get_abundances
        parameters = self.build_param_dict(sample,parameters_read)

        self.PT_plot_mode = True
        pressures, temps = self.log_likelihood(sample, 0, 0)
        self.PT_plot_mode = False

        name = self.rd.plot_kwargs["take_PTs_from"]
        abundances, MMW, _, _ = get_abundances(pressures,
                                            temps,
                                            cp.copy(self.data[name].pRT_object.line_species),
                                            cp.copy(self.data[name].pRT_object.cloud_species),
                                            parameters,
                                            AMR=False)
        return abundances, MMW

    def get_evidence(self, ret_name = ""):
        """
        Get the log10 Z and error for the retrieval

        This function uses the pymultinest analyzer to
        get the evidence for the current retrieval_name
        by default, though any retrieval_name in the
        out_PMN folder can be passed as an argument -
        useful for when you're comparing multiple similar
        models. This value is also printed in the summary file.

        Args:
            ret_name : string
                The name of the retrieval that prepends all of the PMN
                output files.
        """
        analyzer = self.get_analyzer(ret_name)
        s = analyzer.get_stats()
        return s['global evidence']/np.log(10), s['global evidence error']/np.log(10)

    def get_best_fit_likelihood(self,samples):
        """
        Get the log likelihood of the best fit model

        Args:
            samples : numpy.ndarray
                An array of samples and likelihoods taken from a post_equal_weights file
        """
        logL = samples[:,-1]
        best_fit_index = np.argmax(logL)
        print(f"Best fit likelihood = {logL[best_fit_index]:.2f}")
        return logL[best_fit_index], best_fit_index

    def get_best_fit_chi2(self,samples):
        """
        Get the 𝛘^2 of the best fit model - removing normalization term from log L

        Args:
            samples : numpy.ndarray
                An array of samples and likelihoods taken from a post_equal_weights file
        """
        logL, best_fit_index = self.get_best_fit_likelihood(samples)
        norm = 0.0
        for name, dd in self.data.items():
            if dd.covariance is not None:
                add = 0.5 * dd.log_covariance_determinant
            else:
                add = 0.5*np.sum(np.log(2*np.pi*dd.flux_error**2.))
            norm += add
            #print(name,norm)
        print(f"Best fit 𝛘^2 = {-logL - norm:.2f}")
        return (-logL - norm)*2.

    def get_reduced_chi2(self,samples):
        """
        Get the 𝛘^2/DoF of the best fit model - divide chi^2 by DoF

        Args:
            samples : numpy.ndarray
                An array of samples and likelihoods taken from a post_equal_weights file
        """
        chi2 = self.get_best_fit_chi2(samples)
        DoF = 0
        for name, dd in self.data.items():
            DoF += np.size(dd.flux)
        for name, pp in self.parameters.items():
            if pp.is_free_parameter:
                DoF -= 1
        print(f"Best fit 𝛘^2/DoF = {chi2/DoF:.2f}")
        self.chi2 = chi2/DoF
        return chi2/DoF

    def get_analyzer(self,ret_name = ""):
        """
        Get the PMN analyer from a retrieval run

        This function uses gets the PMN analyzer object
        for the current retrieval_name by default,
        though any retrieval_name in the out_PMN folder can
        be passed as an argument - useful for when you're
        comparing multiple similar models.

        Args:
            ret_name : string
                The name of the retrieval that prepends all of the PMN
                output files.
        """
        # Avoid loading if we just want the current retrievals output
        if ret_name == "" and self.analyzer is not None:
            return self.analyzer
        if ret_name == "":
            ret_name = self.retrieval_name
        prefix = self.output_dir + 'out_PMN/'+ret_name+'_'

        # How many free parameters?
        n_params = 0
        free_parameter_names = []
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                free_parameter_names.append(self.parameters[pp].name)
                n_params += 1

        # Get the outputs
        analyzer = pymultinest.Analyzer(n_params = n_params,
                                        outputfiles_basename = prefix)
        if ret_name == self.retrieval_name:
            self.analyzer = analyzer
        return analyzer

    def build_param_dict(self,sample,free_param_names):
        """
        This function builds a dictionary of parameters that can be passed to the
        model building functions. It requires a numpy array with the same length
        as the number of free parameters, and a list of all of the parameter names
        in the order they appear in the array. The returned dictionary will contain
        all of these parameters, together with the fixed retrieval parameters.

        Args:
            sample : numpy.ndarray
                An array or list of free parameter values
            free_param_names : list(string)
                A list of names for each of the free parameters.
        Returns:
            params : dict
                A dictionary of Parameters, with values set to the values
                in sample.
        """
        params = {}
        i_p = 0
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                for i_s in range(len(free_param_names)):
                    if free_param_names[i_s] == self.parameters[pp].name:
                        params[self.parameters[pp].name] = \
                            Parameter(pp,False,value=sample[i_p])
                        i_p += 1
            else:
                params[pp] = Parameter(pp,False,value=self.parameters[pp].value)
        return params

    def sample_teff(self,sample_dict,param_dict,ret_names = None,nsample = None,resolution=40):
        r"""
        This function samples the outputs of a retrieval and computes Teff
        for each sample. For each sample, a model is computed at low resolution,
        and integrated to find the total radiant emittance, which is converted into
        a temperature using the stefan boltzmann law: $j^{\star} = \sigma T^{4}$.
        Teff itself is computed using util.calc_teff.

        Args:
            sample_dict : dict
                A dictionary, where each key is the name of a retrieval, and the values
                are the equal weighted samples.
            param_dict : dict
                A dictionary where each key is the name of a retrieval, and the values
                are the names of the free parameters associated with that retrieval.
            ret_names : Optional(list(string))
                A list of retrieval names, each should be included in the sample_dict.
                If left as none, it defaults to only using the current retrieval name.
            nsample : Optional(int)
                The number of times to compute Teff. If left empty, uses the "take_PTs_from"
                plot_kwarg. Recommended to use ~300 samples, probably more than is set in
                the kwarg!
            resolution : int
                The spectra resolution to compute the models at. Typically, this should be very
                low in order to enable rapid calculation.
        Returns:
            tdict : dict
                A dictionary with retrieval names for keys, and the values are the calculated
                values of Teff for each sample.
        """
        from .util import teff_calc
        if ret_names is None:
            ret_names = [self.retrieval_name]
        if nsample is None:
            nsample = self.rd.plot_kwargs["nsample"]

        # Setup the pRT object
        species = []
        for line in self.rd.line_species:
            if not os.path.isdir(self.path + "opacities/lines/corr_k/" +\
                                 line + "_R_" + \
                                 str(resolution)):
                species.append(line)
        # If not, setup low-res c-k tables
        if len(species)>0:
            exo_k_check = True
            print("Exo-k should only be run on a single thread.")
            print("The retrieval should be run once on a single core to build the c-k\ntables, and then again with multiple cores for the remainder of the retrieval.")
            # Automatically build the entire table
            bin_species_exok(species,resolution)
        species = []
        for spec in self.rd.line_species:
            species.append(spec + "_R_" + str(resolution))

        pRT_Object = Radtrans(line_species = cp.copy(self.rd.line_species), \
                            rayleigh_species= cp.copy(self.rd.rayleigh_species), \
                            continuum_opacities = cp.copy(self.rd.continuum_opacities), \
                            cloud_species = cp.copy(self.rd.cloud_species), \
                            mode='c-k', \
                            wlen_bords_micron = [0.5,28],
                            do_scat_emis = self.rd.scattering)
        if self.rd.AMR:
            p = self.rd._setup_pres()
        else:
            p = self.rd.p_global
        pRT_Object.setup_opa_structure(p)
        tdict = {}
        for name in ret_names:
            teffs = []
            samples = sample_dict[name]
            parameters_read = param_dict[name]
            rands = np.random.randint(0,samples.shape[0],nsample)
            duse = self.data[self.rd.plot_kwargs["take_PTs_from"]]
            for rint in rands:
                samp = samples[rint,:-1]
                params = self.build_param_dict(samp,parameters_read)
                wlen,model = duse.model_generating_function(pRT_Object,
                                                            params,
                                                            False,
                                                            self.rd.AMR)
                tfit = teff_calc(wlen,model,params["D_pl"],params["R_pl"])
                teffs.append(tfit)
            tdict[name] = np.array(teffs)
            np.save(self.output_dir + "evaluate_" + name + "/sampled_teff",np.array(teffs))
        return tdict


#############################################################
# Plotting functions
#############################################################
    def plot_all(self, output_dir = None, ret_names = [], contribution = False):
        """
        Produces plots for the best fit spectrum, a sample of 100 output spectra,
        the best fit PT profile and a corner plot for parameters specified in the
        run definition.
        """

        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        if output_dir is None:
            output_dir = self.output_dir
        sample_dict, parameter_dict = self.get_samples(output_dir,ret_names=ret_names)

        ###########################################
        # Plot best-fit spectrum
        ###########################################
        samples_use = cp.copy(sample_dict[self.retrieval_name])
        parameters_read = cp.copy(parameter_dict[self.retrieval_name])
        i_p = 0

        # This might actually be redundant...
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                for i_s in range(len(parameters_read)):
                    if parameters_read[i_s] == self.parameters[pp].name:
                        samples_use[:,i_p] = sample_dict[self.retrieval_name][:, i_s]
                i_p += 1

        print("Best fit parameters")
        i_p = 0
        # Get best-fit index
        logL ,best_fit_index = self.get_best_fit_likelihood(samples_use)


        # Print outputs
        # TODO add verbosity
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                for i_s in range(len(parameters_read)):
                    if parameters_read[i_s] == self.parameters[pp].name:
                        print(self.parameters[pp].name, samples_use[best_fit_index][i_p])
                        i_p += 1

        # Plotting
        self.plot_spectra(samples_use,parameters_read)
        if self.evaluate_sample_spectra:
            self.plot_sampled(samples_use, parameters_read)
        self.plot_PT(sample_dict,parameters_read, contribution = contribution)
        self.plot_corner(sample_dict,parameter_dict,parameters_read)
        if contribution:
            self.plot_contribution(samples_use,parameters_read)
        self.plot_abundances(samples_use,parameters_read, contribution = contribution)
        print("Done!")
        return

    def plot_spectra(self,samples_use,parameters_read,model_generating_func = None):
        """
        Plot the best fit spectrum, the data from each dataset and the residuals between the two.
        Saves a file to OUTPUT_DIR/evaluate_RETRIEVAL_NAME/best_fit_spec.pdf

        Args:
            samples_use : numpy.ndarray
                An array of the samples from the post_equal_weights file, used to find the best fit sample
            parameters_read : list
                A list of the free parameters as read from the output files.
            model_generating_fun : method
                A function that will take in the standard 'model' arguments
                (pRT_object, params, pt_plot_mode, AMR, resolution)
                and will return the wavlength and flux arrays as calculated by petitRadTrans.
                If no argument is given, it uses the method of the first dataset included in the retrieval.

        Returns:
            fig : matplotlib.figure
                The matplotlib figure, containing the data, best fit spectrum and residuals.
            ax : matplotlib.axes
                The upper pane of the plot, containing the best fit spectrum and data
            ax_r : matplotlib.axes
                The lower pane of the plot, containing the residuals between the fit and the data
        """
        check = self.evaluate_sample_spectra
        if self.evaluate_sample_spectra == True:
            self.evaluate_sample_spectra = False
        #TODO: include plotting of multiple retrievals
        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        print("\nPlotting Best-fit spectrum")
        fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col', sharey=False,
                               gridspec_kw={'height_ratios': [2.5, 1],'hspace':0.1},
                               figsize=(20, 10))
        ax = axes[0] # Normal Spectrum axis
        ax_r = axes[1] # residual axis

        # Get best-fit index
        logL, best_fit_index = self.get_best_fit_likelihood(samples_use)

        # Setup best fit spectrum
        # First get the fit for each dataset for the residual plots
        self.log_likelihood(samples_use[best_fit_index, :-1], 0, 0)
        # Then get the full wavelength range
        bf_wlen, bf_spectrum = self.get_best_fit_model(samples_use[best_fit_index, :-1],\
                                                       parameters_read)
        # Iterate through each dataset, plotting the data and the residuals.
        for name,dd in self.data.items():
            # If the user has specified a resolution, rebin to that
            if not dd.photometry:
                try:
                    # Sometimes this fails, I'm not super sure why.
                    resolution_data = np.mean(dd.wlen[1:]/np.diff(dd.wlen))
                    ratio = resolution_data / self.rd.plot_kwargs["resolution"]
                    if int(ratio) > 1:
                        flux,edges,_ = binned_statistic(dd.wlen,dd.flux,'mean',dd.wlen.shape[0]/ratio)
                        error,_,_ = binned_statistic(dd.wlen,dd.flux_error,\
                                                    'mean',dd.wlen.shape[0]/ratio)/np.sqrt(ratio)
                        wlen = np.array([(edges[i]+edges[i+1])/2.0 for i in range(edges.shape[0]-1)])

                    else:
                        wlen = dd.wlen
                        error = dd.flux_error
                        flux = dd.flux
                except:
                    wlen = dd.wlen
                    error = dd.flux_error
                    flux = dd.flux
                # Setup bins to rebin the best fit model to find the residuals
                wlen_bins = np.zeros_like(wlen)
                wlen_bins[:-1] = np.diff(wlen)
                wlen_bins[-1] = wlen_bins[-2]
            else:
                wlen = np.mean(dd.width_photometry)
                flux = dd.flux
                error = dd.flux_error
                wlen_bins = dd.wlen_bins

            # If the data has an arbitrary retrieved scaling factor
            scale = dd.scale_factor
            errscale = 1.0
            if dd.scale_err:
                errscale = dd.scale_factor
            if not dd.photometry:
                if dd.external_pRT_reference is None:
                    best_fit_binned = rgw(self.best_fit_specs[name][0], \
                                            self.best_fit_specs[name][1], \
                                            wlen, \
                                            wlen_bins)
                else:
                    best_fit_binned = rgw(self.best_fit_specs[dd.external_pRT_reference][0], \
                                self.best_fit_specs[dd.external_pRT_reference][1], \
                                wlen, \
                                wlen_bins)
            else:
                if dd.external_pRT_reference is None:
                    best_fit_binned = dd.photometric_transformation_function(self.best_fit_specs[name][0],
                                                                         self.best_fit_specs[name][1])
                    # Species functions give tuples of (flux,error)
                    try:
                        best_fit_binned = best_fit_binned[0]
                    except:
                        pass

                else:
                    best_fit_binned = \
                        dd.photometric_transformation_function(self.best_fit_specs[dd.external_pRT_reference][0],
                                                               self.best_fit_specs[dd.external_pRT_reference][1])
                    try:
                        best_fit_binned = best_fit_binned[0]
                    except:
                        pass
            # Plot the data
            marker = 'o'
            if dd.photometry:
                marker = 's'
            if not dd.photometry:
                label = dd.name
                ax.errorbar(wlen, \
                            flux * self.rd.plot_kwargs["y_axis_scaling"] * scale, \
                            yerr = error * self.rd.plot_kwargs["y_axis_scaling"] *errscale, \
                            marker=marker, markeredgecolor='k', linewidth = 0, elinewidth = 2, \
                            label = label, zorder =10, alpha = 0.9)
            else:
                # Don't label photometry?
                ax.errorbar(wlen, \
                            flux * self.rd.plot_kwargs["y_axis_scaling"] * scale, \
                            yerr = error * self.rd.plot_kwargs["y_axis_scaling"] *errscale, \
                            xerr = dd.wlen_bins/2., linewidth = 0, elinewidth = 2, \
                            marker=marker, markeredgecolor='k', color = 'grey', zorder = 10, \
                            label = None, alpha = 0.6)
            # Plot the residuals
            col = ax.get_lines()[-1].get_color()
            if dd.external_pRT_reference is None:

                ax_r.errorbar(wlen, \
                            ((flux*scale) - best_fit_binned )/(error*errscale) ,
                            yerr = error/error,
                            color = col,
                            linewidth = 0, elinewidth = 2, \
                            marker=marker, markeredgecolor='k', zorder = 10,
                            alpha = 0.9)
            else:
                ax_r.errorbar(wlen, \
                        ((flux*scale) - best_fit_binned )/(error*errscale),
                        yerr = error/error,
                        color = col,
                        linewidth = 0, elinewidth = 2, \
                        marker=marker, markeredgecolor='k', zorder = 10,
                        alpha = 0.9)
        # Plot the best fit model
        ax.plot(bf_wlen, \
                bf_spectrum * self.rd.plot_kwargs["y_axis_scaling"],
                label = f'Best Fit Model, $\chi^{2}=${self.get_reduced_chi2(samples_use):.2f}',
                linewidth=4,
                alpha = 0.5,
                color = 'r')
        # Plot the shading in the residual plot
        yabs_max = abs(max(ax_r.get_ylim(), key=abs))
        lims = ax.get_xlim()
        lim_y = ax.get_ylim()
        lim_y = [lim_y[0],lim_y[1]*1.12]
        ax.set_ylim(lim_y)

        # weird scaling to get axis to look ok on log plots
        if self.rd.plot_kwargs["xscale"] == 'log':
            lims = [lims[0]*1.09,lims[1]*1.02]
        else:
            lims = [bf_wlen[0]*0.98,bf_wlen[-1]*1.02]
        if self.rd.plot_kwargs.get('wavelength_lim') is not None:
            ax.set_xlim(self.rd.plot_kwargs.get('wavelength_lim'))
            ax_r.set_xlim(self.rd.plot_kwargs.get('wavelength_lim'))
        else:
            ax.set_xlim(lims)
            ax_r.set_xlim(lims)
        ax_r.set_ylim(ymin=-yabs_max, ymax=yabs_max)
        ax_r.fill_between(lims,-1,1,color='dimgrey',alpha=0.4,zorder = -10)
        ax_r.fill_between(lims,-3,3,color='darkgrey',alpha=0.3,zorder = -9)
        ax_r.fill_between(lims,-5,5,color='lightgrey',alpha=0.3,zorder = -8)
        ax_r.axhline(linestyle = '--', color = 'k',alpha=0.8, linewidth=2)

        # Making the plots pretty
        try:
            ax.set_xscale(self.rd.plot_kwargs["xscale"])
        except:
            pass
        try:
            ax.set_yscale(self.rd.plot_kwargs["yscale"])
        except:
            pass

        # Fancy ticks for upper pane
        ax.tick_params(axis="both",direction="in",length=10,bottom=True, top=True, left=True, right=True)
        try:
            ax.xaxis.set_major_formatter('{x:.1f}')
        except:
            logging.warning("Please update to matplotlib 3.3.4 or greater")
            pass

        if self.rd.plot_kwargs["xscale"] == 'log':
            # For the minor ticks, use no labels; default NullFormatter.
            x_major = LogLocator(base = 10.0, subs = (1,2,3,4), numticks = 4)
            ax.xaxis.set_major_locator(x_major)
            x_minor = LogLocator(base = 10.0, subs = np.arange(0.1,10.1,0.1)*0.1, numticks = 100)
            ax.xaxis.set_minor_locator(x_minor)
            ax.xaxis.set_minor_formatter(NullFormatter())
        else:
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.tick_params(axis='both', which='minor',
                           bottom=True, top=True, left=True, right=True,
                           direction='in',length=5)
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(axis='both', which='minor',
                       bottom=True, top=True, left=True, right=True,
                       direction='in',length=5)
        ax.set_ylabel(self.rd.plot_kwargs["spec_ylabel"])

        # Fancy ticks for lower pane
        ax_r.tick_params(axis="both",direction="in",length=10,bottom=True, top=True, left=True, right=True)

        try:
            ax_r.xaxis.set_major_formatter('{x:.1f}')
        except:
            logging.warning("Please update to matplotlib 3.3.4 or greater")
            pass

        if self.rd.plot_kwargs["xscale"] == 'log':
            # For the minor ticks, use no labels; default NullFormatter.
            x_major = LogLocator(base = 10.0, subs = (1,2,3,4), numticks = 4)
            ax_r.xaxis.set_major_locator(x_major)
            x_minor = LogLocator(base = 10.0, subs = np.arange(0.1,10.1,0.1)*0.1, numticks = 100)
            ax_r.xaxis.set_minor_locator(x_minor)
            ax_r.xaxis.set_minor_formatter(NullFormatter())
        else:
            ax_r.xaxis.set_minor_locator(AutoMinorLocator())
            ax_r.tick_params(axis='both', which='minor',
                             bottom=True, top=True, left=True, right=True,
                             direction='in',length=5)
        ax_r.yaxis.set_minor_locator(AutoMinorLocator())
        ax_r.tick_params(axis='both', which='minor',
                         bottom=True, top=True, left=True, right=True,
                         direction='in',length=5)
        ax_r.set_ylabel(r"Residuals [$\sigma$]")
        ax_r.set_xlabel(self.rd.plot_kwargs["spec_xlabel"])
        ax.legend(loc='upper center',ncol = len(self.data.keys())+1).set_zorder(1002)
        plt.tight_layout()
        plt.savefig(self.output_dir + 'evaluate_'+self.rd.retrieval_name +'/' +  self.retrieval_name  + '_best_fit_spec.pdf')
        self.evaluate_sample_spectra = check
        return fig, ax, ax_r

    def plot_sampled(self,samples_use,parameters_read, downsample_factor = None, save_outputs = False):
        """
        Plot a set of randomly sampled output spectra for each dataset in
        the retrieval.

        This will save nsample files for each dataset included in the retrieval.
        Note that if you change the model_resolution of your Data and rerun this
        function, the files will NOT be updated - if the files exists the function
        defaults to reading from file rather than recomputing. Delete all of the
        sample functions and run it again.

        Args:
            samples_use : np.ndarray
                posterior samples from pynmultinest outputs (post_equal_weights)
            downsample_factor : int
                Factor by which to reduce the resolution of the sampled model,
                for smoother plotting. Defaults to None. A value of None will result
                in the full resolution spectrum. Note that this factor can only
                reduce the resolution from the underlying model_resolution of the
                data.
        """
        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        self.rd.plot_kwargs["nsample"] = int(self.rd.plot_kwargs["nsample"])

        print("\nPlotting Best-fit spectrum with "+ str(self.rd.plot_kwargs["nsample"]) + " samples.")
        print("This could take some time...")
        len_samples = samples_use.shape[0]
        path = self.output_dir + 'evaluate_'+self.retrieval_name + "/"

        wmin = 99999.0
        wmax = 0.0
        for name,dd in self.data.items():
            if dd.wlen_range_pRT[0] < wmin:
                wmin = dd.wlen_range_pRT[0]
            if dd.wlen_range_pRT[1] > wmax:
                wmax = dd.wlen_range_pRT[1]
        # Set up parameter dictionary
        atmosphere = Radtrans(line_species = cp.copy(self.rd.line_species), \
                                rayleigh_species= cp.copy(self.rd.rayleigh_species), \
                                continuum_opacities = cp.copy(self.rd.continuum_opacities), \
                                cloud_species = cp.copy(self.rd.cloud_species), \
                                mode='c-k', \
                                wlen_bords_micron = [wmin*0.98,wmax*1.02],
                                do_scat_emis = self.rd.scattering)
        fig,ax = plt.subplots(figsize = (16,10))
        for i_sample in range(self.rd.plot_kwargs["nsample"]):
            random_index = int(np.random.uniform()*len_samples)
            if os.path.exists(path + "posterior_sampled_spectra_"+str(int(i_sample+1)).zfill(5)):
                wlen, model = np.load(path + "posterior_sampled_spectra_"+str(int(i_sample+1)).zfill(5)+".npy")
            else:
                parameters = self.build_param_dict(samples_use[random_index, :-1], parameters_read)
                parameters["contribution"] = Parameter("contribution", False, value = False)
                wlen, model = self.get_full_range_model(parameters, pRT_object = atmosphere)
            if downsample_factor != None:
                npoints = int(len(wlen))
                model = nc.running_mean(model,downsample_factor)[::downsample_factor]
                wlen = wlen[::downsample_factor]
            if save_outputs:
                np.save(path + "posterior_sampled_spectra_"+
                                str(int(i_sample+1)).zfill(5),
                                np.column_stack((wlen, model)))
            ax.plot(wlen,model, color = "#00d2f3", alpha = 1/self.rd.plot_kwargs["nsample"] + 0.1, linewidth = 0.2, marker = None)
        logL, best_fit_index = self.get_best_fit_likelihood(samples_use)

        # Setup best fit spectrum
        # First get the fit for each dataset for the residual plots
        #self.log_likelihood(samples_use[best_fit_index, :-1], 0, 0)
        # Then get the full wavelength range
        bf_wlen, bf_spectrum = self.get_best_fit_model(samples_use[best_fit_index, :-1],\
                                                       parameters_read)
        ax.plot(bf_wlen,
                bf_spectrum,
                marker = None,
                label = f"Best fit, $\chi^{2}=${self.get_reduced_chi2(samples_use):.2f}",
                linewidth=4,
                alpha = 0.5,
                color = 'r')

        for name,dd in self.data.items():
            fig, ax = plot_data(fig,ax,dd,
                                resolution = self.rd.plot_kwargs["resolution"],
                                scaling = self.rd.plot_kwargs["y_axis_scaling"])
        ax.set_xlabel('Wavelength [micron]')
        ax.set_ylabel(self.rd.plot_kwargs["spec_ylabel"])
        ax.legend(loc='best')
        plt.tight_layout()
        plt.savefig(path + self.retrieval_name  +'_sampled.pdf',bbox_inches = 0.)
        return fig, ax

    def plot_PT(self, sample_dict, parameters_read, contribution = False):
        """
        Plot the PT profile with error contours

        Args:
            samples_use : np.ndarray
                posterior samples from pynmultinest outputs (post_equal_weights)
            parameters_read : List
                Used to plot correct parameters, as some in self.parameters are not free, and
                aren't included in the PMN outputs
            weighted : bool
                Weight the opacity of the pt profile by the emission contribution function,
                and overplot the contribution curve.

        Returns:
            fig : matplotlib.figure
            ax : matplotlib.axes
        """

        print("\nPlotting PT profiles")
        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        self.PT_plot_mode = True
        samples_use = cp.copy(sample_dict[self.retrieval_name])
        i_p = 0
        for pp in self.parameters:
            if self.parameters[pp].is_free_parameter:
                for i_s in range(len(parameters_read)):
                    if parameters_read[i_s] == self.parameters[pp].name:
                        samples_use[:,i_p] = sample_dict[self.retrieval_name][:, i_s]
                i_p += 1

        temps = []
        for i_s in range(len(samples_use)):
            pressures, t = self.log_likelihood(samples_use[i_s, :-1], 0, 0)
            temps.append(t)

        logL, best_fit_index = self.get_best_fit_likelihood(samples_use)
        temps = np.array(temps)
        temps_sort = np.sort(temps, axis=0)
        fig,ax = plt.subplots(figsize=(16, 10))
        len_samp = len(samples_use)

        ax.fill_betweenx(pressures, \
                        x1 = temps_sort[0, :], \
                        x2 = temps_sort[-1, :], \
                        color = 'cyan', label = 'all',
                        zorder = 0)
        ax.fill_betweenx(pressures, \
                        x1 = temps_sort[int(len_samp*(0.5-0.997/2.)), :], \
                        x2 = temps_sort[int(len_samp*(0.5+0.997/2.)), :], \
                        color = 'brown', label = '3 sig',
                        zorder = 1)
        ax.fill_betweenx(pressures, \
                        x1 = temps_sort[int(len_samp*(0.5-0.95/2.)), :], \
                        x2 = temps_sort[int(len_samp*(0.5+0.95/2.)), :], \
                        color = 'orange', label = '2 sig',
                        zorder = 2)
        ax.fill_betweenx(pressures, \
                        x1 = temps_sort[int(len_samp*(0.5-0.68/2.)), :], \
                        x2 = temps_sort[int(len_samp*(0.5+0.68/2.)), :], \
                        color = 'red', label = '1 sig',
                        zorder = 3)

        if contribution:
            self.PT_plot_mode = False
            bf_wlen, bf_spectrum, bf_contribution = self.get_best_fit_model(samples_use[best_fit_index, :-1],\
                                                                        parameters_read,
                                                                        contribution = True)
            nu = nc.c/bf_wlen
            mean_diff_nu = -np.diff(nu)
            diff_nu = np.zeros_like(nu)
            diff_nu[:-1] = mean_diff_nu
            diff_nu[-1] = diff_nu[-2]
            spectral_weights = bf_spectrum*diff_nu/np.sum(bf_spectrum*diff_nu)

            if self.plotting:
                plt.clf()
                plt.plot(wlen/1e-4, spectral_weights)
                plt.show()
                print(np.shape(bf_contribution))

            pressure_weights = np.diff(np.log10(pressures))
            weights = np.ones_like(pressures)
            weights[:-1] = pressure_weights
            weights[-1] = weights[-2]
            weights = weights / np.sum(weights)
            weights = weights.reshape(len(weights), 1)

            contr_em = bf_contribution/weights

            # This probably doesn't need to be in a loop
            for i_str in range(bf_contribution.shape[0]):
                contr_em[i_str, :] = bf_contribution[i_str, :] * spectral_weights

            contr_em = np.sum(bf_contribution, axis = 1)
            contr_em = contr_em / np.sum(contr_em)

            if self.plotting:
                plt.clf()
                plt.yscale('log')
                plt.ylim([pressures[-1], pressures[0]])
                plt.plot(contr_em, pressures)
                plt.show()

            #####
            # Use contribution function to weigh alphas
            #####

            contr_em_weigh = contr_em/np.max(contr_em)
            from scipy.interpolate import interp1d
            contr_em_weigh_intp = interp1d(pressures, contr_em_weigh)

            yborders = pressures
            for i_p in range(len(yborders)-1):
                mean_press = (yborders[i_p+1]+yborders[i_p])/2.
                #print(1.-contr_em_weigh_intp(mean_press))
                ax.fill_between(self.rd.plot_kwargs["temp_limits"],
                                yborders[i_p+1],
                                yborders[i_p],
                                color = 'white',
                                alpha = min(1.-contr_em_weigh_intp(mean_press), 0.9),
                                linewidth=0,
                                rasterized = True,
                                zorder = 4)

            ax.plot(contr_em_weigh*(
                self.rd.plot_kwargs["temp_limits"][1]-self.rd.plot_kwargs["temp_limits"][0])\
                +self.rd.plot_kwargs["temp_limits"][0],
                pressures, '--',
                color = 'black',
                linewidth = 1.,
                label='Spectrally weighted contribution',
                zorder = 5)

        ax.set_yscale('log')
        try:
            ax.set_ylim(self.rd.plot_kwargs["press_limits"])
        except:
            ax.set_ylim([pressures[-1]*1.03, pressures[0]/1.03])
        try:
            ax.set_xlim(self.rd.plot_kwargs["temp_limits"])
        except:
            pass
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Pressure [bar]')
        ax.legend(loc='best')
        plt.tight_layout()
        plt.savefig(self.output_dir + 'evaluate_'+self.retrieval_name +'/' +  self.retrieval_name  + '_PT_envelopes.pdf')
        return fig, ax

    def plot_corner(self,sample_dict,parameter_dict,parameters_read, plot_best_fit = True, **kwargs):
        """
        Make the corner plots

        Args:
            samples_dict : Dict
                Dictionary of samples from PMN outputs, with keys being retrieval names
            paramete`   1   1`  Qar_dict : Dict
                Dictionary of parameters for each of the retrievals to be plotted.
            parameters_read : List
                Used to plot correct parameters, as some in self.parameters are not free, and
                aren't included in the PMN outputs
            kwargs : dict
                Each kwarg can be one of the kwargs used in corner.corner. These can be used to adjust
                the title_kwargs,label_kwargs,hist_kwargs, hist2d_kawargs or the contour kwargs. Each
                kwarg must be a dictionary with the arguments as keys and values as the values.
        """

        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        print("\nMaking corner plot")
        sample_use_dict = {}
        p_plot_inds = {}
        p_ranges = {}
        p_use_dict = {}
        bf_index = None
        if plot_best_fit:
            bf_index = {}

        for name,params in parameter_dict.items():
            samples_use = cp.copy(sample_dict[name])
            parameters_use = cp.copy(params)
            parameter_plot_indices = []
            parameter_ranges       = []
            i_p = 0
            for pp in parameters_read:
                if self.parameters[pp].plot_in_corner:
                    parameter_plot_indices.append(i_p)
                if self.parameters[pp].corner_label is not None:
                    parameters_use[i_p] = self.parameters[pp].corner_label
                if self.parameters[pp].corner_transform is not None:
                    samples_use[:, i_p] = \
                        self.parameters[pp].corner_transform(samples_use[:, i_p])
                parameter_ranges.append(self.parameters[pp].corner_ranges)

                i_p += 1
            p_plot_inds[name] = parameter_plot_indices
            p_ranges[name] = parameter_ranges
            p_use_dict[name] = parameters_use
            sample_use_dict[name] = samples_use


        output_file = self.output_dir + 'evaluate_'+self.retrieval_name +'/' +  self.retrieval_name  + '_corner_plot.pdf'

        # from Plotting
        fig = contour_corner(sample_use_dict,
                             p_use_dict,
                             output_file,
                             parameter_plot_indices = p_plot_inds,
                             parameter_ranges = p_ranges, \
                             true_values = None,
                             prt_plot_style=self.prt_plot_style,
                             plot_best_fit = plot_best_fit,
                             **kwargs)
        return fig

    def plot_data(self):
        fig, ax = plt.subplots()
        for name, dd in self.rd.data.items():
            if dd.photometry:
                wlen = np.mean(dd.width_photometry)
            else:
                wlen = dd.wlen
            ax.errorbar(wlen, dd.flux, yerr = dd.flux_error, label = name, marker = 'o')
        ax.legend()
        plt.savefig(self.output_dir +"evaluate_" + self.retrieval_name + "/" + self.retrieval_name + "_Data.pdf")

    def plot_contribution(self,samples_use,parameters_read,model_generating_func = None,log_scale_contribution = False, n_contour_levels = 30):
        """
        Plot the contribution function from the best fit spectrum, the data from each dataset and the residuals
        between the two. Saves a file to OUTPUT_DIR/evaluate_RETRIEVAL_NAME/best_fit_spec.pdf

        Args:
            samples_use : numpy.ndarray
                An array of the samples from the post_equal_weights file, used to find the best fit sample
            parameters_read : list
                A list of the free parameters as read from the output files.
            model_generating_fun : method
                A function that will take in the standard 'model' arguments
                (pRT_object, params, pt_plot_mode, AMR, resolution)
                and will return the wavlength and flux arrays as calculated by petitRadTrans.
                If no argument is given, it uses the method of the first dataset included in the retrieval.

        Returns:
            fig : matplotlib.figure
                The matplotlib figure, containing the data, best fit spectrum and residuals.
            ax : matplotlib.axes
                The upper pane of the plot, containing the best fit spectrum and data
            ax_r : matplotlib.axes
                The lower pane of the plot, containing the residuals between the fit and the data
        """

        self.evaluate_sample_spectra = False
        #TODO: include plotting of multiple retrievals
        if not self.run_mode == 'evaluate':
            logging.warning("Not in evaluate mode. Changing run mode to evaluate.")
            self.run_mode = 'evaluate'
        print("\nPlotting Best-fit contribution function")

        # Get best-fit index
        logL ,best_fit_index = self.get_best_fit_likelihood(samples_use)

        # Setup best fit spectrum
        # First get the fit for each dataset for the residual plots
        #self.log_likelihood(samples_use[best_fit_index, :-1], 0, 0)
        # Then get the full wavelength range
        bf_wlen, bf_spectrum, bf_contribution = self.get_best_fit_model(samples_use[best_fit_index, :-1],\
                                                                        parameters_read,
                                                                        contribution = True)

        index = (bf_contribution < 1e-16) & np.isnan(bf_contribution)
        bf_contribution[index] = 1e-16

        self.PT_plot_mode = True
        pressures, t = self.log_likelihood(samples_use[best_fit_index, :-1], 0, 0)
        self.PT_plot_mode = False


        pressure_weights = np.diff(np.log10(pressures))
        weights = np.ones_like(pressures)
        weights[:-1] = pressure_weights
        weights[-1] = weights[-2]
        weights = weights / np.sum(weights)
        weights = weights.reshape(len(weights), 1)

        X, Y = np.meshgrid(bf_wlen, pressures)
        fig, ax = plt.subplots()
        if log_scale_contribution:
            plot_cont = -np.log10(bf_contribution* self.rd.plot_kwargs["y_axis_scaling"]/weights)
            label = "-Log Weighted Flux"
        else:
            plot_cont = bf_contribution* self.rd.plot_kwargs["y_axis_scaling"]/weights
            label = "Weighted Flux"

        im = ax.contourf(X,
                         Y,
                         plot_cont,
                         n_contour_levels,
                         cmap=plt.cm.magma)
        ax.set_xlabel(self.rd.plot_kwargs["spec_xlabel"])
        ax.set_ylabel("Pressure [bar]")
        ax.set_xscale(self.rd.plot_kwargs["xscale"])
        ax.set_yscale("log")
        ax.set_ylim(pressures[-1]*1.03, pressures[0]/1.03)
        plt.colorbar(im, ax = ax, label = label)
        plt.tight_layout()
        plt.savefig(self.output_dir + 'evaluate_'+self.retrieval_name +'/' +  self.retrieval_name  + '_best_fit_contribution.pdf')
        return bf_contribution

    def plot_abundances(self,samples_use,parameters_read, species_to_plot = None, contribution = False):
        print("\nPlotting Abundances profiles")
        # Get best-fit index
        logL ,best_fit_index = self.get_best_fit_likelihood(samples_use)
        self.PT_plot_mode = True
        pressures, temps = self.log_likelihood(samples_use[best_fit_index , :-1], 0, 0)
        self.PT_plot_mode = False

        abundances, MMW = self.get_abundances(samples_use[best_fit_index , :-1], parameters_read)
        # Compute spectrum for each chem case
        fig,ax = plt.subplots(figsize = (12,7))
        if species_to_plot is None:
            species_to_plot = self.data[self.rd.plot_kwargs["take_PTs_from"]].pRT_object.line_species
        for spec in species_to_plot:
            ax.plot(abundances[spec],pressures,label=spec.split('_')[0])
        if contribution:
            bf_wlen, bf_spectrum, bf_contribution = self.get_best_fit_model(samples_use[best_fit_index, :-1],\
                                                                        parameters_read,
                                                                        contribution = True)
            nu = nc.c/bf_wlen
            mean_diff_nu = -np.diff(nu)
            diff_nu = np.zeros_like(nu)
            diff_nu[:-1] = mean_diff_nu
            diff_nu[-1] = diff_nu[-2]
            spectral_weights = bf_spectrum*diff_nu/np.sum(bf_spectrum*diff_nu)

            if self.plotting:
                plt.clf()
                plt.plot(wlen/1e-4, spectral_weights)
                plt.show()
                print(np.shape(bf_contribution))

            pressure_weights = np.diff(np.log10(pressures))
            weights = np.ones_like(pressures)
            weights[:-1] = pressure_weights
            weights[-1] = weights[-2]
            weights = weights / np.sum(weights)
            weights = weights.reshape(len(weights), 1)

            contr_em = bf_contribution/weights

            # This probably doesn't need to be in a loop
            for i_str in range(bf_contribution.shape[0]):
                contr_em[i_str, :] = bf_contribution[i_str, :] * spectral_weights

            contr_em = np.sum(bf_contribution, axis = 1)
            contr_em = contr_em / np.sum(contr_em)

            if self.plotting:
                plt.clf()
                plt.yscale('log')
                plt.ylim([pressures[-1], pressures[0]])
                plt.plot(contr_em, pressures)
                plt.show()

            #####
            # Use contribution function to weigh alphas
            #####

            contr_em_weigh = contr_em/np.max(contr_em)
            from scipy.interpolate import interp1d
            contr_em_weigh_intp = interp1d(pressures, contr_em_weigh)

            yborders = pressures
            for i_p in range(len(yborders)-1):
                mean_press = (yborders[i_p+1]+yborders[i_p])/2.
                #print(1.-contr_em_weigh_intp(mean_press))
                ax.fill_between([1e-7,3],
                                yborders[i_p+1],
                                yborders[i_p],
                                color = 'white',
                                alpha = min(1.-contr_em_weigh_intp(mean_press), 0.9),
                                linewidth=0,
                                rasterized = True,
                                zorder = 100)

            #plt.plot(temp, p, color = 'white', linewidth = 3.)
            #plt.plot(temp, p, '-', color = 'black', linewidth = 1.,label='Input')
            ax.plot(contr_em_weigh*(
                3 - 1e-7)\
                +1e-7,
                pressures, '--',
                color = 'black',
                linewidth = 1.,
                zorder = 120,
                label='Contribution')
        ax.set_xlabel("Mass Fraction Abundance")
        ax.set_ylabel("Pressure [bar]")
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.invert_yaxis()
        ax.set_xlim(1e-7,3)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize =14)
        plt.tight_layout()
        plt.savefig(self.output_dir + 'evaluate_'+self.retrieval_name +'/' +  self.retrieval_name  + '_best_fit_abundance_profiles.pdf')