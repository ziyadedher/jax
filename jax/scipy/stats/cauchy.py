# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy as np
import scipy.stats as osp_stats

from jax import lax
from jax.numpy import lax_numpy as jnp
from jax.scipy.stats._freezing import Freezer


freeze = Freezer(__name__.split(".")[-1], loc=0, scale=1)


@freeze.wrap
@jnp._wraps(osp_stats.cauchy.logpdf, update_doc=False)
def logpdf(x, loc=0, scale=1):
  x, loc, scale = jnp._promote_args_inexact("cauchy.logpdf", x, loc, scale)
  one = jnp._constant_like(x, 1)
  pi = jnp._constant_like(x, np.pi)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.mul(pi, scale))
  return lax.neg(lax.add(normalize_term, lax.log1p(lax.mul(scaled_x, scaled_x))))


@freeze.wrap
@jnp._wraps(osp_stats.cauchy.pdf, update_doc=False)
def pdf(x, loc=0, scale=1):
  return lax.exp(logpdf(x, loc, scale))
