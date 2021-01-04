-#Python workflow for converting depths below ground surface of geologic units
#to elevations above sea level
#Developed by Martin Palkovic, Geologist at Colorado Geological Survey
#Colorado School of Mines

#Step 1: Import system modules
#-----------------------------
import arcpy, os
from arcpy import env
from arcpy.sa import *

#Step 2: Define the workspaces
#-----------------------------
env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
env.workspaceBM = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Basemaps.gdb'

#Define local variables
#----------------------
inFeatures = os.path.join(env.workspace, 'Tops_61620')
inRaster = os.path.join(env.workspaceBM, 'LaPlata10mDEM_ft')
intValues = 'INTERPOLATE'
addAtt = 'VALUE_ONLY'
fieldType = 'DOUBLE'
fieldList = [field.name for field in arcpy.ListFields(inFeatures)]
del fieldList [0:5] #Removes the first four items in the list. We won't be iterating
#over these, so this will speed up our processing time. Note that this deletes
#up to, but NOT including, index #5 (i.e GALLUP_COGCC)

#Next, we're going to add a point value field in the dataset for the DEM raster
#value at each DWR well. Example syntax for ExtractValuesToPoints:
#ExtractValuesToPoints (input features, input raster, output point features, interpolate values, add attributes)
#"INTERPOLATE" and "VALUE ONLY" are good 'go to' defaults)
#---------------------------------------------------------
Contour ('LP10mFT', env.workspace + '\\Ten_m_ftContours', 10) #Doing this to QC the extract by points below

ExtractValuesToPoints (inFeatures, inRaster, outPoints, intValues, addAtt)

fieldList = [field.name for field in arcpy.ListFields (inFeatures)]
del fieldList[0:5]
fieldType = 'DOUBLE'
#print (fieldList)

for field in fieldList:
    arcpy.AddField_management (inFeatures, field[:-5] + 'Elev_ftASL', fieldType)
    
fieldList = [field.name for field in arcpy.ListFields(inFeatures)] #Redo the list
#to make sure our index numbers match up with the conditional logic below

for field in fieldList:
    print (field, fieldList.index(field))

#The list for this example looks like this:
#(u'OBJECTID', 0)
#(u'UWI_API', 1)
#(u'DATUM', 2)
#(u'LAT', 3)
#(u'LON', 4)
#(u'GALLUP_COGCC', 5)
#(u'POINT_LOOKOUT_COGCC', 6)
#(u'MENEFEE_COGCC', 7)
#(u'PICTURED_CLIFFS_COGCC', 8)
#(u'OJO_ALAMO_COGCC', 9)
#(u'ANIMAS_COGCC', 10)
#(u'SANASTEE_COGCC', 11)
#(u'LEWIS_COGCC', 12)
#(u'FRUITLAND_COAL_COGCC', 13)
#(u'CLIFF_HOUSE_COGCC', 14)
#(u'KIRTLAND_COGCC', 15)
#(u'ENTRADA_COGCC', 16)
#(u'MANCOS_COGCC', 17)
#(u'MORRISON_COGCC', 18)
#(u'MESAVERDE_COGCC', 19)
#(u'CHINLE_COGCC', 20)
#(u'DAKOTA_COGCC', 21)
#(u'FRUITLAND_COGCC', 22)
#(u'Shape', 23)
#(u'FARMINGTON_COGCC', 24)
#(u'RASTERVALU', 25)
#(u'GALLUP_Elev_ftASL', 26)
#(u'POINT_LOOKOUT_Elev_ftASL', 27)
#(u'MENEFEE_Elev_ftASL', 28)
#(u'PICTURED_CLIFFS_Elev_ftASL', 29)
#(u'OJO_ALAMO_Elev_ftASL', 30)
#(u'ANIMAS_Elev_ftASL', 31)
#(u'SANASTEE_Elev_ftASL', 32)
#(u'LEWIS_Elev_ftASL', 33)
#(u'FRUITLAND_COAL_Elev_ftASL', 34)
#(u'CLIFF_HOUSE_Elev_ftASL', 35)
#(u'KIRTLAND_Elev_ftASL', 36)
#(u'ENTRADA_Elev_ftASL', 37)
#(u'MANCOS_Elev_ftASL', 38)
#(u'MORRISON_Elev_ftASL', 39)
#(u'MESAVERDE_Elev_ftASL', 40)
#(u'CHINLE_Elev_ftASL', 41)
#(u'DAKOTA_Elev_ftASL', 42)
#(u'FRUITLAND_Elev_ftASL', 43)
#(u'FARMINGTON_Elev_ftASL', 44)

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [5] == 0):
            row [5] = None
        if (row [5] != None): #if Gallup Sandstone is not equal to zero
            row [26] = row [25] - row [5] #Gallup Elev = DEM value - Gallup top
        else:
            row [26] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [6] == 0):
            row [6] = None
        if (row [6] != None): #Point Lookout Sandstone
            row [27] = row [25] - row [6] 
        else:
            row [27] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [7] == 0):
            row [7] = None
        if (row [7] != None): #Menefee Formation
            row [28] = row [25] - row [7] 
        else:
            row [28] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [8] == 0):
            row [8] = None
        if (row [8] != None): #Pictured Cliffs Formation
            row [29] = row [25] - row [8] 
        else:
            row [29] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [9] == 0):
            row [9] = None
        if (row [9] != None): #Ojo Alamo Sandstone
            row [30] = row [25] - row [9]
        else:
            row [30] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [10] == 0):
            row [10] = None
        if (row [10] != None): #Animas Formation
            row [31] = row [25] - row [10]
        else:
            row [31] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [11] == 0):
            row [11] = None
        if (row [11] != None): #Sanastee Formation, string values
            row [32] = row [25] - float(row [11]) 
        else:
            row [32] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [12] == 0):
            row [12] = None
        if (row [12] != None): #Lewis Shale
            row [33] = row [25] - row [12] 
        else:
            row [33] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [13] == 0):
            row [13] = None
        if (row [13] != None): #Fruitland Coal
            row [34] = row [25] - row [13]
        else:
            row [34] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [14] == 0):
            row [14] = None
        if (row [14] != None): #Cliff House Sandstone
            row [35] = row [25] - row [14] 
        else:
            row [35] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [15] == 0):
            row [15] = None
        if (row [15] != None): #Kirtland Shale
            row [36] = row [25] - row [15]
        else:
            row [36] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [16] == 0):
            row [16] = None
        if (row [16] != None): #Entrada Sandstone, string values
            row [37] = row [25] - float(row [16])
        else:
            row [37] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [17] == 0):
            row [17] = None
        if (row [17] != None): #Mancos Shale
            row [38] = row [25] - row [17]
        else:
            row [38] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [18] == 0):
            row [18] = None
        if (row [18] != None): #Morrison Formation
            row [39] = row [25] - row [18]
        else:
            row [39] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [19] == 0):
            row [19] = None
        if (row [19] != None): #Mesaverde Formation
            row [40] = row [25] - row [19]
        else:
            row [40] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [20] == 0):
            row [20] = None
        if (row [20] != None): #Chinle Formation, string values
            row [41] = row [25] - float(row [20])
        else:
            row [41] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [21] == 0):
            row [21] = None
        if (row [21] != None): #Dakota Sandstone
            row [42] = row [25] - row [21]
        else:
            row [42] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [22] == 0):
            row [22] = None
        if (row [22] != None): #Fruitland Formation
            row [43] = row [25] - row [22]
        else:
            row [43] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        if (row [24] == 0):
            row [24] = None
        if (row [24] != None): #Farmington Sandstone
            row [44] = row [25] - row [24]
        else:
            row [44] = None
        cursor.updateRow(row)
del cursor, row

#Next, I'm going to add the word 'top' to each field name:
alterList = fieldList [26:45]

for field in alterList:
    arcpy.AlterField_management(inFeatures, field, field + '_Top', field + '_Top')
    arcpy.AddField_management (inFeatures, field[:-3] + 'Bot', fieldType) 
#Id recommend putting your list in stratigraphic order after this

#Populate the bottom elevation fields
with arcpy.da.UpdateCursor (inFeatures, fieldList) as cursor:
    for row in cursor:
        row [50] = row [30] #bottom of Animas = top of the Ojo Alamo 
        row [49] = row [36] #bottom of Ojo Alamo = top of Kirtland 
        row [55] = row [43] #bottom of Kirtland = top of Fruitland
        row [62] = row [29] #bottom of Fruitland = top of Pictured Cliffs
        row [48] = row [33] #bottom of Pictured Cliffs = top of Lewis
        row [52] = row [40] #bottom of Lewis = top of  Mesaverde
        row [54] = row [28] #bottom of Cliff House = top of Menefee
        row [47] = row [27] #bottom of Menefee = top of Point Lookout
        row [46] = row [38] #bottom of Point Lookout = top of Mancos
        row [57] = row [42] #bottom of Mancos = top of Dakota
        row [61] = row [39] #bottom of Dakota = top of Morrison
        row [58] = row [37] #bottom of Morrison = top of Entrada
        cursor.updateRow(row)
del cursor, row

#Next task is to manually add some points along geologic contacts, and populate
#the geo field elevations. We will do the calcs in python

inFeatures = 'Tops'
inRaster = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Basemaps.gdb\LaPlata10mDEM_ft'
outPoints = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb\AKvalues' #Change the file name everytime you add new points along the contacts, and run ExtractValuesToPoints accordingly
intValues = 'NONE'
addAtt = 'VALUE_ONLY'

ExtractValuesToPoints (inFeatures, inRaster, outPoints, intValues, addAtt)   

env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\StructureContours.gdb'
env.overwriteOutput = True
env.addOutputsToMap = False 
inFeatures = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb\Tops'
outGA = ''
intList = [f.name for f in arcpy.ListFields(inFeatures) if f.name.endswith('Top') or f.name.endswith('Bot')]       
print (intList)

for f in intList:
    try:
        arcpy.IDW_ga (inFeatures, f, outGA, env.workspace + '\\' + f + '_IDW')
    except:
        print (arcpy.GetMessages())
        pass

#Check for bullseyes on the structure contours - delete the appropriate data
#and run again COMBINE FRUITLAND AND PICTURED CLIFFS

for f in intList:
    try:
        arcpy.IDW_ga (inFeatures, f, outGA, env.workspace + '\\' + f + '_IDW')
    except:
        print (arcpy.GetMessages())
        pass

#---------------
import arcpy, os
from arcpy import env
from arcpy.sa import *

env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\StructureContours.gdb'
env.overwriteOutput = True
outEVTP = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb\DWR_ConstructedReplaced'
rList = arcpy.ListRasters("*Bot*") #Only returns the bottom elevation structure contours
print (rList)
arcpy.CheckOutExtension('Spatial')

for r in rList:
    outP = os.path.join(outEVTP, r + '_EVTP623')
    try:
        ExtractValuesToPoints(inDWR, r, outP, 'NONE', 'VALUE_ONLY')
    except:
        ExtractValuesToPoints(inDWR, r, outP, 'INTERPOLATE', 'VALUE_ONLY')

#Not happy with the modeling results for the Fruitland Pictured Cliffs. Redo below:
    
import arcpy, os
from arcpy import env
from arcpy.sa import *

env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\StructureContours.gdb'
env.overwriteOutput = True
outEVTP = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR Wells.gdb\DWR_ConstructedReplaced'
rList = [r for r in arcpy.ListRasters() if 'FRUITLAND_PICTUREDCLIFFS' in r]
#print (rList)
        

import arcpy, os
from arcpy import env
from arcpy.sa import *

env.workspace = r'N:\PROJECT\\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb\DWR_ConstructedReplaced'

eList = [fc for fc in arcpy.ListFeatureClasses() if fc.endswith('620')]
print (eList)

for fc in eList:
    try:
        #fList = arcpy.ListFields(fc)
        #arcpy.AlterField_management(fc, 'RASTERVALU', fc[:-9], fc[:-9]) 
        fList = arcpy.ListFields(fc) #Need to do this because of the AlterField process
        jField = fList[4]
        fValue = fList[63]
        
        d = {jField:fValue for jField, fValue in arcpy.da.SearchCursor(fc, [jField.name, fValue.name])}
        
        arcpy.AddField_management(inDWR, fValue.name, fValue.type)
        with arcpy.da.UpdateCursor(inDWR, [jField.name, fValue.name]) as cursor:
            for row in cursor:
                if row[0] in d:
                    row[1] = d[row[0]]
                    cursor.updateRow(row)
                else:
                    row[1] = None
                    pass
    except:
        pass

#Some of the bottoms of units modeled higher than the tops. Lets remove that 
#data with an update cursor,it's no good

inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb\DWR_ConstructedReplaced'
fields = [f.name for f in arcpy.ListFields(inDWR) if f.name.endswith('Bot_ID')]
print (fields)

for f in fields:
    print (f, fields.index(f))

# (u'POINT_LOOKOUT_Elev_ftASL_Bot_ID', 0)
# (u'MENEFEE_Elev_ftASL_Bot_ID', 1)
# (u'LEWIS_Elev_ftASL_Bot_ID', 2)
# (u'CLIFF_HOUSE_Elev_ftASL_Bot_ID', 3)
# (u'KIRTLAND_Elev_ftASL_Bot_ID', 4)
# (u'MANCOS_Elev_ftASL_Bot_ID', 5)
# (u'MORRISON_Elev_ftASL_Bot_ID', 6)
# (u'DAKOTA_Elev_ftASL_Bot_ID', 7)
# (u'ANIMAS_OJO_Elev_ftASL_Bot_ID', 8)
# (u'FLND_PCLIFF_Elev_ftASL_Bot_ID', 9)
# (u'MESAVERDE_Elev_ftASL_Bot_ID', 10)

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[4] > row[8]: #if bot of Kirtland is greater than bot of animas:
            row[4] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[9] > row[4]: #if bot of Frtlnd Pict Ciffs is greater than bot of kirtland:
            row[9] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[2] > row[9]: #if bot of Lewis is greater than bot of Frtlnd Pict Ciffs:
            row [2] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[10] > row[2]: #if bot of Mesaverde is greater than bot of Lewis:
            row[10] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[3] > row[2]: #if bot of Cliff House is greater than bot of Lewis:
            row[3] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[1] > row[3]: #if bot of Menefee is greater than bot of Cliff House:
            row[1] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[0] > row[1]: #if bot pt lookout is greater than bot of Menefee:
            row[0] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[10] > row[0]: #if bot of Mesaaverde is greater than bot of pt lookout:
            row[10] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[5] > row[10]: #if bot of Mancos is greater than bot of Mesaverde:
            row[5] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[5] > row[3]: #if bot of Mancos is greater than bot cliff house:
            row[5] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[5] > row[1]: #if bot of Mancos is greater than bot menefee:
            row[5] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[5] > row[0]: #if bot of Mancos is greater than bot pt lookout:
            row[5] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[2] > row[4]: #if bot of lewis is greater than bot of kirtland:
            row[2] = None
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if row[6] > row[7]: #if bot of morrison is greater than bot of Dakota:
            row[6] = None
        cursor.updateRow(row)
del cursor, row

import arcpy, os
from arcpy import env
from arcpy.sa import *

inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb\DWR_ConstructedReplaced'
env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
outP = os.path.join(env.workspace, 'DWR_Elev_ftASL_ID')
inDEM = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Basemaps.gdb\LaPlata10mDEM_ft'
jField = 'Permit'
ExtractValuesToPoints(inDWR, inDEM , outP , 'NONE', 'VALUE_ONLY')
arcpy.AlterField_management(outP, 'RASTERVALU', 'DEM_Elev_ftASL', 'DEM_Elev_ftASL')
arcpy.JoinField_management(inDWR, jField, outP, jField,'DEM_Elev_ftASL')      
#Add a field named 'Aquifer'
arcpy.AddField_management (inDWR, 'Aquifer', 'Text')
        
#The next UpdateCursor calculates the elevation above sea
#level for the top of perforated casing, bottom of perforated casing, 
#and well depth. Note that you will need to add blank fields that you wish to fill
#with these calculations, either manually (fast) or with python
#-------------------------------------------------------------
import arcpy, os
from arcpy import env
env.workspace = r'N:\PROJECT\\WATER\OF-19-01 La Plata Co GW\GIS\LaPlataFmTops.gdb'
inDWR = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb\DWR_ConstructedReplaced'
fields = [f.name for f in arcpy.ListFields(inDWR) if f.name.startswith('TopPerf') or f.name.startswith('BotPerf')]
wellD = [f.name for f in arcpy.ListFields(inDWR) if 'WellDepth' in f.name]
dem = [f.name for f in arcpy.ListFields(inDWR) if 'DEM_Elev_ftASL' in f.name]
fields.extend (wellD)
fields.extend (dem)
print (fields)

for f in fields[:3]: #No field added for the last item in the list
    arcpy.AddField_management(inDWR, f + '_Elev_ftASL')

#make a new list
fields = [f.name for f in arcpy.ListFields(inDWR) if f.name.startswith('TopPerf') or f.name.startswith('BotPerf')]
wellD = [f.name for f in arcpy.ListFields(inDWR) if 'WellDepth' in f.name]
dem = [f.name for f in arcpy.ListFields(inDWR) if 'DEM_Elev_ftASL' in f.name]
fields.extend (wellD)
fields.extend (dem)
print (fields)

for field in fields:
    print (field, fields.index(field))

# (u'TopPerfCas', 0)
# (u'BotPerfCas', 1)
# (u'TopPerfCas_Elev_ftASL', 2)
# (u'BotPerfCas_Elev_ftASL', 3)
# (u'WellDepth', 4)
# (u'WellDepth_Elev_ftASL', 5)
# (u'DEM_Elev_ftASL', 6)
    
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        for row in cursor:
            if (row[0] != 0): #if top perf casing doesn't equal 0
                row[2] = row[6] - row[0] 
            else:
                row[2] = None
            cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        for row in cursor:
            if (row[1] != 0): #if bot perf casing doesn't equal 0
                row[3] = row[6] - row[1]
            else:
                row[3] = None
            cursor.updateRow(row)
del cursor, row
                
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        for row in cursor:
            if (row[4] != 0): #if well depth doesn't equal 0
                row[5] = row[6] - row[4]
            else:
                row[5] = None
            cursor.updateRow(row)
del cursor, row      
        
#Now, a long line of if-elif statements to populate that aquifer field. These lines
#will check the well perforations, and then well depths if no perforation data exists,
#against the values in the DWR file for each geologic unit.
#----------------------------------------------------------
import arcpy, os
from arcpy import env
from arcpy.sa import *
env.workspace = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\DWR_Wells.gdb'
inDWR = 'DWR_ConstructedReplaced'
fields = [f.name for f in arcpy.ListFields(inDWR) if f.name.endswith('Bot_ID')]
wellD = [f.name for f in arcpy.ListFields(inDWR) if f.name.endswith('ASL')]
aqDWR = [f.name for f in arcpy.ListFields(inDWR) if f.name.startswith('Aq')] #This grabs both the DWR and CGS aquifer fields
conf = [f.name for f in arcpy.ListFields(inDWR) if f.name.startswith('Conf')]
coords = [f.name for f in arcpy.ListFields(inDWR) if f.name.endswith('Deg')]
#I then added a field == DEM elev minus 100 ft...
dem = [f.name for f in arcpy.ListFields(inDWR) if 'DEMMinus100' in f.name]
fields.extend(aqDWR)
fields.extend(wellD)
fields.extend(conf)
fields.extend(coords)
fields.extend(dem)
#print (fields) #List is looking good so I commented this out

for field in fields:
    print (field, fields.index(field))        

#This is what the list looks like
# (u'POINT_LOOKOUT_Elev_ftASL_Bot_ID', 0)
# (u'MENEFEE_Elev_ftASL_Bot_ID', 1)
# (u'LEWIS_Elev_ftASL_Bot_ID', 2)
# (u'CLIFF_HOUSE_Elev_ftASL_Bot_ID', 3)
# (u'KIRTLAND_Elev_ftASL_Bot_ID', 4)
# (u'MANCOS_Elev_ftASL_Bot_ID', 5)
# (u'MORRISON_Elev_ftASL_Bot_ID', 6)
# (u'DAKOTA_Elev_ftASL_Bot_ID', 7)
# (u'ANIMAS_OJO_Elev_ftASL_Bot_ID', 8)
# (u'FLND_PCLIFF_Elev_ftASL_Bot_ID', 9)
# (u'MESAVERDE_Elev_ftASL_Bot_ID', 10)
# (u'Aquifer1', 11)
# (u'Aquifer2', 12)
# (u'Aquifer', 13)
# (u'DEM_Elev_ftASL', 14)
# (u'TopPerfCas_Elev_ftASL', 15)
# (u'BotPerfCas_Elev_ftASL', 16)
# (u'WellDepth_Elev_ftASL', 17)
# (u'Confidence', 18)
# (u'LatDecDeg', 19)
# (u'LongDecDeg', 20)
# (u'DEMMinus100_Elev_ftASL1', 21)

""" Step 1: If a well lies within a hydro unit in the SW corner of the study area (Area specified by Lesley Sebol), and its 
perforations are less than 200 ft deep, the well is within that aquifer. If there
are no perforations, use well depths instead. These wells are high confidence. 
I'm using these criteria on the following units in the SW corner:

    -Eolian Deposits
    -Mass Wasting Deposits
    -Terrace Alluvium
    -Older Gravels
    

**I'm excluding alluvial aquifer and alluvium-colluvium, undivided, 
because 200 ft is far too thick for alluvial deposits in this area. Also, there
are no sinter-tufa deposits or glacial deposits in this area, so Im excluding those
as well.

Step 2: If a well lies within a hydro unit and it's perforations are less than 100 ft deep,
That well is within that aquifer. If there are no perforations, use well depth instead.
These wells are high confidence.

Step 3: After we've gone through all surficial geology, then check the blank aquifer
fields against the subsurface geology

Step 4: At this point, we have 8473/11998 wells with an aquifer field, or 3525 wells without 
an aquifer field. For this next step, I'm going to focus on all of the wells that have a <Null> aquifer field, and either don't have a depth 
or have 0 for their well depth. If a well meets those criteria and is within a polygon, it will become == that aquifer.
*everything adhering to these rules is 'low' confidence

Step 5:Now we've got 10574/11998 aquifers, or we still need aquifer values for 1419 of the wells.
This code filled in 88.2% of the aquifer fields. I'm going to manually enter data for 49 of these
wells (all wells <= 100 ft deep)
1370 of these are greater than 100 ft deep, but commonly do not
have enough subsurface bottoms data to have an aquifer populated based on the code. We'll call these 'BEDROCK AQUIFER
with a low confidence value. This accounts for 11.4% of the wells (pretty good, IMO!)

*some of these wells don't lie within polygon boundaries. See FID 11166, 11167, 5961, 6975, 6982. 
I manually entered the closest polygon as the aquifer for these

*Many of these 49 wells are just over 100 ft in depth - i.e 100.1, 100.2 etc. 
So, they did not meet our criteria for surficial classification (i.e if a well is <= 100 ft deep and overlies this polygon, it is in that aquifer)
i.e some of these wells are 100.1, 100.2, etc feet deep, don't have enough subsurface data for classification, and cant be classified by the code above'
I started going through these manually to classify them as the surficial unit 
they are within, but realized they don't meet our criteria! I thought these were 
errors and wasn't sure why the code didn't pick them up. Floating point numbers, am I rite!!!!?
"""

#Quaternary Units
#----------------
af = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\af_hydro' #artificial fill
qa = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qa_hydro' #alluvial aquifer
qac = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qac_hydro' #alluvium-colluvium, undivided
qe = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qe_hydro' #eolian deposits
qmw = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qmw_hydro' #mass wasting deposits
qta = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qta_hydro' #terrace alluvium
qgo = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qgo_hydro' #older gravels
qtu = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qtu_hydro' #sinter-tufa deposits
qgds = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgds_hydro' #glacial dammed sediment
qgmk = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgmk_hydro' #glacial moraines and kames
qgd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgd_hydro' #glacial drift


arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qe)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #in the SW corner of the study area, Quaternary deposits are thicker. We'll use 200 ft for our cutoff here (see the lat/lon coordinates a few lines below)
    for row in cursor:
        if (row[19] < 37.35 and row[19] > 37 and row[20] > -108.35 and row[20] <-108.02): #The area that Lesley specified where the Surficial aquifer is <= 200 ft BGS (SW study area)
            if (row[13] == None): #if Aquifer_CGS is <Null>
                if (row[16] != None): #if bottom of perforated casing has a value:
                    if (row[14] - row[16] <= 200): #if the bottom of perforated casing is <= 200 ft below ground surface:
                        row[13] = 'EOLIAN DEPOSITS'
                        if (row[18] == None): #if confidence is <Null>
                            row[18] = 'high'
                elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                    if (row[17] != None): #if well depth has a value:
                        if (row[14] - row[17] <= 200): #if DEM_Elev - Well Depth is <= 200:
                            row[13] = 'EOLIAN DEPOSITS'
                            if (row[18] == None): #if there is not already a confidence value listed:
                                row[18] = 'high'                  
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qmw)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #in the SW corner of the study area, Quaternary deposits are thicker. We'll use 200 ft for our cutoff here (see the lat/lon coordinates a few lines below)
    for row in cursor:
        if (row[19] < 37.35 and row[19] > 37 and row[20] > -108.35 and row[20] <-108.02): #The area that Lesley specified where the Surficial aquifer is <= 200 ft BGS (SW study area)
            if (row[13] == None): #if Aquifer_CGS is <Null>
                if (row[16] != None): #if bottom of perforated casing has a value:
                    if (row[14] - row[16] <= 200): #if the bottom of perforated casing is <= 200 ft below ground surface:
                        row[13] = 'MASS WASTING DEPOSITS'
                        if (row[18] == None): #if confidence is <Null>
                            row[18] = 'high'
                elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                    if (row[17] != None): #if well depth has a value:
                        if (row[14] - row[17] <= 200): #if DEM_Elev - Well Depth is <= 200:
                            row[13] = 'MASS WASTING DEPOSITS'
                            if (row[18] == None): #if there is not already a confidence value listed:
                                row[18] = 'high'                  
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qta)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #in the SW corner of the study area, Quaternary deposits are thicker. We'll use 200 ft for our cutoff here (see the lat/lon coordinates a few lines below)
    for row in cursor:
        if (row[19] < 37.35 and row[19] > 37 and row[20] > -108.35 and row[20] <-108.02): #The area that Lesley specified where the Surficial aquifer is <= 200 ft BGS (SW study area)
            if (row[13] == None): #if Aquifer_CGS is <Null>
                if (row[16] != None): #if bottom of perforated casing has a value:
                    if (row[14] - row[16] <= 200): #if the bottom of perforated casing is <= 200 ft below ground surface:
                        row[13] = 'TERRACE ALLUVIUM'
                        if (row[18] == None): #if confidence is <Null>:
                            row[18] = 'high'
                elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                    if (row[17] != None): #if well depth has a value:
                        if (row[14] - row[17] <= 200): #if DEM_Elev - Well Depth is <= 200:
                            row[13] = 'TERRACE ALLUVIUM'
                            if (row[18] == None): #if there is not already a confidence value listed:
                                row[18] = 'high'                  
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgo)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #in the SW corner of the study area, Quaternary deposits are thicker. We'll use 200 ft for our cutoff here (see the lat/lon coordinates a few lines below)
    for row in cursor:
        if (row[19] < 37.35 and row[19] > 37 and row[20] > -108.35 and row[20] <-108.02): #The area that Lesley specified where the Surficial aquifer is <= 200 ft BGS (SW study area)
            if (row[13] == None): #if Aquifer_CGS is <Null>
                if (row[16] != None): #if bottom of perforated casing has a value:
                    if (row[14] - row[16] <= 200): #if the bottom of perforated casing is <= 200 ft below ground surface:
                        row[13] = 'OLDER GRAVELS'
                        if (row[18] == None): #if confidence is <Null>:
                            row[18] = 'high'
                elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                    if (row[17] != None): #if well depth has a value:
                        if (row[14] - row[17] <= 200): #if DEM_Elev - Well Depth is <= 200:
                            row[13] = 'OLDER GRAVELS'
                            if (row[18] == None): #if there is not already a confidence value listed:
                                row[18] = 'high'                  
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

"""Step 2: If a well does not already have an aquifer value (i.e not in the SW corner of the study area), 
lies within a hydro unit and it's perforations are less than 100 ft deep, that well is within that aquifer. 
If there are no perforations, use well depth instead. These wells are high confidence. """

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', af)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is <= 100 ft below ground surface:
                    row[13] = 'ANTHROPOGENIC DEPOSITS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'ANTHROPOGENIC DEPOSITS'
                        if (row[18] == None): #if there is not already a confidence value listed:
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')           

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qa)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'ALLUVIAL AQUIFER'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'ALLUVIAL AQUIFER'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qac)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'ALLUVIUM-COLLUVIUM, UNDIVIDED'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'ALLUVIUM-COLLUVIUM, UNDIVIDED'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qe)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'EOLIAN DEPOSITS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'EOLIAN DEPOSITS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qmw)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'MASS WASTING DEPOSITS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'MASS WASTING DEPOSITS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qta)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'TERRACE ALLUVIUM'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'TERRACE ALLUVIUM'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgo)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'OLDER GRAVELS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'OLDER GRAVELS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qtu)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'SINTER-TUFA DEPOSITS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'SINTER-TUFA DEPOSITS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qtu)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'SINTER-TUFA DEPOSITS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'SINTER-TUFA DEPOSITS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

#No wells within the Bridgetimber gravel, so I am skipping it.

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgds)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'GLACIAL DAMMED SEDIMENTS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'GLACIAL DAMMED SEDIMENTS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgmk)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'GLACIAL MORAINES AND KAMES'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'GLACIAL MORAINES AND KAMES'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgd)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'GLACIAL DRIFT'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None): #if well depth has a value:
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'GLACIAL DRIFT'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

#Bedrock Units
#-------------
psjn = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Paleogene\PEsn_outcrop' #san jose and nacimiento aquifer
peki = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Paleogene\PEKi_outcrop' #volcanic intrusives
ka = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\PEKa_outcrop' #animas formation
kk = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kk_outcrop' #kirtland shale
kfp = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kfp_outcrop' #fruitland-pictured cliffs formation
kl = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kl_outcrop' #lewis shale
kmv = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kmv_outcrop' #mesaverde formation
km = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Km_outcrop' #mancos shale
kd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kdb_outcrop' #dakota sandstone/burro canyon, undivided
jmj = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Jmj_outcrop' #morrison/junction creek
jw = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Jw_outcrop' #wannakah formation
je = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Je_outcrop' #entrada formation
trd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Triassic\trd_outcrop' #dolores formation
pc = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Permian\Pc_outcrop' #cutler formation
pphm = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Pennsylvanian\PPhm_outcrop' #hermosa group
mdli = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Middle_Paleozoics\MDli_outcrop' #middle paleozoic aquifer
pcig = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Precambrian\pC_igneous_outcrop' #igneous rock
pcm = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Precambrian\pC_meta_outcrop' #metamorphic rock

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', psjn)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'SAN JOSE-NACIMIENTO'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'SAN JOSE-NACIMIENTO'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', peki)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'VOLCANIC INTRUSIVES'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'VOLCANIC INTRUSIVES'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', ka)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'ANIMAS-OJO ALAMO'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'ANIMAS-OJO ALAMO'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kk)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'KIRTLAND SHALE'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'KIRTLAND SHALE'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kfp)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'FRUITLAND-PICTURED CLIFFS'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'FRUITLAND-PICTURED CLIFFS'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kl)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'LEWIS SHALE'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'LEWIS SHALE'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kmv)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'MESAVERDE FORMATION'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'MESAVERDE FORMATION'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', km)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'MANCOS SHALE'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'MANCOS SHALE'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kd)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'DAKOTA SANDSTONE'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'DAKOTA SANDSTONE'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', jmj)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'MORRISON-JUNCTION CREEK'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'MORRISON-JUNCTION CREEK'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', jw)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'WANNAKAH FORMATION'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'WANNAKAH FORMATION'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', je)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'ENTRADA SANDSTONE'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'ENTRADA SANDSTONE'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', trd)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'DOLORES FORMATION'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'DOLORES FORMATION'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pc)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'CUTLER FORMATION'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'CUTLER FORMATION'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pphm)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'HERMOSA GROUP'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'HERMOSA GROUP'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', mdli)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'MIDDLE PALEOZOIC AQUIFER'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'MIDDLE PALEOZOIC AQUIFER'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pcig)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'IGNEOUS ROCK'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'IGNEOUS ROCK'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pcm)
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if 'Aquifer' is <Null>:
            if (row[16] != None): #if bottom of perforated casing has an elevation value:
                if (row[14] - row[16] <= 100): #if the bottom of the perforated casing is < 100 ft below ground surface:
                    row[13] = 'METAMORPHIC ROCK'
                    if (row[18] == None): #if the confidence value is <Null>:
                        row[18] = 'high'
            elif (row[16] == None): #if bottom of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[14] - row[17] <= 100): #if DEM_Elev - Well Depth is <= 100:
                        row[13] = 'METAMORPHIC ROCK'
                        if (row[18] == None):
                            row[18] = 'high'
        cursor.updateRow(row)
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')


"""Step 3: After we've gone through all surficial geology, then check the blank aquifer
fields against the subsurface geology """


# with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
#     for row in cursor:
#         if (row[19] == None): #if well depth == <Null>
#             row[15] = None #Aquifer = <Null>
#         cursor.updateRow(row)
# del cursor, row

#Select all wells within the alluvial polygons
# arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qa)
# with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
#     for row in cursor:
#         if (row[15] == None): #if Aquifer is <Null>:
#             if (row[16] != None and row[19] != None): #If DEM_Elev does not equal <Null> and well depth does not equal <Null>"
#                 if (row[16] - row[19] < 50): #if DEM_Elev - Well Depth is < 50 ft:
#                     row[15] = 'QUATERNARY ALLUVIUM'
#         cursor.updateRow(row)
# del cursor, row
# arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

# with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #Surficial Aquifer
#     for row in cursor:
#         if (row[15] == None):
#             if (row[18] != None):
#                 if (row[18] >= row[20]):
#                     row[15] = 'SURFICIAL AQUIFER'
#             elif(row[18] == None): 
#                 if (row[19] >= row[20]):
#                     row[15] = 'SURFICIAL AQUIFER'
#         cursor.updateRow(row)
# del cursor, row 

#First rule: Use DWR's aquifer if they have one provided above all else
with arcpy.da.UpdateCursor(inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if Aquifer is <Null>
            if (row[11] != 'ALL UNNAMED AQUIFERS'):
                row[13] = row[11] #Our CGS aquifer field = DWR's aquifer field
                row[18] = 'high'
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #animas-ojo alamo sandstone
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[8] != None): #if Animas-Ojo Alamo bottom has a value:
                    if (row[16] < row[21] and row[16] > row[8]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the animas-ojo alamo:
                        row[13] = 'ANIMAS-OJO ALAMO'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[8] != None): #if Animas-Ojo Alamo has a value:    
                        if (row[17] < row[21] and row[17] > row[8]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'ANIMAS-OJO ALAMO'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[8] == None): #if animas-ojo alamo bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #kirtland shale
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[4] != None): #if kirtland bottom has a value:
                    if (row[16] < row[21] and row[16] > row[4]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the kirtland:
                        row[13] = 'KIRTLAND SHALE'
                        if (row[18] == None):
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[4] != None): #if kirtland bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[4]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'KIRTLAND SHALE'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[4] == None): #if kirtland bottom no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row 

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #fruitland-pictured cliffs
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[9] != None): #if fruitland-pictured cliffs bottom has a value:
                    if (row[16] < row[21] and row[16] > row[9]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the fruitland pictured cliffs:
                        row[13] = 'FRUITLAND-PICTURED CLIFFS'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[9] != None): #if fruitland-pictured cliffs bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[9]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'KIRTLAND SHALE'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[9] == None): #if fruitland-pictured cliffs bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row                 

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #lewis shale
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[2] != None): #if lewis bottom has a value:
                    if (row[16] < row[21] and row[16] > row[2]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the lewis:
                        row[13] = 'LEWIS SHALE'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[2] != None): #if lewis bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[2]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'LEWIS SHALE'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[2] == None): #if lewis bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #cliff house member (mesaverde group)
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[3] != None): #if cliff house bottom has a value:
                    if (row[16] < row[21] and row[16] > row[3]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the cliff house:
                        row[13] = 'CLIFF HOUSE (MESAVERDE FORMATION)'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[3] != None): #if cliff house bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[3]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'CLIFF HOUSE (MESAVERDE FORMATION)'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[3] == None): #if cliff house bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row               

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #menefee member (mesaverde group)
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[1] != None): #if menefee bottom has a value:
                    if (row[16] < row[21] and row[16] > row[1]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the menefee:
                        row[13] = 'MENEFEE (MESAVERDE FORMATION)'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[1] != None): #if menefee bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[1]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'MENEFEE (MESAVERDE FORMATION)'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[1] == None): #if menefee bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row  

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #point lookout member (mesaverde group)
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[0] != None): #if point lookout bottom has a value:
                    if (row[16] < row[21] and row[16] > row[0]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the point lookout:
                        row[13] = 'POINT LOOKOUT (MESAVERDE FORMATION)'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[0] != None): #if point lookout bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[0]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'POINT LOOKOUT (MESAVERDE FORMATION)'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[0] == None): #if point lookout bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row  

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #mancos shale
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[5] != None): #if mancos bottom has a value:
                    if (row[16] < row[21] and row[16] > row[5]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the mancos:
                        row[13] = 'MANCOS SHALE'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[5] != None): #if mancos bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[5]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'MANCOS SHALE'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[5] == None): #if mancos bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row  

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #dakota sandstone
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[7] != None): #if dakota bottom has a value:
                    if (row[16] < row[21] and row[16] > row[7]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the dakota:
                        row[13] = 'DAKOTA SANDSTONE'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[7] != None): #if dakota bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[7]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'DAKOTA SANDSTONE'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[7] == None): #if dakota bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row  

with arcpy.da.UpdateCursor(inDWR, fields) as cursor: #morrison-junction creek
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[16] != None): #if bottom of perforated casing has a value:
                if (row[6] != None): #if morrison bottom has a value:
                    if (row[16] < row[21] and row[16] > row[6]): #if bottom of perforated casing is less than (ground surface - 100 ft) and greater than the bottom of the morrison:
                        row[13] = 'MORRISON-JUNCTION CREEK'
                        if (row[18] == None): #if there is no confidence value:
                            row[18] = 'high'
            elif (row[16] == None): #if bot of perforated casing is <Null>, use well depth instead:
                if (row[17] != None):
                    if (row[6] != None): #if morrison bottom has a value:    
                        if (row[17] < row[21] and row[17] > row[6]): #if bottom of perforated casing == 0, same logic as above but using well depth:
                            row[13] = 'MORRISON-JUNCTION CREEK'
                            if (row[18] == None): #if there is no confidence value:
                                row[18] = 'high'
                    elif (row[6] == None): #if morrison bottom has no value:
                        row[13] = None #aquifer = <Null>
        cursor.updateRow(row)
del cursor, row 

"""Step 4: At this point, we have 8473/11998 wells with an aquifer field, or 3525 wells without 
an aquifer field. For this next step, I'm going to focus on all of the wells that have a <Null> aquifer field, and either don't have a depth 
or have 0 for their well depth. If a well meets those criteria and is within a polygon, it will become == that aquifer.

*everything adhering to these rules is 'low' confidence"""

#Quaternary Units
#----------------
af = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\af_hydro' #artificial fill
qa = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qa_hydro' #alluvial aquifer
qac = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qac_hydro' #alluvium-colluvium, undivided
qe = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qe_hydro' #eolian deposits
qmw = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qmw_hydro' #mass wasting deposits
qta = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qta_hydro' #terrace alluvium
qgo = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qgo_hydro' #older gravels
qtu = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Quaternary\Qtu_hydro' #sinter-tufa deposits
qgds = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgds_hydro' #glacial dammed sediment
qgmk = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgmk_hydro' #glacial moraines and kames
qgd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Glacial\Qgd_hydro' #glacial drift

#Bedrock Units
#-------------
psjn = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Paleogene\PEsn_outcrop' #san jose and nacimiento aquifer
ka = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\PEKa_outcrop' #animas formation
kk = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kk_outcrop' #kirtland shale
kfp = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kfp_outcrop' #fruitland-pictured cliffs formation
kl = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kl_outcrop' #lewis shale
kmv = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kmv_outcrop' #mesaverde formation
km = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Km_outcrop' #mancos shale
kd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Cretaceous\Kdb_outcrop' #dakota sandstone/burro canyon, undivided
jmj = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Jmj_outcrop' #morrison/junction creek
jw = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Jw_outcrop' #wannakah formation
je = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Jurassic\Je_outcrop' #entrada sandstone
trd = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Triassic\trd_outcrop' #dolores formation
pc = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Permian\Pc_outcrop' #cutler formation
pphm = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Pennsylvanian\PPhm_outcrop' #hermosa group
mdli = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Middle_Paleozoics\MDli_outcrop' #middle paleozoic aquifer
pcig = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Precambrian\pC_igneous_outcrop' #igneous rock
pcm = r'N:\PROJECT\WATER\OF-19-01 La Plata Co GW\GIS\Final Hydro Units.gdb\Precambrian\pC_meta_outcrop' #metamorphic rock

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', af) #artificial fill
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'ANTHROPOGENIC DEPOSITS'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qa) #alluvial aquifer
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'ALLUVIAL AQUIFER'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qac) #alluvium-colluvium, undivided
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'ALLUVIUM-COLLUVIUM, UNDIVIDED'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qe) #eolian deposits
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'EOLIAN DEPOSITS'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qmw) #mass wasting deposits
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MASS WASTING DEPOSITS'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qta) #terrace alluvium
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'TERRACE ALLUVIUM'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgo) #older gravels
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'OLDER GRAVELS'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qtu) #sinter-tufa deposits
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'SINTER-TUFA DEPOSITS'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgds) #glacial dammed sediment
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'GLACIAL DAMMED SEDIMENT'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgmk) #glacial moraines and kames
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'GLACIAL MORAINES AND KAMES'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', qgd) #glacial drift
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'GLACIAL DRIFT'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', psjn) #san jose and nacimiento aquifer
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'SAN JOSE-NACIMIENTO'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', ka) #animas formation
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'ANIMAS-OJO ALAMO'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kk) #kirtland shale
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'KIRTLAND SHALE'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kfp) #fruitland-pictured cliffs
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MESAVERDE FORMATION'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kl) #lewis shale
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'LEWIS SHALE'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kmv) #mesaverde formation
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MESAVERDE FORMATION'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', km) #mancos shale
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MANCOS SHALE'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', kd) #dakota sandstone
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'DAKOTA SANDSTONE'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', jmj) #morrison-junction creek
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MORRISON-JUNCTION CREEK'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', jw) #wannakah formation
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'WANNAKAH FORMATION'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION') 

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', je) #entrada sandstone
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'ENTRADA SANDSTONE'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', trd) #dolores formation
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'DOLORES FORMATION'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pc) #cutler formation
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'CUTLER FORMATION'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pphm) #hermosa group
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'HERMOSA GROUP'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', mdli) #middle paleozoic aquifer
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'MIDDLE PALEOZOIC AQUIFER'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pcig) #igneous rock
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'IGNEOUS ROCK'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')  

arcpy.SelectLayerByLocation_management(inDWR, 'WITHIN', pcm) #metamorphic rock
with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] == None or row[17] == 0): #if Well depth is <Null> or well depth is zero:
                row[13] = 'METAMORPHIC ROCK'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
arcpy.SelectLayerByAttribute_management(inDWR, 'CLEAR_SELECTION')    

"""Now we've got 10574/11998 aquifers, or we still need aquifer values for 1419 of the wells.
This code filled in 88.2% of the aquifer fields. I'm going to manually enter data for 49 of these
wells (all wells <= 100 ft deep)'
1370 of these are greater than 100 ft deep, but commonly do not
have enough subsurface bottoms data to have an aquifer populated based on the code. We'll call these 'BEDROCK AQUIFER
with a low confidence value. This accounts for 11.4% of the wells (pretty good, IMO!)

*some of these wells don't lie within polygon boundaries. See FID 11166, 11167, 5961, 6975, 6982. 
I manually entered the closest polygon as the aquifer for these

*Many of these 49 wells are just over 100 ft in depth - i.e 100.1, 100.2 etc. 
So, they did not meet our criteria for surficial classification (i.e if a well is <= 100 ft deep and overlies this polygon, it is in that aquifer)
i.e some of these wells are 100.1, 100.2, etc feet deep, don't have enough subsurface data for classification, and cant be classified by the code above'
I started going through these manually to classify them as the surficial unit 
they are within, but realized they don't meet our criteria! I thought these were 
errors and wasn't sure why the code didn't pick them up. Floating point numbers, am I rite!!!!?"""

with arcpy.da.UpdateCursor (inDWR, fields) as cursor:
    for row in cursor:
        if (row[13] == None): #if aquifer field is <Null>:
            if (row[17] > 100): #if Well depth is > 100 ft below ground surface:
                row[13] = 'BEDROCK AQUIFER'
                if (row[18] == None): #if confidence is <Null>:
                    row[18] = 'low'
        cursor.updateRow(row) 
del cursor, row
