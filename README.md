
# Learn JEDI

This tutorial series is designed to help you run the Joint Effort for Data assimilation Integration (JEDI) system through small, practical examples.

Please note that JEDI is under active development, so some YAML keys and configurations may change over time. If you encounter differences, refer to the ctest examples in the official JEDI code repositories for the most up-to-date reference. Each tutorial includes links to the relevant ctest examples to help you explore further.


## Requirements:
This tutorial assumes that you have set up your work environment (which can be done by loading [Spack-Stack modules](https://spack-stack.readthedocs.io/en/1.5.1/PreConfiguredSites.html) or using JCSDA [containers](https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/using/jedi_environment/containers/container_overview.html)) and that you have built [jedi-bundle](https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/using/building_and_running/building_jedi.html).


## Table of Contents:
1. How to run JEDI applications. This section includes tutorials about various Data Assimilation concepts and methods.
   1. [Running HofX3D application with JEDI](https://mer-a-o.github.io/howtojedi/jedi_applications/run_hofx/run_hofx3D.html)
   2. [Running HofX and saving GeoVaLs](https://mer-a-o.github.io/howtojedi/jedi_applications/run_hofx/run_hofx_save_geovals.html)
   3. [Running 4DVar application on Discover](https://mer-a-o.github.io/howtojedi/jedi_applications/run_var/4dvar/run_4dvar_discover.html)


2. How to use JEDI utilities. This section includes examples of the JEDI utilities available for pre- or post-processing.
   1. [Converting cubed sphere to lat/lon grid using JEDI](https://mer-a-o.github.io/howtojedi/jedi_utils/run_convert_to_latlon/convert_to_latlon.html)
   2. Changing the resolution of model output files


