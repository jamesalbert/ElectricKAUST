# Introduction to Jupyter
* "Interactive Computing Environment" allowing code, plot, texts, equations, etc. to be created and shared
* Requirements:
    - Python 3.6 (Recommended!) or 2.7 (even if working in R)
    - Web browser
    - Language-specific Kernel (R, Python, or Julia)

## Installing Anaconda:
[Download](https://www.continuum.io/downloads) the binary and follow the instructions.

* Important points:
    - Install the latest version (Python 3.6 or Python 2.7)
    - If you are asked during the installation process wheter you'd like to make Anaconda your default Python installation, say **yes**
    - Otherwise you can accept all of the defaults

* Package Management:
    - The packages in Anaconda ocontain the various scientific libraries used in day to day scientific programming. Anaconda supplies a great tool called ```conda``` to keep your packages organized and up to date.
    - Execute the follwing to update the whole Anaconda distribution:
        1. Open up a terminal
        2. Type ```conda update anaconda```

## Using the R Kernel (For R users)
 Note that Anaconda comes with the Python kernel, but if you are using R, you also need to install the R kernel. For this, go to command line and type:
```
conda install -c r r-essentials
```

### R packages in Python (Optoinal)
Most required packages such as numpy, pandas, scipy, and matplotlib come with the Anaconda installation. However, to use R packages in python you need to install rpy2 and statsmodels packages. You can use the ```conda``` install command in command-line (or the Anaconda prompt in Windows):
```
conda install rpy2
conda install statsmodels
```

* Note about packages for R in python:
```%matplotlib inline```
```
# Import required Python Packages
import numpy as np
import pandas as pd
import statsmodels.api as sm

import rpy2.robjects as robjs
import rpy2.robjects.packages import importr
from IPython.display import display

# Important R packages in Python
r = robjs.r
nlme = importr('nlme')
stats = importr('stats')
```

