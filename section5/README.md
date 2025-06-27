In this section we discuss the closure test results used to validate the model selection and uncertainty quantification.

## Choice of underlying law

The underlying law used in these closure test fits has been generated using this [notebook](../notebooks/underlying_law.ipynb).

## Validation of model selection strategy

To validate our model-selection strategy, we perform a scan over a family of models with
progressively increasing complexity, each fitted to the same instance of Level 1 data. By
comparing the Bayesian evidence for each model, we verify that the inference procedure
correctly identifies the model with the appropriate number of parameters, thus preventing
both underfitting and overfitting.

In this repository we provide both the [analytical](../runcards/template_analytical_L1.yaml) as well as the [numerical](../runcards/template_numerical_L1.yaml) template cards containing all of the fit-specs, data and actions used in this section. We also provide two python scripts, one for the [analytical](../runcards/run_parallel_analytic.py) and one for the [numerical](../runcards/run_parallel_num.py) that can be used for running a model scan.

> **Note:**  
> The fitting strategy adopted, as described in section 4 of the paper, is based on a Bayesian update strategy.
> Because of this we provide the two runcard templates separately.

To run the model scan, after having set-up your environment paths, you can simply run

```bash
python run_parallel_analytic.py
```

Once the analytical fit has finished, you can run the fully numerical one with

```bash
python run_parallel_num.py
```


For plotting purposes (eg Fig 7 of the paper) we provide the User with the following [notebook](../notebooks/l1_model_scan.ipynb).

<img src="../figures/figure7.png" width="300"/> 

## Uncertainty quantification in the data-region

To validate the reliability of PDF-predicted uncertainties in data space, we employ the
normalised bias estimator recently introduced in https://arxiv.org/pdf/2503.17447. 
This metric quantifies the actual mean square deviation of predictions from ground truth, expressed in units of the predicted
standard deviation. We conduct $N_{\rm fit} = 25$ closure tests, each utilizing a distinct, randomly
generated set of L1 data.

The analytical and numerical cards for this section can be taken from above. However, we provide a separate running script
for both the [analytical](../runcards/run_parallel_analytic_mct.py) and the [numerical](../runcards/run_parallel_num_mct.py) allowing the execution of multiple different L1 data fits in parallel.

Once the multi-closure fits have been run, it is possible to compute the normalised bias using the `validphys` executable which should be available in your environment. To do so, first complete the template yaml [runcard](../runcards/rb_runcard.yaml), and then simply execute


```bash
validphys rb_runcard.yaml
```


