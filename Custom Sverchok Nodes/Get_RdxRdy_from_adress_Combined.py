# Deze code is oorspronkelijk aan een bestaande addon toegevoegd. 
# Er zijn meer acties nodig om deze daadwerkelijk te gebruiken:
# 
# bl_idname van class SvO3PointCloudCustomNode moet geregistreerd worden in de addon zelf.
# In dit geval was dat in de nodes_index.py bestand van de addon.




import bpy
from bpy.props import BoolProperty, StringProperty
from sverchok.node_tree import SverchCustomTreeNode
from GIS2BIM import *
from GIS2BIM_NL import *

class UpdateGISDataOperator(bpy.types.Operator):
    """Operator to update GIS data from the inputs."""
    bl_idname = "node.update_gis_data"
    bl_label = "Update GIS Data"

    node_name: StringProperty()

    def execute(self, context):
        node_tree = context.space_data.node_tree
        node = node_tree.nodes.get(self.node_name)

        print('knop')
        # Retrieve inputs with error handling
        try:
            stad_input = node.inputs['Stad']
            straat_input = node.inputs['Straatnaam']
            huisnummer_input = node.inputs['Huisnummer']
        
            stad = stad_input.sv_get()[0] if stad_input.is_linked else node.stad_
            straat = straat_input.sv_get()[0] if straat_input.is_linked else node.straatnaam_
            huisnummer = huisnummer_input.sv_get()[0] if huisnummer_input.is_linked else node.huisnummer_
    
            # URL encode the inputs
            stad = str(stad).strip().replace(" ", "%20")
            straat = str(straat).strip().replace(" ", "%20")
            huisnummer = str(huisnummer).strip().replace(" ", "%20")
    
            # Debug print
            print("Processed Address: Stad = {}, Straatnaam = {}, Huisnummer = {}".format(stad, straat, huisnummer))
    
            res = NL_GetLocationData(NLPDOKServerURL, stad, straat, huisnummer)
    
            # Validate the response
            if res and len(res) >= 2:
                Rdx, Rdy = res[0], res[1]
                print("Rdx = {}, Rdy = {}".format(Rdx, Rdy))
    
                if node.outputs['Rdx'].is_linked:
                    Rdx = float(Rdx)
                    node.outputs['Rdx'].sv_set([Rdx])
                    print("Updated Rdx output socket with value:", Rdx)
                else:
                    print("Rdx output socket is not linked.")
                
                if node.outputs['Rdy'].is_linked:
                    node.outputs['Rdy'].sv_set([Rdy])
                    print("Updated Rdy output socket with value:", Rdy)
                else:
                    print("Rdy output socket is not linked.")
            else:
                print("Error: Invalid address provided. Please check the Stad, Straatnaam, and Huisnummer.")
                if node.outputs['Rdx'].is_linked:
                    node.outputs['Rdx'].sv_set(["Error"])
                if node.outputs['Rdy'].is_linked:
                    node.outputs['Rdy'].sv_set(["Error"])
    
        except Exception as e:
            print(f"Exception occurred: {e}")
            if node.outputs['Rdx'].is_linked:
                node.outputs['Rdx'].sv_set(["Error"])
            if node.outputs['Rdy'].is_linked:
                node.outputs['Rdy'].sv_set(["Error"])
        return{'FINISHED'}

class SvO3PointCloudCustomNode(SverchCustomTreeNode, bpy.types.Node):
    bl_idname = 'SvO3PointCloudCustomNode'
    bl_label = 'Adres naar Rdx & Rdy'
    bl_icon = 'MESH_CUBE'

    stad_: StringProperty(name='Stad', default="Dordrecht")
    straatnaam_: StringProperty(name='Straatnaam', default="lange geldersekade")
    huisnummer_: StringProperty(name='Huisnummer', default="2")

    def sv_init(self, context):
        self.inputs.new('SvStringsSocket', "Stad").prop_name = 'stad_'
        self.inputs.new('SvStringsSocket', "Straatnaam").prop_name = 'straatnaam_'
        self.inputs.new('SvStringsSocket', "Huisnummer").prop_name = 'huisnummer_'

        self.outputs.new('SvStringsSocket', "Rdx")
        self.outputs.new('SvStringsSocket', "Rdy")
        

    def draw_buttons(self, context, layout):
        layout.operator(UpdateGISDataOperator.bl_idname, text="Update GIS Data").node_name = self.name

    def process(self):
        if self.outputs['Rdx'].is_linked:
            self.outputs['Rdx'].sv_set(["Error"])
        if self.outputs['Rdy'].is_linked:
            self.outputs['Rdy'].sv_set(["Error"])
        pass


def register():
    bpy.utils.register_class(SvO3PointCloudCustomNode)
    bpy.utils.register_class(UpdateGISDataOperator)

def unregister():
    bpy.utils.unregister_class(SvO3PointCloudCustomNode)
    bpy.utils.unregister_class(UpdateGISDataOperator)

if __name__ == "__main__":
    register()