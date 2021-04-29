#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A script to solve D2min field between two different particle states.

Originally forked from:
https://github.com/Binxu-Stack/D2min
created by Bin Xu (xubinrun@gmail.com)

Modifications include more documentation, change of notation,
and change from bond-focused calculation to center-focused
calculation (see code for more details).

Intended for use within other projects, so CLI access has been
removed.

~ Jack Featherstone (jdfeathe@ncsu.edu)
"""

import numpy as np
from numpy.linalg import inv

def calculateD2Min(initialCenters, finalCenters, refParticleIndex=0):
    """
    Calculate the d2min between an initial and final state of particles;
    a measure of how non-affine the transformation is, as originally described
    in Falk & Langer (1998).


    Parameters
    ----------

    initialCenters :  [N, d] numpy.ndarray or list
        List of initial center points of N particles in d dimensions.

    finalCenters :  [N, d] numpy.ndarray or list
        List of final center points of N particles in d dimensions. Must be
        in the same order as initialCenters.

    refParticleIndex : int (default=0)
        The index of the particle to treat as the reference particle (r_0 in Falk & Langer
        1998 eq. 2.11). If set to None, will calculate the D2min N times using each particle
        as the reference (and return types will have an extra first dimension N).


    Returns
    -------

    (d2min, epsilon)

    d2min : double
        The minimum value of D2 for the transition from the initial to final state.

    epsilon : [d, d] numpy.ndarray
        The uniform strain tensor that minimizes D2; equation 2.14 in Falk & Langer (1998).

    In the case that refParticleIndex=None, the return will instead be a tuple of numpy arrays
    containing the same information but for every particle:

    (d2minArr, epsilonArr)

    d2minArr : [N] numpy.ndarray
        The minimum value of D2 for the transition from the initial to final state for
        every possible configuration.

    epsilonArr : [N, d, d] numpy.ndarray
        The uniform strain tensor that minimizes D2 for every possible configuration


    Examples
    --------

    See `test` folder in repository.

        
    References
    ----------    

    Falk, M. L., & Langer, J. S. (1998). Dynamics of viscoplastic deformation in amorphous solids. Physical Review E, 57(6), 7192–7205.
    [https://doi.org/10.1103/PhysRevE.57.7192](https://doi.org/10.1103/PhysRevE.57.7192)

    """

    # The number of particles and spatial dimension
    N, d = np.shape(initialCenters)

    # In the case that a single reference particle is defined, we just calculate exactly as described in the paper
    if not isinstance(refParticleIndex, list) and not isinstance(refParticleIndex, np.ndarray) and refParticleIndex != None:

        # Bin's original code defined the differences between centers in
        # Falk & Langer eq. 2.11 - 2.13 as "bonds"

        # We first calculate these bonds using our reference particle index
        # Do this by subtracting the ref particle center from the center of every other particle
        # Note that you could technically leave in the ref bond, since it will be 0 and not contribute,
        # but it is cleaner to just remove it
        initialBonds = initialCenters[np.arange(N) != refParticleIndex] - initialCenters[refParticleIndex]
        finalBonds = finalCenters[np.arange(N) != refParticleIndex] - finalCenters[refParticleIndex]

        # More succinct notation for doing the calculation, from Bin's original code
        # Converting to numpy matrices makes matrix multiplication happen automatically
        b0 = np.mat(initialBonds)
        b = np.mat(finalBonds)

        # Calculate the two functions used to minimize D2, X and Y (eq. 2.12 and 2.13 respectively)
        X = b.transpose() * b0
        Y = b0.transpose() * b0

        # Calculate the uniform strain tensor that minimizes D2 (eq. 2.14)
        # Note that we don't include the kronecker delta function since it will
        # be cancelled out when plugged into the D2min equation (eq. 2.11).
        # Also not that this is actually the transpose of the strain tensor as
        # it is defined in the paper, since it makes the matrix multiplication easier
        # in the next step
        epsilon = inv(Y) * X

        # Non-affine part, or the terms that are squared and summed over in eq. 2.11
        non_affine = b - b0*epsilon

        # The final value
        d2min = np.sum(np.square(non_affine))

        return (d2min, np.array(epsilon))

    # If we don't have a reference particle, or we are given multiple, we calculate for each of those
    if not isinstance(refParticleIndex, list) and not isinstance(refParticleIndex, np.ndarray):
        refParticleIndex = np.arange(N)

    # Now calculate for all of those possibilities
    d2minArr = np.zeros(len(refParticleIndex))
    epsilonArr = np.zeros([len(refParticleIndex), d, d])
    
    for i in range(len(refParticleIndex)):

        d2min, epsilon = calculateD2Min(initialCenters, finalCenters, refParticleIndex[i])
        d2minArr[i] = d2min
        epsilonArr[i] = epsilon

    return (d2minArr, epsilonArr)

        
def vonMisesStrain(uniformStrainTensor):

    # The number of spatial dimensions
    dimension = np.shape(uniformStrainTensor)[0]

    # Lagrangian strain matrix
    eta = 0.5 * (uniformStrainTensor * uniformStrainTensor.transpose() - np.eye(dimension))

    # von-Mises strain
    eta_m = 1.0/np.double(dimension) * np.trace(eta)
    tmp = eta - eta_m * np.eye(dimension)
    eta_s = np.sqrt(0.5*np.trace(tmp*tmp))

    return eta_s
