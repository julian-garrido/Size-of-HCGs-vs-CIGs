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
	   +- datasets: input data and result data for different steps of the experiment. datasets/results folders is not completely in GitHub due to size restrictions
	   |
	   +- config: configuration and template files to be able to run the workflows and scripts
	   |
	   +- fig: folder with figures
	   |
	   +- test: folder that is used for testing specific parts of the experiment.
	   |
	   +- data_obsolete: files that are of no use but are preserved.



Log that summarizes the steps accomplished during the realization of this part of the experiment
============================================================================================================

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
10. Save all results of setp 9 in datasets/results/sextractor2ndIterationTables

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
    (all the images where cut but one (HCG 37c)

19. Execute workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow
    --> Input table:  datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml

20??. Run BuildDS9Image4sexResults.t2flow to create preview images of the resulting sextractor seg images
   in order to be able to verify the quality of the results. Do it for the results the previous step.
   to preview only valid results.
    --> Input file: datasets/results/ ********************sextractor1stIterationTables/valid_band_g_results.text
    --> Save results at datasets/results/sextractor/ds9jpeg


21. Review all results with mirian and modify additional sex config files. During the revision:
    i) commands to run sextractor and build ds9 pre-visualization are saved in scripts/edit_and_visualize_seconfig_and_results.txt
    ii) the review was documented at http://amiga.iaa.es:8888/display/science/Review+of+source+detection
    iii) three images from dataset/images are modified to mask a star (HCG 06b, 06c and 97a). new image files are created and
    added to the results/images folders (with -ptch sufix, patched). The tableforCustomizedListOfConfigFiles.xml file is modified accordingly.
    iv) the file datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml is modified to force the use
    of different images for some galaxies (this is done when one image is too small and the image from a galaxy of the same
    group is bigger)


22. Execute workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow
    --> Input table:  datasets/inputs/gather_galaxy_porperties/tableforCustomizedListOfConfigFiles.xml

23. Save results in datasets/results/sextractor3rdIterationTables.
    This includes votable_band_XXX_results.text files (for each band).

24. Run combineVOtables.t2flow wf to combine results from 1st iteration of the processing wf (sextractor) and
    the 3rd iteration of the workflow (considering the customized sex configuration files).
    Remove also the galaxies that are rejected in the manual review
     Inputs:
      - list of galaxies to be removed from the VOTable (the ones resulting from the manual review of Julian an Mirian
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor1stIterationTables/valid_band_g_results.text
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor1stIterationTables/valid_band_i_results.text
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor1stIterationTables/valid_band_r_results.text
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor3rdIterationTables/valid_band_g_results.text
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor3rdIterationTables/valid_band_i_results.text
      - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor3rdIterationTables/valid_band_r_results.text
     The taverna file with the parameters for this workflow is in  datasets/inputs/combineVOTables folder

25. Save results of the previous wf execution in datasets/results/combine_1st_and_3rd_it_results/
    results:
    - asciiTable_band_g.text
    - table_band_g.text
    - asciiTable_band_i.text
    - table_band_i.text
    - asciiTable_band_r.text
    - table_band_r.text
    - list_of_galaxies_to_reject_from_votable1.text
    - list_of_galaxies_to_reject_from_votable2.text
    Comment: the HCG galaxy should have been rejected, but it wasn't.

26. Fix bug:
    bug description: the flux values is missing in the final table because sextractor provides a column with float type
    and pair of values separated by spaces. After the first operation, the values are lost and replaced by a NaN.
    resolution: modify the beanshells that read the cat files. Now, they also replace the float type by a char type.
    workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow is fixed. The other workflow is pending

27. Duplicate datasets/results/preprocessing/cleanedOutputTable.xml into datasets/results/preprocessing/cleanedOutputTable_patched.xml
    Modify the resulting file to include the changes that were introduced in tableforCustomizedListOfConfigFiles.xml
      - changes in the images to be processed for each galaxy. Some of them were replaced because of the size or
        because they were edited: 06b, 06c, 17e -> 17a, 37c -> 37b, 51d -> 51c, 69d -> 69a, 74e -> 74c

28. Execute workflows/Gather_HCG_galaxy_properties_using_existing_sexConfigFile.t2flow
    input Table: File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/preprocessing/cleanedOutputTable_patched.xml

29. Save results at: datasets/results/sextractor4thIteration/
- valid_band_g_results.text
- valid_band_i_results.text
- valid_band_r_results.text

30. Execute workflow/removeRejectedSubSample.t2flow using the results from the previous step:
    - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor4thIterationTables/valid_band_r_results.text
    - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor4thIterationTables/valid_band_i_results.text
    - File : /home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/sextractor4thIterationTables/valid_band_g_results.text
    - list of galaxies to be removed according to the manual review.

31. Comparision between the results of step 25 and 30 for band g (using band g):
   - galaxies 51d is in the result of step 25 but not in step 30. It didn't pass the filters because of the size in one band
   - galaxies 82c is in the result of step 25 but not in step 30. 82c was rejected and it is right if it is not in step 30

32. Provide results from step 30 to Mirian to perform K Correction.
    Result is saved in datasets/results/KCorrect/R50_SM_HCG.txt

33. Run script (scripts/convertASCII_table_to_SQL.py) to transform datasets/results/KCorrect/R50_SM_HCG.txt data into sql update sentences. The resulting sql
    script is saved in datasets/results/KCorrect/sql_script_to_update_HCG_galaxies.sql and run in the DB.

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

workflows/combineVOtables.t2flow
    It combines votables (with the same columns) and transforms them into ascii tables. For the three bands
    The combined tables are provided in votable and ascii formats.
    The columns that refer to file names and paths thar were used during the execution of other workflwos, have been removed
    in the ascii table.

workflow/removeRejectedSubSample.t2flow
    This workflow removed from the input table a list of rows corresponding to the rejected subsample.
    It also transform the table into ascii format. In this case, several columns are not in the ascii file

Some of the nested workflows:

workflows/addRowEmptyTables.t2flow: Replace and empty TableData in a VOTable by an empty row (with nulls and NaN).
    PreCondition:
        - The first column in the VOTable must be the object name and it contains MAGICKEYTOREPLACE

workflows/BuildDS9Image4sexResults.t2flow: It creates preview images using ds9 and applying scale log option to all frames.

workflows/sextractor.t2flow: Run sextractor to apply source extraction to an image

workflows/combineVOtablesForOneBand.t2flow
    It makes the same thing that combineVOtables.t2flow, but for one band.



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

