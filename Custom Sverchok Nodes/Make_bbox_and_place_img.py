# ***NIET VOLLEDIG WERKEND***

# Image plaatsen in Blender werkt nog niet. Workaround: 

# Deze code is oorspronkelijk aan een bestaande addon toegevoegd. 
# Er zijn meer acties nodig om deze daadwerkelijk te gebruiken:
# 
# bl_idname van class SvO3PointCloudCustomNode moet geregistreerd worden in de addon zelf.
# In dit geval was dat in de nodes_index.py bestand van de addon.

import bpy
from bpy.props import BoolProperty, StringProperty, FloatProperty
from sverchok.node_tree import SverchCustomTreeNode
from GIS2BIM import *
from GIS2BIM_NL import *
import os

class CreateImageOperator(bpy.types.Operator):
    """Operator to create the image from WMS request."""
    bl_idname = "node.create_image"
    bl_label = "Create Image"
    
    node_name: StringProperty()

    def execute(self, context):
        node_tree = context.space_data.node_tree
        node = node_tree.nodes.get(self.node_name)

        if node:
            node.create_image(context)  # Call the create image method
        return {'FINISHED'}

class DisplayImageOperator(bpy.types.Operator):
    """Operator to display the created image."""
    bl_idname = "node.display_image"
    bl_label = "Display Image"

    node_name: StringProperty()

    def execute(self, context):
        node_tree = context.space_data.node_tree
        node = node_tree.nodes.get(self.node_name)

        if node:
            node.load_image()  # Call the load image method
            node.create_image_plane(context)  # Create a plane to display the image
        return {'FINISHED'}

class SvO3WMSImageCustomNode(SverchCustomTreeNode, bpy.types.Node):
    bl_idname = 'SvO3WMSImageCustomNode'
    bl_label = 'WMS Image Custom'
    bl_icon = 'IMAGE_DATA'

    # Properties for the inputs
    Rdx: FloatProperty(name="Rdx", default=0.0)
    Rdy: FloatProperty(name="Rdy", default=0.0)
    breedte: FloatProperty(name="Breedte", default=400.0)
    hoogte: FloatProperty(name="Hoogte", default=400.0)
    tempfilelocation: StringProperty(name="Tempfile Location", default="C:/TEMP/test.jpg")

    def sv_init(self, context):
        self.inputs.new('SvStringsSocket', "Rdx").prop_name = "Rdx"
        self.inputs.new('SvStringsSocket', "Rdy").prop_name = "Rdy"
        self.inputs.new('SvStringsSocket', "Breedte").prop_name = "breedte"
        self.inputs.new('SvStringsSocket', "Hoogte").prop_name = "hoogte"
        self.inputs.new('SvStringsSocket', "Tempfile Location").prop_name = "tempfilelocation"
        
        self.outputs.new('SvStringsSocket', "Image Path")

    def draw_buttons(self, context, layout):
        layout.prop(self, "tempfilelocation")  # Display the tempfile location input
        layout.operator(CreateImageOperator.bl_idname, text="Create Image").node_name = self.name
        layout.operator(DisplayImageOperator.bl_idname, text="Display Image").node_name = self.name

    def process(self):
        # Handle data when the node tree is updated
        if self.inputs["Rdx"].is_linked:
            self.Rdx = self.inputs["Rdx"].sv_get()[0]
        if self.inputs["Rdy"].is_linked:
            self.Rdy = self.inputs["Rdy"].sv_get()[0]
        if self.inputs["Breedte"].is_linked:
            self.breedte = self.inputs["Breedte"].sv_get()[0]
        if self.inputs["Hoogte"].is_linked:
            self.hoogte = self.inputs["Hoogte"].sv_get()[0]
        if self.inputs["Tempfile Location"].is_linked:
            self.tempfilelocation = self.inputs["Tempfile Location"].sv_get()[0]

        # Ensure that you process the image creation if the inputs are valid
        if self.Rdx and self.Rdy and self.breedte and self.hoogte and self.tempfilelocation:
            self.create_image(bpy.context)

    def create_image(self, context):
        # Ensure the directory exists before creating the image
        directory = os.path.dirname(self.tempfilelocation)
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it does not exist

        # Create the image based on the properties
        bbox = GisRectBoundingBox().Create(self.Rdx, self.Rdy, self.breedte, self.hoogte, 0)
        tempfile = self.tempfilelocation

        # Call WMSRequest to create the image
        image_created = WMSRequest(NLPDOKLuchtfoto2021, bbox.boundingBoxString, tempfile, 3000, 3000)

        if os.path.exists(tempfile):
            self.outputs["Image Path"].sv_set([tempfile])
            print(f"Image created successfully at {tempfile}")
        else:
            print("Image creation failed. Tempfile not found.")

    def load_image(self):
        # Load and display the image in Blender
        if os.path.exists(self.tempfilelocation):
            if bpy.data.images.get("WMS Image"):
                bpy.data.images.remove(bpy.data.images["WMS Image"])
            img = bpy.data.images.load(self.tempfilelocation)
            img.name = "WMS Image"
            print(f"Image successfully loaded from {self.tempfilelocation}")
        else:
            print("No image found to load.")

    def create_image_plane(self, context):
    # Ensure the image file exists
        if os.path.exists(self.tempfilelocation):
            # Ensure the Image Import Add-on is enabled
            if not bpy.ops.image.import_as_mesh_planes.poll():
                bpy.ops.preferences.addon_enable(module="io_import_images_as_planes")
            
            # Import the image as a mesh plane
            bpy.ops.image.import_as_mesh_planes(
                relative=False,
                filepath=self.tempfilelocation,
                files=[{"name": os.path.basename(self.tempfilelocation), "name": os.path.basename(self.tempfilelocation)}],
                directory=os.path.dirname(self.tempfilelocation),
            )
            print("Image successfully imported and displayed as a textured plane.")
        else:
            print("Image file not found. Ensure it was created before trying to display it.")

def register():
    bpy.utils.register_class(SvO3WMSImageCustomNode)
    bpy.utils.register_class(CreateImageOperator)
    bpy.utils.register_class(DisplayImageOperator)

def unregister():
    bpy.utils.unregister_class(SvO3WMSImageCustomNode)
    bpy.utils.unregister_class(CreateImageOperator)
    bpy.utils.unregister_class(DisplayImageOperator)

if __name__ == "__main__":
    register()
