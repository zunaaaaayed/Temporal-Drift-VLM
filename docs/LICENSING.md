# Licensing

## Current software

The current Temporal Drift VLM research software, accompanying documentation, and
configurations are licensed under the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version. The SPDX identifier is `AGPL-3.0-or-later`. The unmodified license
text is in [LICENSE](../LICENSE).

The software is provided without warranty, as described in the license. Research
and commercial use are permitted. Distribution of covered software requires
compliance with the license's source-sharing and notice requirements. Under
section 13, a modified version supporting remote network interaction must prominently
offer its corresponding source to users interacting with it over that network.
Private local use does not by itself require publishing source, and merely running
the framework does not automatically place papers or numerical outputs under AGPL.

The full license governs these obligations. See the Free Software Foundation's
[explanation of AGPL](https://www.gnu.org/licenses/why-affero-gpl.html) and
[license text](https://www.gnu.org/licenses/agpl-3.0.html).

## Scope and historical releases

The switch to AGPL-3.0-or-later was made on 17 November 2026. Earlier versions,
including commit `23fa110c2efd08d0218cf5f61dc37add0826745a`, were published under
Apache-2.0. Their existing grants are not revoked. An unchanged copy of the original
license is retained in [LICENSES/Apache-2.0.txt](../LICENSES/Apache-2.0.txt), alongside
[NOTICE](../NOTICE) for attribution and licensing history. Its presence does not
provide a blanket Apache alternative for subsequent AGPL-only changes.

Completed experiment artifacts and the source snapshots under `runs/` remain
unchanged. Those historical snapshots retain their original Apache-2.0 licensing,
including the metadata captured at the time of each run. A historical
`license = "Apache-2.0"` entry in a frozen `pyproject.toml` is intentional.

Third-party photographs, datasets, model weights, dependencies, and any embedded
third-party content in figures retain their respective rights and licenses. This
software licensing change grants no additional rights to those materials or to the
historical draft paper and notebook. Check the applicable original terms before
redistributing them.

## Why AGPL was selected

AGPL supports reproducible research and reuse while keeping covered distributed
derivatives, and modified versions offered over a network, available under its
source-sharing terms. It permits commercial use; it is not a noncommercial license.

The other considered licenses address different priorities:

- [Anti-996](https://github.com/996icu/996.ICU/blob/master/LICENSE) adds labor-law and
  employment conditions. Those conditions do not provide AGPL's source-sharing model.
- [Server Side Public License](https://www.mongodb.com/legal/licensing/server-side-public-license)
  requires a broader set of service-management and hosting source code when offering
  the program as a service. That scope is unnecessary for this research framework.
- [Business Source License 1.1](https://mariadb.com/bsl11/) restricts production use
  unless an additional use grant permits it, and transitions to a specified change
  license. Its commercial licensing model is not the project's objective.

AGPL was adopted without adding any of those extra restrictions.
