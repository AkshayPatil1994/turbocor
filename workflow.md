# Workflow Recommendations

Setting up the pre-processing can be rather convoluted but here are some quick tips and guides to achieve the best results.

- Generating the stochastic coral bed can be relatively tricky. However, we recommend keeping the total number of coral to a manageable level using the `scale` option. This avoids two issues, a. the total filesize of the corals is small as this can be a concern when generating the SDF, b. with small file size it becomes easier to visualise and debug any potential issues
- It is important to ensure that the generated obj/stl file is watertight. This can be achived through the use of `geowrapper` code written by [Ivan Padjen]: