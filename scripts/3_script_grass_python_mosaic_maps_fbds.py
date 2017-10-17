#---------------------------------------------------------------------------
#
# Modeling Atlantic Forest regenerability
# 
# 3. Combining maps to define a final raster map of natural vegetation
#    in the extended limit of the Atlantic Forest
# Including FBDS map
#
# Bernardo BS Niebuhr - bernardo_brandaum@yahoo.com.br
# Mauricio Humberto Vancine
#
# 02/06/2017
# Feel free to modify and share this code
#---------------------------------------------------------------------------

###--------------------------------------------------------------------###
## Import python modules
import os # operational system commands
import grass.script as grass # GRASS GIS commands
###--------------------------------------------------------------------###

# 1. Gather FBDS maps for all regions and all uses and export

# Region of study - for gathering FBDS maps regardless of AF limits

# # First trial - set it manually - NO!
#grass.run_command('g.region', n=3028995, s=138585, w=-74890, e=2742860, res = 30, flags = 'p') 
#grass.run_command('g.region', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp', res = 30, flags = 'ap') 

# List of maps
maps_fbds = grass.list_grouped('rast', pattern = '*v2*')['PERMANENT']

# Region of study
# # Second trial - align it to the resolution - problem - the pixels may displace a little!!
grass.run_command('g.region', rast = maps_fbds, res = 30, flags = 'ap') 

# # Third trial - use base map and increase an extesion to the west (dividible by the resolution 30m) to include all states
grass.run_command('g.region', rast = 'MA_extendido_rast', flags = 'p') # This extension already has resolution = 30m
grass.run_command('g.region', w = 'w-300000', flags = 'p') # reduce the west limit in 300km, which inclues all FBDS state maps and is divisible per 30
# this is ok! we kept only that.

# Combine maps
grass.run_command('r.patch', input = maps_fbds, output = 'FBDS_map_all_states', overwrite = True)

# Export FBDS map for all uses
folder = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined'
os.chdir(folder)
grass.run_command('r.out.gdal', input = 'FBDS_map_all_states', output = 'FBDS_map_all_states.tif')
# With compression
grass.run_command('r.out.gdal', input = 'FBDS_map_all_states', output = 'FBDS_map_all_states_compressed.tif', createopt="COMPRESS=DEFLATE")

# 2. Gather FBDS maps for all regions and each use separately, and export

out_dir = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined\separated_classes'
os.chdir(out_dir)

# 1 = water
expression1 = 'FBDS_map_all_states_water = if(FBDS_map_all_states == 1, 1, 0)'
grass.mapcalc(expression1, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_water', output = 'FBDS_map_all_states_water.tif')

# 2 = antropic areas
expression2 = 'FBDS_map_all_states_antropic_areas = if(FBDS_map_all_states == 2, 1, 0)'
grass.mapcalc(expression2, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_antropic_areas', output = 'FBDS_map_all_states_antropic_areas.tif')

# 3 = building area
expression3 = 'FBDS_map_all_states_building_areas = if(FBDS_map_all_states == 3, 1, 0)'
grass.mapcalc(expression3, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_building_areas', output = 'FBDS_map_all_states_building_areas.tif')

# 4 = forest
expression4 = 'FBDS_map_all_states_forest = if(FBDS_map_all_states == 4, 1, 0)'
grass.mapcalc(expression4, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_forest', output = 'FBDS_map_all_states_forest.tif')

# 5 = non forest natural areas
expression5 = 'FBDS_map_all_states_non_forest_natural_areas = if(FBDS_map_all_states == 5, 1, 0)'
grass.mapcalc(expression5, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_non_forest_natural_areas', output = 'FBDS_map_all_states_non_forest_natural_areas.tif')

# 6 = silviculture
expression6 = 'FBDS_map_all_states_silviculture = if(FBDS_map_all_states == 6, 1, 0)'
grass.mapcalc(expression6, overwrite = True)

grass.run_command('r.out.gdal', input = 'FBDS_map_all_states_silviculture', output = 'FBDS_map_all_states_silviculture.tif')

# better to do 1/null??

# Exporting compressed
per_class_maps_fbds = grass.list_grouped('rast', pattern = 'FBDS_map_all_states_*') ['PERMANENT']
out_dir = r'G:\regenerabilidade_MA\02_saidas\FBDS_combined\separated_classes'
os.chdir(out_dir)

for i in per_class_maps_fbds:
    # With compression
    grass.run_command('r.out.gdal', input = i, output = i+'_compressed.tif', createopt="COMPRESS=DEFLATE")    


#------------------------------------------
# 3. Maps for the expanded AF (the widest limit) - resolution 30m

out_dir_ext_AF = r'G:\regenerabilidade_MA\02_saidas\extended_AF'
os.chdir(out_dir_ext_AF)

# Region of study - for the AF
grass.run_command('g.region', vector = 'limite_ma_extendido_albers_sad69_shp', res = 30, flags = 'p',
                  align = 'MA_extendido_rast') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# a. FBDS map for this delimitation
grass.run_command('r.mask', vector = 'limite_ma_extendido_albers_sad69_shp') # Mask for the extended AF
grass.mapcalc('FBDS_map_extended_AF = FBDS_map_all_states', overwrite = True) # Filling SP with a binary map of forest patches

# Export
grass.run_command('r.out.gdal', input = 'FBDS_map_extended_AF', output = './fbds_raw/FBDS_map_extended_AF.tif')
# With compression
grass.run_command('r.out.gdal', input = 'FBDS_map_extended_AF', output = './fbds_raw/FBDS_map_extended_AF_compressed.tif', createopt="COMPRESS=DEFLATE")

grass.run_command('r.mask', flags = 'r') # Remove mask


# b. Get only forest
grass.mapcalc('FBDS_map_extended_AF_forest = if(FBDS_map_all_states == 4, 1, 0)', overwrite = True)
grass.run_command('r.mask', flags = 'r') # Remove mask

grass.run_command('r.mask', vector = 'limite_RJ_albers_sad69_shp')
grass.mapcalc('atlas_sosma_rj_2014_2015_albers_sad69_rast_HABMAT_only_RJ = atlas_sosma_rj_2014_2015_albers_sad69_rast_habmat', overwrite = True)
grass.run_command('r.mask', flags = 'r')


# 3. Combine forest patches from SOSMA 2014 with forest patches < 10 ha from the AF from Mapbiomas 2016 (considering all classes of natural forest - 1 to 8)

# 3.1 Reclassify AF map from MapBiomas 2016 - considering all classes of natural forest - 1 to 8
reclass_legend = ['1 thru 8 = 1 forest', 
                  '*        = NULL']

# Create txt file for reclassification
folder = r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas'
file_name = 'reclass_mapbiomas_vegetation_MA.txt'
os.chdir(folder)
reclass_file = open(file_name, 'w')
for i in reclass_legend:
    reclass_file.write(i)
    reclass_file.write('\n')
    
reclass_file.close()

# Reclassify
grass.run_command('r.reclass', input='MATAATLANTICA_colecao2_2016_albers_SAD69_tif', output='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8',
                  rules = file_name, overwrite = True)

# 3.2 Select only patches < 10ha from AF (MapBiomas 2016)

#grass.run_command('r.reclass.area', input = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8', output = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_less_10ha', mode = 'lesser', value = 10, overwrite = True)
# The above did not work - let's do it manually

# Clump areas functionally connected to generate a Patch ID map
grass.run_command('r.clump', input = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8', output = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump')

# Write file with patch area for reclassification, using r.stats
x=grass.read_command('r.stats',flags='a',input='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump').replace('\r','')
y=x.split('\n')
os.chdir(r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas')
txtsaida='reclass_area_less_10ha_mapbiomas.txt'
txtreclass=open(txtsaida, 'w')
#txtreclass.write('COD'+','+'HA\n')
if len(y)!=0:
    for i in y:
        if i !='':
            ##print i
            f=i.split(' ')
            if '*' in f :
                break
            else:
                ##print f
                ids=f[0]
                ids=int(ids)
                ##print ids
                ha=f[1]
                ha=float(ha)
                haint=float(ha)
                haint=haint/10000+1
                ##print haint
                txtreclass.write(`ids`+' = '+`haint`+'\n')
                
txtreclass.close()

# Reclassify patch ID map to generate a Patch Area map (in hectares)
grass.run_command('r.reclass', input='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump', output='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA',
                  rules = txtsaida, overwrite = True)

# Map of patches < 10 ha of AF from MapBiomas 2016
expression = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha = if(MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA <= 10, 1, null())'
grass.mapcalc(expression, overwrite = True)

# Map of patches < 10 ha of AF from MapBiomas 2016 that do not overlap with SOSMA patches
expression2 = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha_nonSOSMA = if(isnull(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast), MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha, null())'
grass.mapcalc(expression2, overwrite = True)


# 4. Preparing the final vegetation map

# 4.1 Mosaic of forest fragmentos: FBDS for SP, SOSMA 2015 for RJ, SOSMA 2014 + MapBiomas 2016 (<10ha) for the rest of AF, 
#     dense forest of Cerrado, Caatinga, and Pantanal for the remaining gaps

# Maps to mosaic, in this order of prevalence
maps = ['floresta_FBDS_albers_final1_HABMAT_tif_only_SP', 'atlas_sosma_rj_2014_2015_albers_sad69_rast_HABMAT_only_RJ',
        'atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast', 'mata_atlantica_remanescentes_sad69_albers_2005_rast',
        'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha_nonSOSMA']

# Region of study
grass.run_command('g.region', n=3207580, s=-215690, w=207880, e=2738800, res = 30, flags = 'p') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# Mask for the region of study - extended limit of the AF
grass.run_command('r.mask', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp')

# Combine maps
grass.run_command('r.patch', input = maps, output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha', overwrite = True)

# 4.2 Clean: Set as null() areas that are roads, water bodies, tree plantations or urban areas
expression3 = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha_clean = if(mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha >= 1 &&& \
isnull(mancha_urbana_composicao_ibge_SOS_limiteMAestendido_albers_sad69_rast) &&& \
isnull(dnit_pavimentada_albers_sad69_rast) &&& isnull(gfw_tree_plantations_albers_sad69_rast) &&& \
isnull(geoft_bho_massa_dagua_albers_sad69_rast), mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha, null())'
grass.mapcalc(expression3, overwrite = True)

grass.run_command('r.mask', flags = 'r')


# 5. Export final vegetation map
folder = r'G:\regenerabilidade_MA\02_saidas'
os.chdir(folder)
grass.run_command('r.out.gdal', input = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha_clean', output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha_clean.tif')
# With compression
grass.run_command('r.out.gdal', input = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha_clean', output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_sos2005_mapbiomas2016_10ha_clean_compress.tif', createopt="COMPRESS=DEFLATE")


###--------------------------------------------------------------------###


###--------------------------------------------------------------------###
## Processing and combining maps - Option 1 (considering only patches < 10ha from AF map of MapBiomas 2016)

# Region of study
grass.run_command('g.region', n=3207580, s=-215690, w=207880, e=2738800, res = 30, flags = 'p') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# 1. Fill the Sao Paulo State with forest fragmentos from FBDS, degrading its resolution to 30m
grass.run_command('r.mask', vector = 'limite_SP_albers_sad69_shp') # Mask for SP
grass.mapcalc('floresta_FBDS_albers_final1_HABMAT_tif_only_SP = floresta_FBDS_albers_final1_HABMAT_tif', overwrite = True) # Filling SP with a binary map of forest patches
grass.run_command('r.mask', flags = 'r') # Remove mask


# 2. Fill the Rio de Janeiro State with forest fragmentos from SOSMA 2015
grass.run_command('r.mask', vector = 'limite_RJ_albers_sad69_shp') # Mask for RJ
grass.mapcalc('atlas_sosma_rj_2014_2015_albers_sad69_rast_habmat = if(atlas_sosma_rj_2014_2015_albers_sad69_rast == 1 &&& !isnull(atlas_sosma_rj_2014_2015_albers_sad69_rast), 1, 0)', overwrite = True) # Transforming the map of forest patches to a binary class map
grass.run_command('r.mask', flags = 'r') # Remove mask

grass.run_command('r.mask', vector = 'limite_RJ_albers_sad69_shp')
grass.mapcalc('atlas_sosma_rj_2014_2015_albers_sad69_rast_HABMAT_only_RJ = atlas_sosma_rj_2014_2015_albers_sad69_rast_habmat', overwrite = True)
grass.run_command('r.mask', flags = 'r')


# 3. Combine forest patches from SOSMA 2014 with forest patches < 10 ha from the AF from Mapbiomas 2016 (considering all classes of natural forest - 1 to 8)

# 3.1 Reclassify AF map from MapBiomas 2016 - considering all classes of natural forest - 1 to 8
reclass_legend = ['1 thru 8 = 1 forest', 
                  '*        = NULL']

# Create txt file for reclassification
folder = r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas'
file_name = 'reclass_mapbiomas_vegetation_MA.txt'
os.chdir(folder)
reclass_file = open(file_name, 'w')
for i in reclass_legend:
    reclass_file.write(i)
    reclass_file.write('\n')
    
reclass_file.close()

# Reclassify
grass.run_command('r.reclass', input='MATAATLANTICA_colecao2_2016_albers_SAD69_tif', output='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8',
                  rules = file_name, overwrite = True)

# 3.2 Select only patches < 10ha from AF (MapBiomas 2016)

#grass.run_command('r.reclass.area', input = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8', output = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_less_10ha', mode = 'lesser', value = 10, overwrite = True)
# The above did not work - let's do it manually

# Clump areas functionally connected to generate a Patch ID map
grass.run_command('r.clump', input = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8', output = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump')

# Write file with patch area for reclassification, using r.stats
x=grass.read_command('r.stats',flags='a',input='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump').replace('\r','')
y=x.split('\n')
os.chdir(r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas')
txtsaida='reclass_area_less_10ha_mapbiomas.txt'
txtreclass=open(txtsaida, 'w')
#txtreclass.write('COD'+','+'HA\n')
if len(y)!=0:
    for i in y:
        if i !='':
            ##print i
            f=i.split(' ')
            if '*' in f :
                break
            else:
                ##print f
                ids=f[0]
                ids=int(ids)
                ##print ids
                ha=f[1]
                ha=float(ha)
                haint=float(ha)
                haint=haint/10000+1
                ##print haint
                txtreclass.write(`ids`+' = '+`haint`+'\n')
                
txtreclass.close()

# Reclassify patch ID map to generate a Patch Area map (in hectares)
grass.run_command('r.reclass', input='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump', output='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA',
                  rules = txtsaida, overwrite = True)

# Map of patches < 10 ha of AF from MapBiomas 2016
expression = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha = if(MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA <= 10, 1, null())'
grass.mapcalc(expression, overwrite = True)

# Map of patches < 10 ha of AF from MapBiomas 2016 that do not overlap with SOSMA patches
expression2 = 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha_nonSOSMA = if(isnull(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast), MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha, null())'
grass.mapcalc(expression2, overwrite = True)


# 3.3 Select only dense forests from Cerrado, Caatinga, and Pantanal

# Consider only class 3 - dense forest
reclass_legend = ['3 = 1 forest', 
                  '* = NULL']

#  Create txt file for reclassification
folder = r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas'
file_name = 'reclass_mapbiomas_vegetation_CE.txt'
os.chdir(folder)
reclass_file = open(file_name, 'w')
for i in reclass_legend:
    reclass_file.write(i)
    reclass_file.write('\n')
    
reclass_file.close()

# Reclassify Cerrado, Caatinga, and Pantanal
grass.run_command('r.reclass', input='CERRADO_colecao2_2016_albers_SAD69_tif', output='CERRADO_colecao2_2016_albers_SAD69_vegetation_3',
                  rules = file_name, overwrite = True)

grass.run_command('r.reclass', input='CAATINGA_colecao2_2016_albers_SAD69_tif', output='CAATINGA_colecao2_2016_albers_SAD69_vegetation_3',
                  rules = file_name, overwrite = True)

grass.run_command('r.reclass', input='PANTANAL_colecao2_2016_albers_SAD69_tif', output='PANTANAL_colecao2_2016_albers_SAD69_vegetation_3',
                  rules = file_name, overwrite = True)


# 4. Preparing the final vegetation map

# 4.1 Mosaic of forest fragmentos: FBDS for SP, SOSMA 2015 for RJ, SOSMA 2014 + MapBiomas 2016 (<10ha) for the rest of AF, 
#     dense forest of Cerrado, Caatinga, and Pantanal for the remaining gaps

# Maps to mosaic, in this order of prevalence
maps = ['floresta_FBDS_albers_final1_HABMAT_tif_only_SP', 'atlas_sosma_rj_2014_2015_albers_sad69_rast_HABMAT_only_RJ',
        'atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast', 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_1a8_clump_areaHA_less10ha_nonSOSMA',
        'CERRADO_colecao2_2016_albers_SAD69_vegetation_3', 'CAATINGA_colecao2_2016_albers_SAD69_vegetation_3',
        'PANTANAL_colecao2_2016_albers_SAD69_vegetation_3']

# Region of study
grass.run_command('g.region', n=3207580, s=-215690, w=207880, e=2738800, res = 30, flags = 'p') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# Mask for the region of study - extended limit of the AF
grass.run_command('r.mask', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp')

# Combine maps
grass.run_command('r.patch', input = maps, output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016', overwrite = True)

# 4.2 Clean: Set as null() areas that are roads, water bodies, tree plantations or urban areas
expression3 = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_clean = if(mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016 >= 1 &&& \
isnull(mancha_urbana_composicao_ibge_SOS_limiteMAestendido_albers_sad69_rast) &&& \
isnull(dnit_pavimentada_albers_sad69_rast) &&& isnull(gfw_tree_plantations_albers_sad69_rast) &&& \
isnull(geoft_bho_massa_dagua_albers_sad69_rast), mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016, null())'
grass.mapcalc(expression3, overwrite = True)

grass.run_command('r.mask', flags = 'r')


# 5. Export final vegetation map
folder = r'G:\regenerabilidade_MA\02_saidas'
os.chdir(folder)
grass.run_command('r.out.gdal', input = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_clean', output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_clean.tif')
###--------------------------------------------------------------------###


###--------------------------------------------------------------------###
## Processing and combining maps - Option 2 (considering all patches of dense forest (class 3) from AF map of MapBiomas 2016)

# Region of study
grass.run_command('g.region', n=3207580, s=-215690, w=207880, e=2738800, res = 30, flags = 'p') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# 1. Fill the Sao Paulo State with forest fragmentos from FBDS, degrading its resolution to 30m
# The same as above

# 2. Fill the Rio de Janeiro State with forest fragmentos from SOSMA 2015
# The same as above

# 3. Combine forest patches from SOSMA 2014 with dense forest patches (class 3) of all size classes from the AF from Mapbiomas 2016

# 3.1 Reclassify AF map from MapBiomas 2016 - considering only class 3 (dense forest)
reclass_legend = ['3 = 1 forest', 
                  '* = NULL']

# Create txt file for reclassification
folder = r'G:\regenerabilidade_MA\01_bases\raster\mapbiomas'
file_name = 'reclass_mapbiomas_vegetation_MA_class3.txt'
os.chdir(folder)
reclass_file = open(file_name, 'w')
for i in reclass_legend:
    reclass_file.write(i)
    reclass_file.write('\n')
    
reclass_file.close()

# Reclassify
grass.run_command('r.reclass', input='MATAATLANTICA_colecao2_2016_albers_SAD69_tif', output='MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_3',
                  rules = file_name, overwrite = True)

# 3.2 Select only patches < 10ha from AF (MapBiomas 2016)
# Not necessary

# 3.3 Select only dense forests from Cerrado, Caatinga, and Pantanal

# The same as above


# 4. Preparing the final vegetation map

# 4.1 Mosaic of forest fragmentos: FBDS for SP, SOSMA 2015 for RJ, SOSMA 2014 + MapBiomas 2016 (all dense forest fragments) for the rest of AF, 
#     dense forest of Cerrado, Caatinga, and Pantanal for the remaining gaps

# Maps to mosaic, in this order of prevalence
maps2 = ['floresta_FBDS_albers_final1_HABMAT_tif_only_SP', 'atlas_sosma_rj_2014_2015_albers_sad69_rast_HABMAT_only_RJ',
        'atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast', 'MATAATLANTICA_colecao2_2016_albers_SAD69_vegetation_3',
        'CERRADO_colecao2_2016_albers_SAD69_vegetation_3', 'CAATINGA_colecao2_2016_albers_SAD69_vegetation_3',
        'PANTANAL_colecao2_2016_albers_SAD69_vegetation_3']

# Region of study
grass.run_command('g.region', n=3207580, s=-215690, w=207880, e=2738800, res = 30, flags = 'p') # nao da a resolucao exata 30m - vamos adicionar um pouco na extensao

# Mask for the region of study - extended limit of the AF
grass.run_command('r.mask', vector = 'limite_leima_ribeiroetal2009_albers_sad69_dissolve_shp')

# Combine maps
grass.run_command('r.patch', input = maps2, output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest', overwrite = True)

# 4.2 Clean: Set as null() areas that are roads, water bodies, tree plantations or urban areas
expression3 = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest_clean = if(mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest >= 1 &&& \
isnull(mancha_urbana_composicao_ibge_SOS_limiteMAestendido_albers_sad69_rast) &&& \
isnull(dnit_pavimentada_albers_sad69_rast) &&& isnull(gfw_tree_plantations_albers_sad69_rast) &&& \
isnull(geoft_bho_massa_dagua_albers_sad69_rast), mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest, null())'
grass.mapcalc(expression3, overwrite = True)

grass.run_command('r.mask', flags = 'r')


# 5. Export final vegetation map
folder = r'G:\regenerabilidade_MA\02_saidas'
os.chdir(folder)
grass.run_command('r.out.gdal', input = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest_clean', output = 'mosaic_vegetation_fbdsSP2014_sosRJ2015_sos2014_mapbiomas2016_alldenseforest_clean.tif')



###############################

# Comparing AF patches between 2014 and 2005

expression01 = 'difference_SOSMA2014_SOSMA2005 = if(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast == 1 &&& mata_atlantica_remanescentes_sad69_albers_2005_rast == 1, 0, \
if(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast == 1 &&& isnull(mata_atlantica_remanescentes_sad69_albers_2005_rast), 1, \
if(isnull(atlas_ma_sos_ma_2014_mata_restinga_mangue_albers_sad69_rast) &&& mata_atlantica_remanescentes_sad69_albers_2005_rast == 1, -1, null())))'
grass.mapcalc(expression01, overwrite = True)