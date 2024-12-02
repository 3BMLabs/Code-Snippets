import bpy

class main_panel(bpy.types.Panel):
    bl_label = "3BM Test Blender Addon"                         # Naam van de panel wanneer uitgeklapt
    bl_idname = "3BM_Panel_Test_PT_layout"                      # Unieke ID voor de class, gebruik de prefix 3BM_
    bl_space_type = 'VIEW_3D'                                   # In welke view deze panel tevoorschijn mag komen; Relevante opties: VIEW_3D; NODE_EDITOR; TEXT_EDITOR; INFO; TOPBAR; STATUSBAR
    bl_region_type = 'UI'                                       # Waar op de view deze panel tevoorschijn mag kopen; Opties: WINDOW; HEADER; CHANNELS; TEMPORARY; UI; TOOLS; TOOL_PROPS; ASSET_SHELF; ASSET_SHELF_HEADER; PREVIEW; HUD; NAVIGATION_BAR; EXECUTE; FOOTER; TOOL_HEADER; XR
    bl_category = "3BM Test"                                    # Naam van de Panel wanneer ingeklapt

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()                                      # Gebruik row.### om verschillende elementen in dezelfde row te plaatsen.
        col = layout.column()                                   # Hetzelfde geldt voor col.###

         
        row.label(text="Hello world!")                          # Tekst in de panel zelf
        row.label(text="Active object is: " + obj.name)         # Tekst in de panel zelf, waarbij de (onveranderlijke) data van het geselecteerde object wordt opgehaald.

        layout.prop(obj, "name")                                # Tekst in de panel zelf, waarbij de data wordt opgehaald en veranderd kan worden (.prop voor property)

        row = layout.row()                                      # Reset de layout row / maak een nieuwe row aan.
        
        row.operator("mesh.primitive_monkey_add")               # Knoppen om een aap of plane toe te voegen. 
        row.operator("mesh.primitive_plane_add")                # Vervang mesh.### voor Blender code die een andere functie uitvoert.



def register():
    bpy.utils.register_class(main_panel)                        # Voeg toe aan bestaande register functie

def unregister():
    bpy.utils.unregister_class(main_panel)                      # Voeg toe aan bestaande unregister functie