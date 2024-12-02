# Maak een nieuwe add-on aan zonder enige functionaliteit. 
# Plaats deze in de "C:\Users\Gebruiker\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons" folder. 
# Herstart Blender en activeer de add-on.

bl_info = {
    "name"          : "Test - Addon - Blender",
    "author"        : "W.J. Roodhorst",
    "description"   : "3BM Bouwkundig Ingenieursbureau custom Blender Add-ons for developing Bonsai",
    "version"       : (0,0,1),
    "blender"       : (4,2,1),
    "location"      : "Right 3D-View Panel -> 3BM Addon",
    "category"      : "Unknown"
    }

def register():
    print('///// 3BM Test Blender Addon /////')

def unregister():
    print('/// 3BM Test Blender Addon Unregistered ///')