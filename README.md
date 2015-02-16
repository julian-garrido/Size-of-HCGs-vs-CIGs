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
    --> Save results at datasets/results/sextractor/ds9jpeg

12. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the results of 2nd iteration of sextractor workflows.
   to preview only valid results.
    --> Input file: datasets/results/sextractor2ndtIterationTables/valid_band_g_results.text
    --> Save results at datasets/results/sextractor2/ds9jpeg



Workflows
=========
workflows/addRowEmptyTables.t2flow: Replace and empty TableData in a VOTable by an empty row (with nulls and NaN).
    PreCondition:
        - The first column in the VOTable must be the object name and it contains MAGICKEYTOREPLACE
workflows/BuildDS9Image4sexResults.t2flow: It creates preview images using ds9 and applying scale log option to all frames.


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

