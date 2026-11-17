# Statistical results

Generated from this run's artifacts; no copied paper values.

Primary H1 comparisons use held-out image pools. H2 resource inference uses languages
as its sampling unit. Nominal pooled H2 p-values are descriptive only.

## H1/clip/tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.01748455171621665,
    "C(tier, Treatment('stable'))[T.fast]": 0.003085473481645665,
    "C(tier, Treatment('stable'))[T.slow]": 0.0031140741544529228,
    "log_resource_centered": -0.0005345505100944654,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00048319612402621635,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0002506651138034662
  },
  "pvalues": {
    "Intercept": 0.0,
    "C(tier, Treatment('stable'))[T.fast]": 1.1924980095112536e-05,
    "C(tier, Treatment('stable'))[T.slow]": 2.457428528936429e-07,
    "log_resource_centered": 1.56800780623901e-11,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0001004158810997358,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.018460053287849817,
    "Group Var": 0.0005152962315556911
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.016603068806301472,
      "C(tier, Treatment('stable'))[T.fast]": 0.0017044551731382872,
      "C(tier, Treatment('stable'))[T.slow]": 0.0019314407299081244,
      "log_resource_centered": -0.0006899618663278861,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00023971332260812802,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 4.215889959544757e-05,
      "Group Var": 0.3046215242009298
    },
    "1": {
      "Intercept": 0.018366034626131827,
      "C(tier, Treatment('stable'))[T.fast]": 0.004466491790153042,
      "C(tier, Treatment('stable'))[T.slow]": 0.004296707578997722,
      "log_resource_centered": -0.0003791391538610448,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0007266789254443047,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0004591713280114848,
      "Group Var": 1.0939945807426468
    }
  },
  "random_intercept_variance": 2.613454295388322e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1280.4537  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.017    0.000 38.877 0.000  0.017  0.018\nC(tier, Treatment('stable'))[T.fast]                        0.003    0.001  4.379 0.000  0.002  0.004\nC(tier, Treatment('stable'))[T.slow]                        0.003    0.001  5.161 0.000  0.002  0.004\nlog_resource_centered                                      -0.001    0.000 -6.741 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  3.890 0.000  0.000  0.001\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  2.356 0.018  0.000  0.000\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H1/clip/tier/kruskal

```json
{
  "statistic": 7.396300773694378,
  "pvalue": 0.02476929774661122
}
```

## H1/clip/tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.0014633786570174712,
    "permutation_p": 0.0988901109889011,
    "cohen_d_independent": 0.5278774976821757,
    "mann_whitney_p": 0.025636853074524065,
    "n_a": 11,
    "n_b": 16,
    "holm_p": 0.1977802219778022
  },
  "fast_vs_slow": {
    "difference": -0.001292382237291112,
    "permutation_p": 0.7948205179482052,
    "cohen_d_independent": -0.3336884704605116,
    "mann_whitney_p": 0.6825318916290903,
    "n_a": 11,
    "n_b": 20,
    "holm_p": 0.7948205179482052
  }
}
```

## H1/clip/dd_tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(dd_tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.018034855542868763,
    "C(dd_tier, Treatment('stable'))[T.fast]": 0.003273581543069297,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.001328355524279518,
    "log_resource_centered": -0.00047116936766768575,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0004132407697345129,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 7.193340001758548e-05
  },
  "pvalues": {
    "Intercept": 0.0,
    "C(dd_tier, Treatment('stable'))[T.fast]": 1.8400695408523455e-06,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.0491063808742489,
    "log_resource_centered": 2.947532756407564e-09,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00029397709417886355,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.5217487637587153,
    "Group Var": 0.00036559337382652697
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.017099243404866547,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.0019285543498847274,
      "C(dd_tier, Treatment('stable'))[T.slow]": 5.200149595896344e-06,
      "log_resource_centered": -0.0006267807821522153,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00018953526662023867,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": -0.00014813437280649739,
      "Group Var": 0.36291155841273104
    },
    "1": {
      "Intercept": 0.01897046768087098,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.004618608736253867,
      "C(dd_tier, Treatment('stable'))[T.slow]": 0.0026515108989631398,
      "log_resource_centered": -0.0003155579531831562,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0006369462728487871,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00029200117284166834,
      "Group Var": 1.2499293079016494
    }
  },
  "random_intercept_variance": 3.02151882036803e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                 Mixed Linear Model Regression Results\n========================================================================================================\nModel:                             MixedLM                Dependent Variable:                ret_swd_k10\nNo. Observations:                  282                    Method:                            REML       \nNo. Groups:                        47                     Scale:                             0.0000     \nMin. group size:                   6                      Log-Likelihood:                    1277.4461  \nMax. group size:                   6                      Converged:                         Yes        \nMean group size:                   6.0                                                                  \n--------------------------------------------------------------------------------------------------------\n                                                              Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n--------------------------------------------------------------------------------------------------------\nIntercept                                                      0.018    0.000 37.780 0.000  0.017  0.019\nC(dd_tier, Treatment('stable'))[T.fast]                        0.003    0.001  4.770 0.000  0.002  0.005\nC(dd_tier, Treatment('stable'))[T.slow]                        0.001    0.001  1.968 0.049  0.000  0.003\nlog_resource_centered                                         -0.000    0.000 -5.934 0.000 -0.001 -0.000\nC(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  3.621 0.000  0.000  0.001\nC(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  0.641 0.522 -0.000  0.000\nGroup Var                                                      0.000    0.000                           \n========================================================================================================\n"
}
```

## H1/clip/dd_tier/kruskal

```json
{
  "statistic": 35.398825354609954,
  "pvalue": 2.057040021333127e-08
}
```

## H1/clip/dd_tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.00691301822256935,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 2.381324775859053,
    "mann_whitney_p": 1.1582319258192444e-06,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  },
  "fast_vs_slow": {
    "difference": 0.004390038486365638,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 1.4812800566409392,
    "mann_whitney_p": 9.36934469056872e-05,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  }
}
```

## H1/clip/style_control

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered + style_swd",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.017107177399702855,
    "C(tier, Treatment('stable'))[T.fast]": 0.002969353021081022,
    "C(tier, Treatment('stable'))[T.slow]": 0.0031062504753899107,
    "log_resource_centered": -0.0005345505100944652,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00048319612402621624,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0002506651138034661,
    "style_swd": 0.006018501606361109
  },
  "pvalues": {
    "Intercept": 4.403781316501968e-133,
    "C(tier, Treatment('stable'))[T.fast]": 4.4332686989246443e-05,
    "C(tier, Treatment('stable'))[T.slow]": 3.085073199770308e-07,
    "log_resource_centered": 1.5680072793117597e-11,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00010041586944599375,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.018460052439869652,
    "style_swd": 0.47655615201273827,
    "Group Var": 0.0005638924128633756
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.0157413747837939,
      "C(tier, Treatment('stable'))[T.fast]": 0.0015442022983511278,
      "C(tier, Treatment('stable'))[T.slow]": 0.0019167366721493646,
      "log_resource_centered": -0.000689961865202511,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00023971332437125153,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 4.215890110529635e-05,
      "style_swd": -0.010552413411416668,
      "Group Var": 0.3060822666014757
    },
    "1": {
      "Intercept": 0.01847298001561181,
      "C(tier, Treatment('stable'))[T.fast]": 0.004394503743810917,
      "C(tier, Treatment('stable'))[T.slow]": 0.004295764278630457,
      "log_resource_centered": -0.00037913915498641944,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0007266789236811809,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0004591713265016359,
      "style_swd": 0.022589416624138887,
      "Group Var": 1.1121703044919888
    }
  },
  "random_intercept_variance": 2.6501469610484887e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1276.8516  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.017    0.001 24.549 0.000  0.016  0.018\nC(tier, Treatment('stable'))[T.fast]                        0.003    0.001  4.084 0.000  0.002  0.004\nC(tier, Treatment('stable'))[T.slow]                        0.003    0.001  5.118 0.000  0.002  0.004\nlog_resource_centered                                      -0.001    0.000 -6.741 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  3.890 0.000  0.000  0.001\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  2.356 0.018  0.000  0.000\nstyle_swd                                                   0.006    0.008  0.712 0.477 -0.011  0.023\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H1/m_openclip/tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.01868568326697234,
    "C(tier, Treatment('stable'))[T.fast]": 0.0030686709208683745,
    "C(tier, Treatment('stable'))[T.slow]": 0.002141693142701054,
    "log_resource_centered": -0.000589281804685507,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00034222043111990693,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00018168134691903497
  },
  "pvalues": {
    "Intercept": 1.9528458734152035e-299,
    "C(tier, Treatment('stable'))[T.fast]": 0.0001057816795907569,
    "C(tier, Treatment('stable'))[T.slow]": 0.0015793715643243808,
    "log_resource_centered": 4.634277274827379e-13,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.007316457652906579,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.09636288027095524,
    "Group Var": 0.0003080810475028801
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.01769547937919903,
      "C(tier, Treatment('stable'))[T.fast]": 0.0015173195755522047,
      "C(tier, Treatment('stable'))[T.slow]": 0.0008131952199136377,
      "log_resource_centered": -0.0007489049018597772,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 9.21390997875371e-05,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": -3.247551071739867e-05,
      "Group Var": 0.39707689002558666
    },
    "1": {
      "Intercept": 0.019675887154745653,
      "C(tier, Treatment('stable'))[T.fast]": 0.0046200222661845446,
      "C(tier, Treatment('stable'))[T.slow]": 0.0034701910654884706,
      "log_resource_centered": -0.00042965870751123685,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0005923017624522768,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0003958382045554686,
      "Group Var": 1.3413080881584287
    }
  },
  "random_intercept_variance": 3.4267964685617754e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1269.1327  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.019    0.001 36.986 0.000  0.018  0.020\nC(tier, Treatment('stable'))[T.fast]                        0.003    0.001  3.877 0.000  0.002  0.005\nC(tier, Treatment('stable'))[T.slow]                        0.002    0.001  3.160 0.002  0.001  0.003\nlog_resource_centered                                      -0.001    0.000 -7.236 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  2.682 0.007  0.000  0.001\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  1.663 0.096 -0.000  0.000\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H1/m_openclip/tier/kruskal

```json
{
  "statistic": 6.246373307543536,
  "pvalue": 0.04401667877720878
}
```

## H1/m_openclip/tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.0012492191696550341,
    "permutation_p": 0.12358764123587641,
    "cohen_d_independent": 0.4702818849443738,
    "mann_whitney_p": 0.05438378483952029,
    "n_a": 11,
    "n_b": 16,
    "holm_p": 0.24717528247175283
  },
  "fast_vs_slow": {
    "difference": -0.0011638900782623193,
    "permutation_p": 0.772022797720228,
    "cohen_d_independent": -0.30262381642198927,
    "mann_whitney_p": 0.6371803931683785,
    "n_a": 11,
    "n_b": 20,
    "holm_p": 0.772022797720228
  }
}
```

## H1/m_openclip/dd_tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(dd_tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.019154333611511788,
    "C(dd_tier, Treatment('stable'))[T.fast]": 0.002930200783401863,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.0006631040649494615,
    "log_resource_centered": -0.000615308889027311,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00033396049228752374,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00022574482877822508
  },
  "pvalues": {
    "Intercept": 0.0,
    "C(dd_tier, Treatment('stable'))[T.fast]": 4.9758763021617596e-05,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.35070693720405344,
    "log_resource_centered": 3.6154619277175894e-14,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00424227871266063,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.04942484667864527,
    "Group Var": 0.0003130761491231158
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.018169571709060486,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.00151451635199057,
      "C(dd_tier, Treatment('stable'))[T.slow]": -0.0007295595732055005,
      "log_resource_centered": -0.0007745329171055313,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00010506152991313598,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 5.680488143314276e-07,
      "Group Var": 0.39369572694903293
    },
    "1": {
      "Intercept": 0.02013909551396309,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.004345885214813156,
      "C(dd_tier, Treatment('stable'))[T.slow]": 0.0020557677031044237,
      "log_resource_centered": -0.0004560848609490908,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0005628594546619115,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00045092160874211874,
      "Group Var": 1.3322641186945479
    }
  },
  "random_intercept_variance": 3.385312654412987e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                 Mixed Linear Model Regression Results\n========================================================================================================\nModel:                             MixedLM                Dependent Variable:                ret_swd_k10\nNo. Observations:                  282                    Method:                            REML       \nNo. Groups:                        47                     Scale:                             0.0000     \nMin. group size:                   6                      Log-Likelihood:                    1269.8689  \nMax. group size:                   6                      Converged:                         Yes        \nMean group size:                   6.0                                                                  \n--------------------------------------------------------------------------------------------------------\n                                                              Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n--------------------------------------------------------------------------------------------------------\nIntercept                                                      0.019    0.001 38.123 0.000  0.018  0.020\nC(dd_tier, Treatment('stable'))[T.fast]                        0.003    0.001  4.057 0.000  0.002  0.004\nC(dd_tier, Treatment('stable'))[T.slow]                        0.001    0.001  0.933 0.351 -0.001  0.002\nlog_resource_centered                                         -0.001    0.000 -7.574 0.000 -0.001 -0.000\nC(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  2.860 0.004  0.000  0.001\nC(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  1.965 0.049  0.000  0.000\nGroup Var                                                      0.000    0.000                           \n========================================================================================================\n"
}
```

## H1/m_openclip/dd_tier/kruskal

```json
{
  "statistic": 34.43836436170213,
  "pvalue": 3.325096057290829e-08
}
```

## H1/m_openclip/dd_tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.006421774942693087,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 2.1754061272042193,
    "mann_whitney_p": 1.1582319258192444e-06,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  },
  "fast_vs_slow": {
    "difference": 0.004181060145140299,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 1.3801508776899887,
    "mann_whitney_p": 0.0001278992694307049,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  }
}
```

## H1/m_openclip/style_control

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered + style_swd",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.018478307742559676,
    "C(tier, Treatment('stable'))[T.fast]": 0.003004860162290236,
    "C(tier, Treatment('stable'))[T.slow]": 0.002137393858204075,
    "log_resource_centered": -0.000589281804685507,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0003422204311199068,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00018168134691903495,
    "style_swd": 0.0033072996019648904
  },
  "pvalues": {
    "Intercept": 4.0479938437579057e-122,
    "C(tier, Treatment('stable'))[T.fast]": 0.0002498860222653056,
    "C(tier, Treatment('stable'))[T.slow]": 0.001801463552488043,
    "log_resource_centered": 4.634288052373092e-13,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.007316460211490718,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.09636289479431909,
    "style_swd": 0.7288330529339915,
    "Group Var": 0.0003340540455745547
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.016937187639386533,
      "C(tier, Treatment('stable'))[T.fast]": 0.001396773896187221,
      "C(tier, Treatment('stable'))[T.slow]": 0.0007951913951080895,
      "log_resource_centered": -0.0007489049088220359,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 9.213908887977391e-05,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": -3.247552005824895e-05,
      "style_swd": -0.015390695235946134,
      "Group Var": 0.403893384860077
    },
    "1": {
      "Intercept": 0.02001942784573282,
      "C(tier, Treatment('stable'))[T.fast]": 0.004612946428393251,
      "C(tier, Treatment('stable'))[T.slow]": 0.003479596321300061,
      "log_resource_centered": -0.0004296587005489782,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0005923017733600398,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00039583821389631887,
      "style_swd": 0.022005294439875915,
      "Group Var": 1.3767613068369675
    }
  },
  "random_intercept_variance": 3.510121071055728e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1265.4550  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.018    0.001 23.500 0.000  0.017  0.020\nC(tier, Treatment('stable'))[T.fast]                        0.003    0.001  3.662 0.000  0.001  0.005\nC(tier, Treatment('stable'))[T.slow]                        0.002    0.001  3.121 0.002  0.001  0.003\nlog_resource_centered                                      -0.001    0.000 -7.236 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  2.682 0.007  0.000  0.001\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  1.663 0.096 -0.000  0.000\nstyle_swd                                                   0.003    0.010  0.347 0.729 -0.015  0.022\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H1/siglip2/tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.014590409592382336,
    "C(tier, Treatment('stable'))[T.fast]": 0.0019748797241756367,
    "C(tier, Treatment('stable'))[T.slow]": 0.0011024808465486607,
    "log_resource_centered": -0.00041745225575183514,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00023903964339374952,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 4.6517414391495106e-05
  },
  "pvalues": {
    "Intercept": 0.0,
    "C(tier, Treatment('stable'))[T.fast]": 0.0007028145886882424,
    "C(tier, Treatment('stable'))[T.slow]": 0.027178622100260896,
    "log_resource_centered": 1.110434179037989e-08,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.03679503798082548,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.6351467878049584,
    "Group Var": 0.0010640831660494602
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.01386129057106099,
      "C(tier, Treatment('stable'))[T.fast]": 0.0008325697528766441,
      "C(tier, Treatment('stable'))[T.slow]": 0.00012426502933107091,
      "log_resource_centered": -0.0005606695751135212,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 1.4661226173081282e-05,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": -0.00014562878259732112,
      "Group Var": 0.2130238812248087
    },
    "1": {
      "Intercept": 0.015319528613703682,
      "C(tier, Treatment('stable'))[T.fast]": 0.0031171896954746295,
      "C(tier, Treatment('stable'))[T.slow]": 0.0020806966637662502,
      "log_resource_centered": -0.00027423493639014906,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00046341806061441773,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.0002386636113803113,
      "Group Var": 0.8489784410472145
    }
  },
  "random_intercept_variance": 1.6852620127988044e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1307.7608  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.015    0.000 39.221 0.000  0.014  0.015\nC(tier, Treatment('stable'))[T.fast]                        0.002    0.001  3.388 0.001  0.001  0.003\nC(tier, Treatment('stable'))[T.slow]                        0.001    0.000  2.209 0.027  0.000  0.002\nlog_resource_centered                                      -0.000    0.000 -5.713 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  2.088 0.037  0.000  0.000\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  0.474 0.635 -0.000  0.000\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H1/siglip2/tier/kruskal

```json
{
  "statistic": 5.89303675048356,
  "pvalue": 0.05252225075636557
}
```

## H1/siglip2/tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.000990058703337321,
    "permutation_p": 0.11538846115388461,
    "cohen_d_independent": 0.4905703526815489,
    "mann_whitney_p": 0.044335520930490445,
    "n_a": 11,
    "n_b": 16,
    "holm_p": 0.23077692230776922
  },
  "fast_vs_slow": {
    "difference": -0.0005726466601384504,
    "permutation_p": 0.6893310668933107,
    "cohen_d_independent": -0.21714644487204485,
    "mann_whitney_p": 0.5246903977520454,
    "n_a": 11,
    "n_b": 20,
    "holm_p": 0.6893310668933107
  }
}
```

## H1/siglip2/dd_tier/lme

```json
{
  "formula": "ret_swd_k10 ~ C(dd_tier, Treatment('stable')) * log_resource_centered",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.014647370157620269,
    "C(dd_tier, Treatment('stable'))[T.fast]": 0.001976316723661434,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.0007157122797375889,
    "log_resource_centered": -0.0003320178755036872,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 5.578391271955275e-06,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": -3.3706710973821075e-05
  },
  "pvalues": {
    "Intercept": 0.0,
    "C(dd_tier, Treatment('stable'))[T.fast]": 0.00015556241260164427,
    "C(dd_tier, Treatment('stable'))[T.slow]": 0.16383850475077344,
    "log_resource_centered": 6.798120848527488e-06,
    "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.9580573056734372,
    "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.7466718494818889,
    "Group Var": 0.0013586317413299632
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.013934934113745863,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.0009521253803746481,
      "C(dd_tier, Treatment('stable'))[T.slow]": -0.0002918244358330298,
      "log_resource_centered": -0.000476630237127294,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": -0.00020231497709510964,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": -0.0002382194740687284,
      "Group Var": 0.18888932569760813
    },
    "1": {
      "Intercept": 0.015359806201494675,
      "C(dd_tier, Treatment('stable'))[T.fast]": 0.0030005080669482194,
      "C(dd_tier, Treatment('stable'))[T.slow]": 0.0017232489953082075,
      "log_resource_centered": -0.00018740551388008044,
      "C(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.0002134717596390202,
      "C(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00017080605212108627,
      "Group Var": 0.7844110151251062
    }
  },
  "random_intercept_variance": 1.5747390468902006e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                 Mixed Linear Model Regression Results\n========================================================================================================\nModel:                             MixedLM                Dependent Variable:                ret_swd_k10\nNo. Observations:                  282                    Method:                            REML       \nNo. Groups:                        47                     Scale:                             0.0000     \nMin. group size:                   6                      Log-Likelihood:                    1306.4433  \nMax. group size:                   6                      Converged:                         Yes        \nMean group size:                   6.0                                                                  \n--------------------------------------------------------------------------------------------------------\n                                                              Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n--------------------------------------------------------------------------------------------------------\nIntercept                                                      0.015    0.000 40.296 0.000  0.014  0.015\nC(dd_tier, Treatment('stable'))[T.fast]                        0.002    0.001  3.782 0.000  0.001  0.003\nC(dd_tier, Treatment('stable'))[T.slow]                        0.001    0.001  1.392 0.164 -0.000  0.002\nlog_resource_centered                                         -0.000    0.000 -4.500 0.000 -0.000 -0.000\nC(dd_tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  0.053 0.958 -0.000  0.000\nC(dd_tier, Treatment('stable'))[T.slow]:log_resource_centered -0.000    0.000 -0.323 0.747 -0.000  0.000\nGroup Var                                                      0.000    0.000                           \n========================================================================================================\n"
}
```

## H1/siglip2/dd_tier/kruskal

```json
{
  "statistic": 33.55797872340426,
  "pvalue": 5.1638962524909776e-08
}
```

## H1/siglip2/dd_tier/contrasts

```json
{
  "fast_vs_stable": {
    "difference": 0.004568777513320464,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 2.298647406112736,
    "mann_whitney_p": 1.4058003251457457e-06,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  },
  "fast_vs_slow": {
    "difference": 0.0030467176950356636,
    "permutation_p": 9.999000099990002e-05,
    "cohen_d_independent": 1.48706040606731,
    "mann_whitney_p": 6.823017917787652e-05,
    "n_a": 15,
    "n_b": 16,
    "holm_p": 0.00019998000199980003
  }
}
```

## H1/siglip2/style_control

```json
{
  "formula": "ret_swd_k10 ~ C(tier, Treatment('stable')) * log_resource_centered + style_swd",
  "n": 282,
  "concepts": 47,
  "converged": true,
  "coefficients": {
    "Intercept": 0.014019115516165677,
    "C(tier, Treatment('stable'))[T.fast]": 0.001799088928816344,
    "C(tier, Treatment('stable'))[T.slow]": 0.0010906368462886547,
    "log_resource_centered": -0.0004174522557518352,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00023903964339374965,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 4.6517414391495146e-05,
    "style_swd": 0.009111203823243878
  },
  "pvalues": {
    "Intercept": 2.4958869128015614e-134,
    "C(tier, Treatment('stable'))[T.fast]": 0.002416844136000789,
    "C(tier, Treatment('stable'))[T.slow]": 0.02757425425050175,
    "log_resource_centered": 1.1104332995896018e-08,
    "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.036795033539355794,
    "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.6351467798274666,
    "style_swd": 0.18641251710068207,
    "Group Var": 0.0012630874844246165
  },
  "confidence_intervals": {
    "0": {
      "Intercept": 0.01290514197223636,
      "C(tier, Treatment('stable'))[T.fast]": 0.0006367099856655447,
      "C(tier, Treatment('stable'))[T.slow]": 0.00012044767582286716,
      "log_resource_centered": -0.0005606695717361428,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 1.4661231464416631e-05,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": -0.00014562877806609234,
      "style_swd": -0.0044043369390063414,
      "Group Var": 0.2036544982204933
    },
    "1": {
      "Intercept": 0.015133089060094994,
      "C(tier, Treatment('stable'))[T.fast]": 0.002961467871967143,
      "C(tier, Treatment('stable'))[T.slow]": 0.0020608260167544424,
      "log_resource_centered": -0.00027423493976752757,
      "C(tier, Treatment('stable'))[T.fast]:log_resource_centered": 0.00046341805532308265,
      "C(tier, Treatment('stable'))[T.slow]:log_resource_centered": 0.00023866360684908264,
      "style_swd": 0.022626744585494095,
      "Group Var": 0.8350931624899964
    }
  },
  "random_intercept_variance": 1.6483597579803009e-06,
  "warnings": [
    "The MLE may be on the boundary of the parameter space."
  ],
  "summary": "                                Mixed Linear Model Regression Results\n=====================================================================================================\nModel:                            MixedLM               Dependent Variable:               ret_swd_k10\nNo. Observations:                 282                   Method:                           REML       \nNo. Groups:                       47                    Scale:                            0.0000     \nMin. group size:                  6                     Log-Likelihood:                   1304.5727  \nMax. group size:                  6                     Converged:                        Yes        \nMean group size:                  6.0                                                                \n-----------------------------------------------------------------------------------------------------\n                                                           Coef.  Std.Err.   z    P>|z| [0.025 0.975]\n-----------------------------------------------------------------------------------------------------\nIntercept                                                   0.014    0.001 24.666 0.000  0.013  0.015\nC(tier, Treatment('stable'))[T.fast]                        0.002    0.001  3.034 0.002  0.001  0.003\nC(tier, Treatment('stable'))[T.slow]                        0.001    0.000  2.203 0.028  0.000  0.002\nlog_resource_centered                                      -0.000    0.000 -5.713 0.000 -0.001 -0.000\nC(tier, Treatment('stable'))[T.fast]:log_resource_centered  0.000    0.000  2.088 0.037  0.000  0.000\nC(tier, Treatment('stable'))[T.slow]:log_resource_centered  0.000    0.000  0.474 0.635 -0.000  0.000\nstyle_swd                                                   0.009    0.007  1.321 0.186 -0.004  0.023\nGroup Var                                                   0.000    0.000                           \n=====================================================================================================\n"
}
```

## H2/pooled_descriptive

```json
{
  "rho": 0.6455325469191707,
  "nominal_p": 1.2289187538273884e-34,
  "n_pairs": 282,
  "n_languages": 6
}
```

## H2/language_level

```json
{
  "rho": 0.6,
  "n_languages": 6,
  "exact_one_sided_p": 0.12083333333333333
}
```

## H3/clip/original

```json
{
  "W": 26.0,
  "pvalue": 7.595701845275471e-12,
  "n_concepts": 47,
  "below_null": 43
}
```

## H3/m_openclip/original

```json
{
  "W": 27.0,
  "pvalue": 8.959943897934863e-12,
  "n_concepts": 47,
  "below_null": 41
}
```

## H3/siglip2/original

```json
{
  "W": 30.0,
  "pvalue": 1.4459544672718039e-11,
  "n_concepts": 47,
  "below_null": 41
}
```

## H3/clip/color_normalized

```json
{
  "W": 45.0,
  "pvalue": 1.197761889670801e-10,
  "n_concepts": 47,
  "below_null": 42
}
```

## artifact/style_swd

```json
{
  "rho": 0.4714384828862164,
  "pvalue": 0.0008229877306999255,
  "n": 47
}
```

## artifact/delta_sharpness

```json
{
  "rho": 0.2682701202590194,
  "pvalue": 0.06826943790116849,
  "n": 47
}
```

## H1/clip/tier/normalized_heldout

```json
{
  "kruskal_statistic": 7.33520309477754,
  "pvalue": 0.025537647388820157,
  "n_concepts": 47
}
```

## H1/clip/dd_tier/normalized_heldout

```json
{
  "kruskal_statistic": 35.398825354609954,
  "pvalue": 2.057040021333127e-08,
  "n_concepts": 47
}
```
