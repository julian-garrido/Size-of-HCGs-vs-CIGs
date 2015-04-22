> Work in progress! This GitHub repository contains an in-progress Research Object (see [http://www.researchobject.org/](http://www.researchobject.org/)), and as such, all of its content, including this README file, can be in an incoherent state while this notice remains in display.

Introduction
============

This repository is the [Research Object (RO)](http://www.researchobject.org/ "Research Object portal") for the comparison of sizes between HCGs and the CIGs.

It has the following structure:

    project
	   |
	   +- README.md: This file
	   |
	   +- article: folder with the article to be written about this RO
	   |
	   +- sql: folder with SQL related-stuff
	   |
	   +- scripts: folder with Python scripts, other
	   |
	   +- workflows: folder with Taverna workflows
	   |
	   +- datasets: input data and result data for different steps of the experiment
	   |
	   +- config: configuration files to be able to run the workflows and scripts


Steps to reproduce
==================

1. Create Table 'HCGgalaxies' (See HCGgalaxies_table.sql)
2. Fill Table 'HCGgalaxies' with the sample selection (use: datasets/inputs/preprocessing/sample_selection/galaxy-names-hcg-ned-output-cut.csv)
3. Add new columns to HCGgalaxies table and calculate new values (See sql/HCGgalaxies_table.sql)
4. Extract from the DB the input data for the workflow 'gather and preprocessing data'.
    --> see query to 'extract sample selection' in HCGgalaxies_table.sql file
    --> exported to datasets/inputs/preprocessing/sample/selection/sample_selection_Extracted_from_db.ascii
5. Run 'gather and preprocessing data' workflow (it downloads images and set up filenames to run the next workflow).
    --> input file: datasets/inputs/preprocessing/sample/selection/sample_selection_Extracted_from_db.ascii
    --> Export result into datasets/results/preprocessing/votable.xml
    --> Name files with - implies that nothing was downloaded
    --> Save result (without the rows corresponding to the galaxies without data in SLOAN) into
             datasets/results/preprocessing/cleanedOutputTable.xml
6. Run 'gather HCG galaxy properties using sextractor' workflow.
    --> Use as input the result from the previous workflow
    --> Intial values for Deblend_Mincont (sextractor parameter in cat file): i=0.02; r=0.02; g=0,03; u=0,05; z=0.005
7. Save results in datasets/results/sextractor1stIterationTables
    --> This includes tables with valid results that have passed the filters: valid_band_i_results.text, valid_band_g_results.text, valid_band_r_results.text
    --> There are two files 'table_for_another_iteration.text' (xml) and 'table_for_another_iteration_ascii.text' that contains the table with the galaxies that didn't pass the filters
8. Run 'gather and preprocessing data withDeblend' using as input 'table_for_another_iteration_ascii.text' (1h execution without provenance)
    --> This is a preparatory workflow to provide inputs for the iteration over DEBLEND sextractor parameter in bands rgi.
    --> Save results as datasets/results/preprocessing/outputTableForA2ndIteration.xml
    --> Save additional results as datasets/results/preprocessing/outputTableForA2ndIteration_raw.xml
9. Run 'gather HCG galaxy properties using sextractor_withDeblend' workflow.
    --> Use as input the result from the previous workflow
        --> datasets/results/preprocessing/outputTableForA2ndIteration.xml
    --> Remove recording of intermediate data in Taverna to avoid running out of memory
10. Save all results of setep 9 in datasets/results/sextractor2ndIterationTables

11. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the results of 1st iteration of sextractor workflows.
   to preview only valid results.
    --> Input file: datasets/results/sextractor1stIterationTables/valid_band_g_results.text
    --> Save result images at datasets/results/sextractor/ds9jpeg
    --> Save provenance files into datasets/results/ds9wf_1st_ite_good_results

12. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the results of 2nd iteration of sextractor workflows.
   to preview only valid results.
    --> Input file: datasets/results/sextractor2ndtIterationTables/valid_band_g_results.text
    --> Save result images at datasets/results/sextractor2/ds9jpeg
    --> Save provenance files into datasets/results/ds9wf_2nd_ite_good_results

13. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the bad results of 2nd iteration of sextractor workflows.
   to preview only valid results.
    --> Input file: /datasets/results/sextractor2ndIterationTables/table_for_another_iteration.text
    --> Save result images at datasets/results/sextractor2/ds9jpeg_badresults
    --> Save provenance files into datasets/results/ds9wf_2nd_ite_bad_results

14. Review the ds9 previews and elaborate a list of the galaxies whose results can be improved by tunning the sextractor
    configuration file.
    --> Save votable file with these galaxies in datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml

15. Tune configuration files that are in datasets/results/sextractor for galaxies selected in the previous step.

16. Identify galaxies that were not detected in step 6 (run 'gather HCG galaxy properties using sextractor' workflow).
    For that, select galaxies that have NULL and NaN values in votable_band_g.text, votable_band_r.text,
    votable_band_i.text files (these are in datasets/results/sextractor1stIterationTables).

    This step could be included to the workflow but we do it creating a subset in topcat to avoid rerunning all workflows
    --> Save result in datasets/inputs/gather_galaxy_porperties/tablewithNoDetections.xml

17. Tune configuration files that are in datasets/results/sextractor for galaxies selected in the previous step
    (datasets/inputs/gather_galaxy_porperties/tablewithNoDetections.xml) and create previews
    --> Create previews in datasets/results/sextractor/ds9jpeg
    --> see command line file for more details scripts/edit_and_visualize_sexconfig_and_results.txt

18. Review the ds9 previews and and select the ones to be added to the list of the galaxies whose results can be
    improved by tunning the sextractor configuration file.
    --> Modify votable file adding these galaxies in datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml

19. Execute workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow
    --> Input table:  datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml

20??. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the results the previous step.
   to preview only valid results.
    --> Input file: datasets/results/ ********************sextractor1stIterationTables/valid_band_g_results.text
    --> Save results at datasets/results/sextractor/ds9jpeg


21. Review all results with mirian and modify additional sex config files. During the revision commands to run sextractor
    and build ds9 pre-visualization are saved in scripts/edit_and_visualize_seconfig_and_results.txt


Workflows
=========
workflows/gather_and_preprocessing_data.t2flow:
    It receives a sample selection and prepares a votable containing the required information an filenames that are
    required during the experiment and the following workflow executions

workflows/gather_and_preprocessing_data_withDeblend.t2flow :
    It receives a sample selection and prepares a votable containing the required information an filenames that are
    required during the experiment and the following workflow executions. For each galaxy, it considers different
    combinations of parameters.

Gather_HCG_galaxy_properties_using_sextractor.t2flow:
    It performs the source extraction and add to the input table information about the each galaxy if a filter criterium
    is passed. It requires that there is only one row for each galaxy and it may occur that there is no result for a
    particular galaxy due to the lack of detection. It returns also a table containing the galaxies for which there was
    no good results to easy another iteration.

Gather_HCG_galaxy_properties_using_sextractor_withDeblend.t2flow:
    It performs the source extraction and add to the input table information about the each galaxy if a filter criterium
    is passed. It considers that there might be more than one row for each galaxy and it may occur that there is no
    result for a particular galaxy due to the lack of detection. It returns also a table containing the galaxies for
    which there was no good results to easy another iteration.
    This workflow is indeed a copy of Gather_HCG_galaxy_properties_using_sextractor.t2flow where the nested
    workflow that creates the configuration file has been removed

workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow:
    It performs the source extraction without creating the sextractor configuration file. This is theoretically created
    in the execution of the previous workflows. The idea is to tune the cofiguration file for those cases where the initial
    execution is not perfect. But be carefull if you modify the same files, because they would be overwritten if you
    execute the previous workflows again.

Some of the nested workflows:

workflows/addRowEmptyTables.t2flow: Replace and empty TableData in a VOTable by an empty row (with nulls and NaN).
    PreCondition:
        - The first column in the VOTable must be the object name and it contains MAGICKEYTOREPLACE

workflows/BuildDS9Image4sexResults.t2flow: It creates preview images using ds9 and applying scale log option to all frames.

workflows/sextractor.t2flow: Run sextractor to apply source extraction to an image




Todo list
=========

1. TODO: Delete redundant fits files for sextractor workflow with deblend iteration
2. TODO: Explore results opening the fits files
3. TODO:
4. TODO:

Dependencies
============
1. Sextractor software
2. curl command line tool
3. Taverna 2.4 + Astrotaverna plugin or Taverna 2.5 Astronomy Edition. It requires the inclusion of stil.jar in taverna lib folder

Comments on sloan images
========
1. HCG74  returns only a image for g-band ---> removed from the workflow
2. HCG26  galaxies are not in sdr9 ---> removed from the workflow.
3. HCG77 returns only a image for g-band ---> removed from the workflow
4. HCG53 and HCG54 are very close. Is that a problem? --> I suppose it is not. 
5. HCG5, HCG36, HCG47 images were to small but this is fixed by including bigger sizes for those groups.
6. HCG10, HCG16, HCG31, HCG41, HCG59, HCG61, HCG72 images were too small

