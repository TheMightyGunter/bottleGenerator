import bpy #import blender python library

#setup - choosing workspace and names
class POTIONMAKER_PT_main_panel(bpy.types.Panel):
    bl_label = "Create Potion from Curve"
    bl_idname = "POTIONMAKER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Curve to Bottle'

    def draw(self, context):
        layout = self.layout
        layout.operator("addonname.addbasic_operator")


class ADDONNAME_OT_add_basic(bpy.types.Operator):
    bl_label = "Convert Curve to Bottle"
    bl_idname = "addonname.addbasic_operator"
    
    def execute(self, context):
        
        bCurve = bpy.ops.object
        bCurveSetting = bpy.context.object
        
        bCurve.modifier_add(type='SCREW')
        bCurveSetting.modifiers["Screw"].axis = 'X' #adding screw modifier (creates bottle)
        bCurveSetting.modifiers["Screw"].use_merge_vertices = True
        
        bCurve.modifier_add(type='SOLIDIFY')
        bCurveSetting.modifiers["Solidify"].thickness = 0.04 #adding solidify modifier (creates thickness at 0.04)
        
        material_basic = bpy.data.materials.new(name = "Basic") #shading
        material_basic.use_nodes = True
        
        bpy.context.object.active_material = material_basic
        
        principled_node = material_basic.node_tree.nodes.get('Principled BSDF')
        
        material_basic.node_tree.nodes.remove(principled_node)
        
        glass_node = material_basic.node_tree.nodes.new('ShaderNodeBsdfGlass')
        
        output_node = material_basic.node_tree.nodes.get('Material Output')
        material_basic.node_tree.links.new(glass_node.outputs[0],output_node.inputs[0]) #assigning shader

        
        return{'FINISHED'}





classes = [POTIONMAKER_PT_main_panel,ADDONNAME_OT_add_basic]
 
#registering/unregistering classes 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
 
 
 
if __name__ == "__main__":
    register()