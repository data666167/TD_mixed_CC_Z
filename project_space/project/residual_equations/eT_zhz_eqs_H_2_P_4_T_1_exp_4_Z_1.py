# system imports
from math import factorial

# third party imports
import numpy as np
import opt_einsum as oe

# local imports
from .symmetrize import symmetrize_tensor
from ..log_conf import log

# ------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- DEFAULT FUNCTIONS --------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------- INDIVIDUAL TERMS --------------------------------------------- #


# -------------- operator(name='', rank=0, m=0, n=0) TERMS -------------- #
def add_m0_n0_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args):
    """ Calculate the operator(name='', rank=0, m=0, n=0) HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    if ansatz.ground_state:
        R += np.einsum('ac, c -> a', h_args[(0, 0)], z_args[(0, 0)])

        if truncation.h_at_least_linear:
            if truncation.z_at_least_linear:
                R += np.einsum('aci, ci -> a', h_args[(0, 1)], z_args[(1, 0)])

    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


def add_m0_n0_eT_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args):
    """ Calculate the operator(name='', rank=0, m=0, n=0) eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    if ansatz.ground_state:
        if truncation.t_singles:
            if truncation.z_at_least_linear:
                R += np.einsum('i, ac, ci -> a', t_args[(0, 1)], h_args[(0, 0)], z_args[(1, 0)])

        if truncation.h_at_least_linear:
            if truncation.t_singles:
                R += np.einsum('i, aci, c -> a', t_args[(0, 1)], h_args[(1, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += (
                        np.einsum('i, acij, cj -> a', t_args[(0, 1)], h_args[(1, 1)], z_args[(1, 0)]) +
                        np.einsum('i, j, acj, ci -> a', t_args[(0, 1)], t_args[(0, 1)], h_args[(1, 0)], z_args[(1, 0)])
                    )

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                R += (1 / 2) * np.einsum('i, j, acij, c -> a', t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += (1 / 2) * np.einsum('i, j, k, acjk, ci -> a', t_args[(0, 1)], t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return

# --------------------------------------------------------------------------- #
# ---------------------------- RANK  1 FUNCTIONS ---------------------------- #
# --------------------------------------------------------------------------- #


# -------------- operator(name='b', rank=1, m=0, n=1) TERMS -------------- #
def add_m0_n1_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args):
    """ Calculate the operator(name='b', rank=1, m=0, n=1) HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    if ansatz.ground_state:
        if truncation.z_at_least_linear:
            R += np.einsum('ac, cz -> az', h_args[(0, 0)], z_args[(1, 0)])

        if truncation.h_at_least_linear:
            R += np.einsum('acz, c -> az', h_args[(1, 0)], z_args[(0, 0)])
            if truncation.z_at_least_linear:
                R += np.einsum('aciz, ci -> az', h_args[(1, 1)], z_args[(1, 0)])

    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


def add_m0_n1_eT_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args):
    """ Calculate the operator(name='b', rank=1, m=0, n=1) eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    if ansatz.ground_state:
        if truncation.h_at_least_linear:
            if truncation.t_singles:
                if truncation.z_at_least_linear:
                    R += (
                        np.einsum('i, acz, ci -> az', t_args[(0, 1)], h_args[(1, 0)], z_args[(1, 0)]) +
                        np.einsum('i, aci, cz -> az', t_args[(0, 1)], h_args[(1, 0)], z_args[(1, 0)])
                    )

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                R += np.einsum('i, aciz, c -> az', t_args[(0, 1)], h_args[(2, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += np.einsum('i, j, acjz, ci -> az', t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
                    R += (1 / 2) * np.einsum('i, j, acij, cz -> az', t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


# --------------------------------------------- RESIDUAL FUNCTIONS --------------------------------------------- #
def compute_m0_n0_amplitude(A, N, ansatz, truncation, t_args, h_args, z_args):
    """Compute the operator(name='', rank=0, m=0, n=0) amplitude."""
    truncation.confirm_at_least_singles()

    # the residual tensor
    R = np.zeros(shape=(A,), dtype=complex)

    # add the terms
    add_m0_n0_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args)
    add_m0_n0_eT_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args)
    return R


def compute_m0_n1_amplitude(A, N, ansatz, truncation, t_args, h_args, z_args):
    """Compute the operator(name='b', rank=1, m=0, n=1) amplitude."""
    truncation.confirm_at_least_singles()

    # the residual tensor
    R = np.zeros(shape=(A, N), dtype=complex)

    # add the terms
    add_m0_n1_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args)
    add_m0_n1_eT_HZ_terms(R, ansatz, truncation, t_args, h_args, z_args)
    return R


# ------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- OPTIMIZED FUNCTIONS -------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------- INDIVIDUAL TERMS --------------------------------------------- #


# -------------- operator(name='', rank=0, m=0, n=0) TERMS -------------- #
def add_m0_n0_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, opt_HZ_path_list):
    """ Optimized calculation of the operator(name='', rank=0, m=0, n=0) HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    # make an iterable out of the `opt_HZ_path_list`
    optimized_einsum = iter(opt_HZ_path_list)

    if ansatz.ground_state:
        R += next(optimized_einsum)(h_args[(0, 0)], z_args[(0, 0)])

        if truncation.h_at_least_linear:
            if truncation.z_at_least_linear:
                R += next(optimized_einsum)(h_args[(0, 1)], z_args[(1, 0)])
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


def add_m0_n0_eT_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, opt_eT_HZ_path_list):
    """ Optimized calculation of the operator(name='', rank=0, m=0, n=0) eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    # make an iterable out of the `opt_eT_HZ_path_list`
    optimized_einsum = iter(opt_eT_HZ_path_list)

    if ansatz.ground_state:
        if truncation.t_singles:
            if truncation.z_at_least_linear:
                R += next(optimized_einsum)(t_args[(0, 1)], h_args[(0, 0)], z_args[(1, 0)])

        if truncation.h_at_least_linear:
            if truncation.t_singles:
                R += next(optimized_einsum)(t_args[(0, 1)], h_args[(1, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += (
                        next(optimized_einsum)(t_args[(0, 1)], h_args[(1, 1)], z_args[(1, 0)]) +
                        next(optimized_einsum)(t_args[(0, 1)], t_args[(0, 1)], h_args[(1, 0)], z_args[(1, 0)])
                    )

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                R += (1 / 2) * next(optimized_einsum)(t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += (1 / 2) * next(optimized_einsum)(t_args[(0, 1)], t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return

# --------------------------------------------------------------------------- #
# ---------------------------- RANK  1 FUNCTIONS ---------------------------- #
# --------------------------------------------------------------------------- #


# -------------- operator(name='b', rank=1, m=0, n=1) TERMS -------------- #
def add_m0_n1_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, opt_HZ_path_list):
    """ Optimized calculation of the operator(name='b', rank=1, m=0, n=1) HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    # make an iterable out of the `opt_HZ_path_list`
    optimized_einsum = iter(opt_HZ_path_list)

    if ansatz.ground_state:
        if truncation.z_at_least_linear:
            R += next(optimized_einsum)(h_args[(0, 0)], z_args[(1, 0)])

        if truncation.h_at_least_linear:
            R += next(optimized_einsum)(h_args[(1, 0)], z_args[(0, 0)])
            if truncation.z_at_least_linear:
                R += next(optimized_einsum)(h_args[(1, 1)], z_args[(1, 0)])

    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


def add_m0_n1_eT_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, opt_eT_HZ_path_list):
    """ Optimized calculation of the operator(name='b', rank=1, m=0, n=1) eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    # make an iterable out of the `opt_eT_HZ_path_list`
    optimized_einsum = iter(opt_eT_HZ_path_list)

    if ansatz.ground_state:

        if truncation.h_at_least_linear:
            if truncation.t_singles:
                if truncation.z_at_least_linear:
                    R += next(optimized_einsum)(t_args[(0, 1)], h_args[(1, 0)], z_args[(1, 0)])

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                R += next(optimized_einsum)(t_args[(0, 1)], h_args[(2, 0)], z_args[(0, 0)])
                if truncation.z_at_least_linear:
                    R += next(optimized_einsum)(t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
                    R += (1 / 2) * next(optimized_einsum)(t_args[(0, 1)], t_args[(0, 1)], h_args[(2, 0)], z_args[(1, 0)])
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return


# --------------------------------------------- RESIDUAL FUNCTIONS --------------------------------------------- #
def compute_m0_n0_amplitude_optimized(A, N, ansatz, truncation, t_args, h_args, z_args, opt_paths):
    """Compute the operator(name='', rank=0, m=0, n=0) amplitude."""
    truncation.confirm_at_least_singles()

    # the residual tensor
    R = np.zeros(shape=(A,), dtype=complex)

    # unpack the optimized paths
    optimized_HZ_paths, optimized_eT_HZ_paths = opt_paths

    # add the terms
    add_m0_n0_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, optimized_HZ_paths)
    add_m0_n0_eT_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, optimized_eT_HZ_paths)
    return R


def compute_m0_n1_amplitude_optimized(A, N, ansatz, truncation, t_args, h_args, z_args, opt_paths):
    """Compute the operator(name='b', rank=1, m=0, n=1) amplitude."""
    truncation.confirm_at_least_singles()

    # the residual tensor
    R = np.zeros(shape=(A, N), dtype=complex)

    # unpack the optimized paths
    optimized_HZ_paths, optimized_eT_HZ_paths = opt_paths

    # add the terms
    add_m0_n1_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, optimized_HZ_paths)
    add_m0_n1_eT_HZ_terms_optimized(R, ansatz, truncation, t_args, h_args, z_args, optimized_eT_HZ_paths)
    return R

# ------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- OPTIMIZED PATHS FUNCTIONS ----------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------- INDIVIDUAL OPTIMIZED PATHS ----------------------------------------- #


# -------------- operator(name='', rank=0, m=0, n=0) OPTIMIZED PATHS -------------- #
def compute_m0_n0_HZ_RHS_optimized_paths(A, N, ansatz, truncation):
    """Calculate optimized einsum paths for the operator(name='', rank=0, m=0, n=0) RHS HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    HZ_opt_path_list = []

    if ansatz.ground_state:
        HZ_opt_path_list.append(oe.contract_expression('ac, c -> a', (A, A), (A,), optimize='auto-hq'))

        if truncation.h_at_least_linear:
            if truncation.z_at_least_linear:
                HZ_opt_path_list.append(oe.contract_expression('aci, ci -> a', (A, A, N), (A, N), optimize='auto-hq'))

    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return HZ_opt_path_list


def compute_m0_n0_eT_HZ_RHS_optimized_paths(A, N, ansatz, truncation):
    """Calculate optimized einsum paths for the operator(name='', rank=0, m=0, n=0) RHS eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    eT_HZ_opt_path_list = []

    if ansatz.ground_state:
        if truncation.t_singles:
            if truncation.z_at_least_linear:
                eT_HZ_opt_path_list.append(oe.contract_expression('i, ac, ci -> a', (N,), (A, A), (A, N), optimize='auto-hq'))

        if truncation.h_at_least_linear:
            if truncation.t_singles:
                eT_HZ_opt_path_list.append(oe.contract_expression('i, aci, c -> a', (N,), (A, A, N), (A,), optimize='auto-hq'))
                if truncation.z_at_least_linear:
                    eT_HZ_opt_path_list.extend([
                        oe.contract_expression('i, acij, cj -> a', (N,), (A, A, N, N), (A, N), optimize='auto-hq'),
                        oe.contract_expression('i, j, acj, ci -> a', (N,), (N,), (A, A, N), (A, N), optimize='auto-hq')
                    ])

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                eT_HZ_opt_path_list.append(oe.contract_expression('i, j, acij, c -> a', (N,), (N,), (A, A, N, N), (A,), optimize='auto-hq'))
                if truncation.z_at_least_linear:
                    eT_HZ_opt_path_list.append(oe.contract_expression('i, j, k, acjk, ci -> a', (N,), (N,), (N,), (A, A, N, N), (A, N), optimize='auto-hq'))
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return eT_HZ_opt_path_list

# --------------------------------------------------------------------------- #
# ---------------------------- RANK  1 OPTIMIZED PATHS ---------------------------- #
# --------------------------------------------------------------------------- #


# -------------- operator(name='b', rank=1, m=0, n=1) OPTIMIZED PATHS -------------- #
def compute_m0_n1_HZ_RHS_optimized_paths(A, N, ansatz, truncation):
    """Calculate optimized einsum paths for the operator(name='b', rank=1, m=0, n=1) RHS HZ terms.
    These terms have no vibrational contribution from the e^T operator.
    This reduces the number of possible non-zero permutations of creation/annihilation operators.
    """

    HZ_opt_path_list = []

    if ansatz.ground_state:
        if truncation.z_at_least_linear:
            HZ_opt_path_list.append(oe.contract_expression('ac, cz -> az', (A, A), (A, N), optimize='auto-hq'))

        if truncation.h_at_least_linear:
            HZ_opt_path_list.append(oe.contract_expression('acz, c -> az', (A, A, N), (A,), optimize='auto-hq'))
            if truncation.z_at_least_linear:
                HZ_opt_path_list.append(oe.contract_expression('aciz, ci -> az', (A, A, N, N), (A, N), optimize='auto-hq'))

    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return HZ_opt_path_list


def compute_m0_n1_eT_HZ_RHS_optimized_paths(A, N, ansatz, truncation):
    """Calculate optimized einsum paths for the operator(name='b', rank=1, m=0, n=1) RHS eT_HZ terms.
    These terms include the vibrational contributions from the e^T operator.
    This increases the number of possible non-zero permutations of creation/annihilation operators.
    """

    eT_HZ_opt_path_list = []

    if ansatz.ground_state:
        if truncation.h_at_least_linear:
            if truncation.t_singles:
                if truncation.z_at_least_linear:
                    eT_HZ_opt_path_list.extend([
                        oe.contract_expression('i, acz, ci -> az', (N,), (A, A, N), (A, N), optimize='auto-hq'),
                        oe.contract_expression('i, aci, cz -> az', (N,), (A, A, N), (A, N), optimize='auto-hq')
                    ])

        if truncation.h_at_least_quadratic:
            if truncation.t_singles:
                eT_HZ_opt_path_list.append(oe.contract_expression('i, aciz, c -> az', (N,), (A, A, N, N), (A,), optimize='auto-hq'))
                if truncation.z_at_least_linear:
                    eT_HZ_opt_path_list.append(oe.contract_expression('i, j, acjz, ci -> az', (N,), (N,), (A, A, N, N), (A, N), optimize='auto-hq'))
                    eT_HZ_opt_path_list.append(oe.contract_expression('i, j, acij, cz -> az', (N,), (N,), (A, A, N, N), (A, N), optimize='auto-hq'))
    else:
        raise Exception('Hot Band amplitudes not implemented properly and have not been theoretically verified!')

    return eT_HZ_opt_path_list


# ----------------------------------------- GROUPED BY PROJECTION OPERATOR ----------------------------------------- #
def compute_m0_n0_optimized_paths(A, N, ansatz, truncation):
    """Compute the optimized paths for this operator(name='', rank=0, m=0, n=0)."""
    truncation.confirm_at_least_singles()

    HZ_opt_path_list = compute_m0_n0_HZ_RHS_optimized_paths(A, N, ansatz, truncation)
    eT_HZ_opt_path_list = compute_m0_n0_eT_HZ_RHS_optimized_paths(A, N, ansatz, truncation)

    return_dict = {
        (0, 0): [HZ_opt_path_list, eT_HZ_opt_path_list]
    }

    return return_dict


def compute_m0_n1_optimized_paths(A, N, ansatz, truncation):
    """Compute the optimized paths for this operator(name='b', rank=1, m=0, n=1)."""
    truncation.confirm_at_least_singles()

    HZ_opt_path_list = compute_m0_n1_HZ_RHS_optimized_paths(A, N, ansatz, truncation)
    eT_HZ_opt_path_list = compute_m0_n1_eT_HZ_RHS_optimized_paths(A, N, ansatz, truncation)

    return_dict = {
        (0, 1): [HZ_opt_path_list, eT_HZ_opt_path_list]
    }

    return return_dict


# ----------------------------------------- MASTER OPTIMIZED PATH FUNCTION ----------------------------------------- #
def compute_all_optimized_paths(A, N, ansatz, truncation):
    """Return dictionary containing optimized contraction paths.
    Calculates all optimized paths for the `opt_einsum` calls up to
        a maximum order of m+n=1 for a projection operator P^m_n
    """
    all_opt_path_lists = {}

    all_opt_path_lists[(0, 0)] = compute_m0_n0_optimized_paths(A, N, ansatz, truncation)[(0, 0)]
    all_opt_path_lists[(0, 1)] = compute_m0_n1_optimized_paths(A, N, ansatz, truncation)[(0, 1)]

    return all_opt_path_lists
