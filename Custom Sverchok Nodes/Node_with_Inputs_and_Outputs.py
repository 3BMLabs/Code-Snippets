class SvO3PointCloudCustomNode(SverchCustomTreeNode, bpy.types.Node):
    bl_idname = 'SvO3PointCloudCustomNode'
    bl_label = 'Adres naar Rdx & Rdy'
    bl_icon = 'MESH_CUBE'

    def sv_init(self, context):
        self.inputs.new('SvStringsSocket', "Stad").prop_name = 'stad_'
        self.inputs.new('SvStringsSocket', "Straatnaam").prop_name = 'straatnaam_'
        self.inputs.new('SvStringsSocket', "Huisnummer").prop_name = 'huisnummer_'

        self.outputs.new('SvStringsSocket', "Rdx")
        self.outputs.new('SvStringsSocket', "Rdy")