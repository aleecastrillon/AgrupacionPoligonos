import arcpy,os,subprocess,time,inspect


#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True

pGDBBorrador = arcpy.GetParameterAsText(0)
pGDBFinal = arcpy.GetParameterAsText(1)
pFeatureClassInicial = arcpy.GetParameterAsText(2)
pFieldSeleccionado = arcpy.GetParameterAsText(3)
pValorMaximo = arcpy.GetParameterAsText(4).replace(",",".")



'''infea=arcpy.GetParameterAsText(0)
infea=infea.split(";")

infea=[arcpy.Describe(x).catalogPath for x in infea]
infea=(";").join(infea)
join_atributtes=arcpy.GetParameterAsText(1)
output_type=arcpy.GetParameterAsText(2)
capa_salida=arcpy.GetParameterAsText(3)'''



#=========Funciones Auxiliares=====================#
def getPythonPath():
    pydir = sys.exec_prefix
    pyexe = os.path.join(pydir, "python.exe")
    if os.path.exists(pyexe):
        return pyexe
    else:
        raise RuntimeError("python.exe no se encuentra instalado en {0}".format(pydir))

def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

#=========Validación de requerimientos=====================#

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar= "Cod_Aux_UPRA_grouping_polygons_cursors.py"
    verPythonfinal=verPython64
# ------------------------------------------------------------

if __name__ == '__main__':
	verPython = verPythonfinal
	verPythonDir=verPython.replace("\\python.exe","")
	script=directorioyArchivo()
	script=script[1]+r"\\"+scriptAuxiliar
	arcpy.AddMessage("Ingresando...")
	comando=r"start %s %s %s %s %s %s %s"%(verPython,script, pGDBBorrador, pGDBFinal, pFeatureClassInicial, pFieldSeleccionado, pValorMaximo)
	arcpy.AddMessage(comando)
	ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
	astdout, astderr = ff.communicate()
	arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))
    
    
    