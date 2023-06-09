from math import pi

masse_max = 1200                #g

masse_volumique = 2.7           #g/cm^3
masse_volumique_Acier = 7.85    #g/cm^3

module_Young_Al = 65            #GPa
module_Young_Acier = 210        #GPa


rayon_plaque_mince = 4 *2.54/2
epaisseur_plaque_mince = 1/8 *2.54

epaisseur_base = 1.75*2.54




masse_plaque_mince = (pi*(rayon_plaque_mince**2)*epaisseur_plaque_mince)*masse_volumique

masse_base = (pi*(rayon_plaque_mince**2)*epaisseur_base)*masse_volumique


masse_restante_vis = ((masse_max-masse_plaque_mince)-masse_base)

print('masse restante:', masse_restante_vis,'\nmasse plaque mince:', masse_plaque_mince,'\nmasse base:', masse_base)
