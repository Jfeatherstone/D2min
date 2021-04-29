# D2Min

Calculate the d2min between an initial and final state of particles;
a measure of how non-affine the transformation is, as originally described
in Falk & Langer (1998).

Originally forked from:

[https://github.com/Binxu-Stack/D2min](https://github.com/Binxu-Stack/D2min)

Modifications include more documentation, change of notation,
and change from bond-focused calculation to center-focused
calculation (see code for more details).
Intended for use within other projects, so CLI access has been
removed.

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
    as the reference (and return types will have an extra first dimension N). Simiarly, can
    be a list of indices for which to calculate as the refernce indices.

interactionRadius : double (default=None)
    The maximum distance between particles that can be considered neighbors. Recommended to
    be set to around 1.1 - 1.5 times the mean particle radius of the system.

    If set to None, all other particles in the system will be considered neighbors. See interactionNeighbors
    for specifying a fixed number of neighbors. In the case that neither a radius or number of
    neighbors are specified, calculation will default to using all other particles as neighbors.

interactionNeighbors : int (default=None)
    As opposed to using an interactionRadius to define neighbors, a fixed number of neighbors can
    be specified here. This number of neighbors will be found using a kd-tree for the reference point(s).

    In the case that neither a radius or number of neighbors are specified, calculation will default
    to using all other particles as neighbors.

normalize : bool (default=True)
    Whether to divide the d2min by the number of neighbors used to calculate it (True) or not (False).
    For heterogeneous systems where the number of neighbors can vary significantly, recommend to set True.
    Will make little difference if a fixed number of neighbors (see interactionNeigbors) are used.

Returns
-------

(d2min, epsilon)

d2min : double
    The minimum value of D2 for the transition from the initial to final state. Units
    are a squared distance dimensionally the same as the initial and final centers (likely
    a pixel^2 value if tracked from images). Changing units to particle diameters afterwards
    may be necessary.

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

