#Multiply_Raster_Match.py
#Created by Leh & Nicki 2021/03/17

import arcpy, os, glob
arcpy.CheckOutExtension("Spatial")

def main():
    ws1 = glob.glob(r'C:/Workspace/nicki/ws1_encounter_prob/*.tif')
    ws2 = glob.glob(r'C:/Workspace/nicki/ws2_lethal_prob/*.tif')
    outWs = r'C:/Workspace/nicki/output'

    multiplier(ws1, ws2, outWs)

def multiplier(ws1, ws2, outWs):
    for r in ws1:
        ws1Name = os.path.basename(r).split(".tif")[0]
        print("ws1 name is: "+ws1Name)
        r1 = arcpy.sa.Raster(r)

        for r in ws2:
            ws2Name = os.path.basename(r).split(".tif")[0]
            if not str(ws2Name) == str(ws1Name):
                continue
            print("ws2 name is: "+ws2Name)

            r2 = arcpy.sa.Raster(r)
            result = r1 * r2
            outName = ws1Name + ".tif"

            result.save(os.path.join(outWs, outName))

if __name__ =='__main__':
    main()