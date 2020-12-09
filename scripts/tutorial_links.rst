###################################### ESTA PARTE YA NO ES NECESARIA################################################
Enlaces simbólicos – Datos de entrada.
Los enlaces simbólicos, tal y como su nombre indica son enlaces que permiten acceder al contenido de una carpeta que está en un sitio sin la necesidad de copiar la carpeta en si misma. 

Para crearlos se hace lo siguiente:

ln -s \path\al\directorio\original \path\a\donde\creamos\el\enlace\

Imagina que descargamos datos de corrientes y de vientos del océano atlántico y se encuentran en la carpeta:

\home\user\datos_cmems\CMEMS_CURRENTS\uv_2020_**.nc 


Sin embargo nuestras simulaciones están en:

\home\user\PROYECTOS\CleanAtlanticSimulations\Atlantic_OceanSources

Para poder utilizar estos datos sin copiar la carpeta entera, lo ideal es hacer lo siguiente:

1) Dentro de cada simulación hay una carpeta input_data.
2) Dentro de input_data debemos separar las subcarpetas por el tipo de dato.
	-hydrodynamic
	-meteorologic
	-waves
	-waterQuality

3) Luego según el tipo de dato, nos referimos a ellas dentro del xml principal de cada simulacion.
4) Para crear el enlace a los datos hydrodinámicos hacemos lo siguiente:
	ln -s \home\user\datos_cmems\CMEMS_CURRENTS \home\user\PROYECTOS\CleanAtlanticSimulations\Atlantic_OceanSources\input_data\hydrodynamic

De esta manera, cuando nuestra simulación quiera acceder a hydrodynamic en realidad está accediendo a los datos de \home\user\datos_cmems\CMEMS_CURRENTS\uv_2020_**.nc 

