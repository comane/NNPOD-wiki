In this section we discuss the choice of the basis and benchmark its completeness and generalisation properties.

## Samples from the NNPDF40 architecture.

Before applying POD to the PDF sample obtained from random realisations
of our NN, we must ensure that we have a sufficient number of samples to accurately estimate the density of the neural network PDF distribution.Figure 2 illustrates the convergence of the neural network distribution’s mean, variance, and correlation.

<img src="../figures/figure2.png" width="300"/> 

Specifically, it shows how the rolling averaged Euclidean distance between estimates based on `N` and `N + 1` samples varies with `N`.
This [notebook](../notebooks/sampled_mean_and_variance.ipynb) contains the material to reproduce these results.


## Assessing the completeness of basis and the flexibility of the model

We validate our methodology by performing two tests that assess whether the starting parametrisation
and its reduced POD representations are sufficiently flexible to capture the full range of
PDF behaviours that one might encounter in a realistic PDF fit.

We test two different aspects of our basis: its completeness and its generalisation capability. 

**Completeness** is defined as the ability of the POD parametrisation to reproduce any random realisation
of the original parametrisation that was used to produce the POD basis; this essentially
tests how closely the linear POD parametrisation approximates the original, generally non-linear, parametrisation. 

In Figure 3 and 4 of the paper we show the performance of the POD basis.
This [completeness notebook](../notebooks/completeness.ipynb) contains the material to reproduce these results.

<img src="../figures/figure3_l.png" width="300"/> 


**Generalisation** is defined as the ability of the basis to
reproduce a PDF representation that does not come from the original parametrisation, but
still satisfies all the theoretical constraints that a PDF replica should have. If the original
PDF space was sufficiently broad as to be able to describe many possible PDFs, then the
POD reduction should inherit this quality too.

This [generalisation notebook](../notebooks/generalisation.ipynb) contains the material to reproduce these results.

<img src="../figures/figure3_r.png" width="300"/> 

