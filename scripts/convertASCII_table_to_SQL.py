__author__ = 'Julian Garrido'

import numpy
import os
from numpy.core.records import fromarrays
from matplotlib.mlab import csv2rec
from StringIO import StringIO

pathDataFile ="/home/lourdes/src/Size-of-HCGs-vs-CIGs/datasets/results/KCorrect/"
data = csv2rec(pathDataFile + "R50_SM_HCG.txt", delimiter=' ')

sql_sentences = ""

#notice that the header contains invalid characters in the column names. Therefore, the names in the array doesn't
# correspond exactly to the names in the file
for i in range(data.size) :
    sql_sentences += "UPDATE `UNPUBLISHED_SIZES_HCG_VS_CIG`.`HCGgalaxies` " \
                    " SET `Dist(Mpc)` = "+ str(data[i]['distmpc']) + ", " + \
                    " `gmag` = "+ str(data[i]['mag_g']) + ", " + \
                    " `e_gmag` = "+ str(data[i]['e_mag_g']) + ", " + \
                    " `rmag` = "+ str(data[i]['mag_r']) + ", " + \
                    " `e_rmag` = "+ str(data[i]['e_mag_r']) + ", " + \
                    " `imag` = "+ str(data[i]['mag_i']) + ", " + \
                    " `e_imag` = "+ str(data[i]['e_mag_i']) + ", " + \
                    " `kmag` = "+ str(data[i]['mag_k']) + ", " + \
                    " `e_kmag` = "+ str(data[i]['e_mag_k']) + ", " + \
                    " `gmagExt` = "+ str(data[i]['ext_g']) + ", " + \
                    " `rmagExt` = "+ str(data[i]['ext_r']) + ", " + \
                    " `imagExt` = "+ str(data[i]['ext_i']) + ", " + \
                    " `Kcorr_g` = "+ str(data[i]['cork_g']) + ", " + \
                    " `Kcorr_r` = "+ str(data[i]['cork_r']) + ", " + \
                    " `Kcorr_i` = "+ str(data[i]['cork_i']) + ", " + \
                    " `Kcorr_k` = "+ str(data[i]['cork_k']) + ", " + \
                    " `gMag_abs` = "+ str(data[i]['mag_g_1']) + ", " + \
                    " `e_gMag_abs` = "+ str(data[i]['e_mag_g_1']) + ", " + \
                    " `rMag_abs` = "+ str(data[i]['mag_r_1']) + ", " + \
                    " `e_rMag_abs` = "+ str(data[i]['e_mag_r_1']) + ", " + \
                    " `iMag_abs` = "+ str(data[i]['mag_i_1']) + ", " + \
                    " `e_iMag_abs` = "+ str(data[i]['e_mag_i_1']) + ", " + \
                    " `KsMag_abs` = "+ str(data[i]['mag_ks']) + ", " + \
                    " `e_KsMag_abs` = "+ str(data[i]['e_mag_ks']) + ", " + \
                    " `log_SM(H0=70)` = "+ str(data[i]['log_smh070']) + ", " + \
                    " `e_log(SM)` = "+ str(data[i]['e_logsm']) + ", " + \
                    " `R50(arcsec)` = "+ str(data[i]['r50arcsec']) + ", " + \
                    " `e_R50(arcsec)` = "+ str(data[i]['e_r50arcsec']) + ", " + \
                    " `R50(kpc)` = "+ str(data[i]['r50kpc']) + ", " + \
                    " `e_R50(kpc)` = "+ str(data[i]['e_r50kpc']) + ", " + \
                    " `ELLIPTICITY` = "+ str(data[i]['ellipticity']) + ", " + \
                    " `THETA_IMAGE` = "+ str(data[i]['theta_image']) + ", " + \
                    " `a(arcsec)` = "+ str(data[i]['aarcsec']) + ", " + \
                    " `e_a(arcsec)` = "+ str(data[i]['e_aarcsec']) + ", " + \
                    " `b(arcsec)` = "+ str(data[i]['barcsec']) + ", " + \
                    " `e_b(arcsec)` = "+ str(data[i]['e_barcsec']) +  \
                    " WHERE `HCGgalaxies`.`ObjectName` = '"+ str(data[i]['hcg']) + "' ; " + os.linesep


#save sql sentences in a file

f = open(pathDataFile + 'sql_script_to_update_HCG_galaxies.sql', 'w')
f.write(sql_sentences)
f.close()








#data1 = numpy.loadtxt(pathInputDataFile + "R50_SM_HCG.txt", delimiter=' ', dtype={'names': ('hcg', 'ra', 'dec', 'z', 'err_z', 'distmpc', 'mag_g', 'e_mag_g', 'mag_r', 'e_mag_r', 'mag_i', 'e_mag_i', 'mag_k', 'e_mag_k',
#'ext_g', 'ext_r', 'ext_i', 'cork_g', 'cork_r', 'cork_i', 'cork_k', 'mag_g_1', 'e_mag_g_1', 'mag_r_1', 'e_mag_r_1', 'mag_i_1',
#'e_mag_i_1', 'mag_ks', 'e_mag_ks', 'log_smh070', 'e_logsm', 'r50arcsec', 'e_r50arcsec', 'r50kpc', 'e_r50kpc', 'ellipticity',
#'theta_image', 'aarcsec', 'e_aarcsec', 'barcsec', 'e_barcsec'), 'formats': ('S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11',
#                                                                            'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11',
#                                                                            'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11',
#                                                                            'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11',
#                                                                            'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11', 'S11')})











"""
'hcg', 'ra', 'dec', 'z', 'err_z', 'distmpc', 'mag_g', 'e_mag_g', 'mag_r', 'e_mag_r', 'mag_i', 'e_mag_i', 'mag_k', 'e_mag_k',
'ext_g', 'ext_r', 'ext_i', 'cork_g', 'cork_r', 'cork_i', 'cork_k', 'mag_g_1', 'e_mag_g_1', 'mag_r_1', 'e_mag_r_1', 'mag_i_1',
'e_mag_i_1', 'mag_ks', 'e_mag_ks', 'log_smh070', 'e_logsm', 'r50arcsec', 'e_r50arcsec', 'r50kpc', 'e_r50kpc', 'ellipticity',
'theta_image', 'aarcsec', 'e_aarcsec', 'barcsec', 'e_barcsec'


ALTER TABLE `HCGgalaxies`
	ADD `Dist(Mpc)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `gmag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_gmag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `rmag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_rmag` DECIMAL(8,4) NULL DEFAULT NULL,
	ADD `imag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_imag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `kmag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_kmag` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `gmagExt` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `rmagExt` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `imagExt` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `Kcorr_g` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `Kcorr_r` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `Kcorr_i` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `Kcorr_k` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `gMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_gMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `rMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_rMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `iMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_iMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `KsMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `e_KsMag_abs` DECIMAL(8,4) NULL DEFAULT NULL ,
	ADD `log_SM(H0=70)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `e_log(SM)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `R50(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `e_R50(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `R50(kpc)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `e_R50(kpc)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `ELLIPTICITY` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `THETA_IMAGE` DECIMAL(8,2) NULL DEFAULT NULL ,
	ADD `a(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `e_a(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `b(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL ,
	ADD `e_b(arcsec)` DECIMAL(8,3) NULL DEFAULT NULL;
"""
