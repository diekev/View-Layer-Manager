import bpy
from bpy.types import Panel, UIList

class ViewLayerManagerPanel(Panel):
    bl_space_type = 'VIEW_LAYER_MANAGER_EDITOR'
    bl_region_type = 'WINDOW'
    # COMPAT_ENGINES must be defined in each subclass

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES)


class ViewLayerParametersPanel(ViewLayerManagerPanel):
    bl_label = "View Layer"
    bl_idname = "VIEW_LAYER_MANAGER_PT_parametres_view_layer"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH', 'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="")
        col.label(text="Use for Rendering")
        for view_layer in scene.view_layers:
            col = row.column()
            col.label(text=view_layer.name)
            col.prop(view_layer, "use", text="")


class ViewLayerCollectionsPanel(ViewLayerManagerPanel):
    bl_label = "Collections"
    bl_idname = "VIEW_LAYER_MANAGER_PT_collections_view_layer"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH', 'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        collections_names = [collection.name for collection in scene.collection.children]

        row = layout.row()
        col = row.column()
        col.label(text="")

        for name in collections_names:
            col.label(text=name)

        for view_layer in scene.view_layers:
            col = row.column()
            col.label(text=view_layer.name)
            
            for name in collections_names:
                collection = view_layer.layer_collection.children[name]
                col.prop(collection, "exclude", text="")


class ViewLayerPassesPanel(ViewLayerManagerPanel):
    bl_label = "Passes"
    bl_idname = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'CYCLES'}

    def draw(self, context):
        pass

def draw_passes_grid(view_layers, layout, props):
    row = layout.row()
    col = row.column()
    col.label(text="")

    for prop in props:
        col.label(text=prop[0])

    for view_layer in view_layers:
        col = row.column()
        col.label(text=view_layer.name)

        for prop in props:
            vl = view_layer

            if len(prop) == 3:
                args = prop[2]

                if "is_cycles" in args and args["is_cycles"]:
                    vl = vl.cycles
                elif "is_eevee" in args and args["is_eevee"]:
                    vl = vl.eevee

            col.prop(vl, prop[1], text="")


class ViewLayerDataPassesPanelCycles(ViewLayerManagerPanel):
    bl_label = "Data"
    bl_idname = "VIEW_LAYER_MANAGER_PT_data_passes_view_layer"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Combined", "use_pass_combined"),
            ("Z", "use_pass_z"),
            ("Mist", "use_pass_mist"),
            ("Position", "use_pass_position"),
            ("Normal", "use_pass_normal"),
            ("Vector", "use_pass_vector"),
            ("UV", "use_pass_uv"),
            ("Denoising Data", "denoising_store_passes", {"is_cycles":True}),
            ("Object Index", "use_pass_object_index"),
            ("Material Index", "use_pass_material_index"),
            ("Alpha Threshold", "pass_alpha_threshold"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerDataPassesPanelEEVEE(ViewLayerManagerPanel):
    bl_label = "Data"
    bl_idname = "VIEW_LAYER_MANAGER_PT_data_passes_view_layer_eevee"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Combined", "use_pass_combined"),
            ("Z", "use_pass_z"),
            ("Mist", "use_pass_mist"),
            ("Normal", "use_pass_normal"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerLightPassesPanelCycles(ViewLayerManagerPanel):
    bl_label = "Light"
    bl_idname = "VIEW_LAYER_MANAGER_PT_light_passes_view_layer"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Diffuse Direct", "use_pass_diffuse_direct"),
            ("Diffuse Indirect", "use_pass_diffuse_indirect"),
            ("Diffuse Color", "use_pass_diffuse_color"),
            ("Glossy Direct", "use_pass_glossy_direct"),
            ("Glossy Indirect", "use_pass_glossy_indirect"),
            ("Glossy Color", "use_pass_glossy_color"),
            ("Transmission Direct", "use_pass_transmission_direct"),
            ("Transmission Indirect", "use_pass_transmission_indirect"),
            ("Transmission Color", "use_pass_transmission_color"),
            ("Volume Direct", "use_pass_volume_direct", {"is_cycles":True}),
            ("Volume Indirect", "use_pass_volume_indirect", {"is_cycles":True}),
            ("Emission", "use_pass_emit"),
            ("Environment", "use_pass_environment"),
            ("Shadow", "use_pass_shadow"),
            ("Ambient Occlusion", "use_pass_ambient_occlusion"),
            ("Shadow Catcher", "use_pass_shadow_catcher", {"is_cycles":True}),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerLightPassesPanelEEVEE(ViewLayerManagerPanel):
    bl_label = "Light"
    bl_idname = "VIEW_LAYER_MANAGER_PT_light_passes_view_layer_eevee"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Diffuse Light", "use_pass_diffuse_direct"),
            ("Diffuse Color", "use_pass_diffuse_color"),
            ("Specular Light", "use_pass_glossy_direct"),
            ("Specular Color", "use_pass_glossy_color"),
            ("Volume Light", "use_pass_volume_direct", {"is_eevee":True}),
            ("Emission", "use_pass_emit"),
            ("Environment", "use_pass_environment"),
            ("Shadow", "use_pass_shadow"),
            ("Ambient Occlusion", "use_pass_ambient_occlusion"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerEffectsPassesPanelEEVEE(ViewLayerManagerPanel):
    bl_label = "Effects"
    bl_idname = "VIEW_LAYER_MANAGER_PT_effects_passes_view_layer_eevee"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Bloom", "use_pass_bloom", {"is_eevee":True}),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerCryptomattePassesPanelCycles(ViewLayerManagerPanel):
    bl_label = "Cryptomatte"
    bl_idname = "VIEW_LAYER_MANAGER_PT_cryptomatte_passes_view_layer"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Object", "use_pass_cryptomatte_object"),
            ("Material", "use_pass_cryptomatte_material"),
            ("Asset", "use_pass_cryptomatte_asset"),
            ("Levels", "pass_cryptomatte_depth"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerCryptomattePassesPanelEEVEE(ViewLayerManagerPanel):
    bl_label = "Cryptomatte"
    bl_idname = "VIEW_LAYER_MANAGER_PT_cryptomatte_passes_view_layer_eevee"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Object", "use_pass_cryptomatte_object"),
            ("Material", "use_pass_cryptomatte_material"),
            ("Asset", "use_pass_cryptomatte_asset"),
            ("Levels", "pass_cryptomatte_depth"),
            ("Accurate Mode", "use_pass_cryptomatte_accurate"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerShaderAOVPassesPanel(ViewLayerManagerPanel):
    bl_label = "Shader AOV"
    bl_idname = "VIEW_LAYER_MANAGER_PT_shader_aov_passes_view_layer"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        main_row = layout.row()

        for view_layer in scene.view_layers:
            col = main_row.column()
            col.label(text=view_layer.name)

            row = col.row()
            col = row.column()

            col.template_list("VIEWLAYER_UL_aov", "aovs", view_layer, "aovs", view_layer, "active_aov_index", rows=3)
            col = row.column()
            sub = col.column(align=True)
            sub.operator("scene.view_layer_add_aov", icon='ADD', text="")
            sub.operator("scene.view_layer_remove_aov", icon='REMOVE', text="")


class ViewLayerLightGroupsPassesPanelCycles(ViewLayerManagerPanel):
    bl_label = "Light Groups"
    bl_idname = "VIEW_LAYER_MANAGER_PT_light_groups_passes_view_layer"
    bl_parent_id = "VIEW_LAYER_MANAGER_PT_passes_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        main_row = layout.row()

        for view_layer in scene.view_layers:
            col = main_row.column()
            col.label(text=view_layer.name)

            row = col.row()
            col = row.column()
            
            col.template_list("UI_UL_list", "lightgroups", view_layer, "lightgroups", view_layer, "active_lightgroup_index", rows=3)
            col = row.column()
            sub = col.column(align=True)
            sub.operator("scene.view_layer_add_lightgroup", icon='ADD', text="")
            sub.operator("scene.view_layer_remove_lightgroup", icon='REMOVE', text="")
            sub.separator()
            sub.menu("VIEWLAYER_MT_lightgroup_sync", icon='DOWNARROW_HLT', text="")


class ViewLayerFilterPanel(ViewLayerManagerPanel):
    bl_label = "Filter"
    bl_idname = "VIEW_LAYER_MANAGER_PT_filter_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Environment", "use_sky"),
            ("Surfaces", "use_solid"),
            ("Curves", "use_strand"),
            ("Volumes", "use_volumes"),
            ("Motion Blur", "use_motion_blur"),
            ("Denoising", "use_denoising", {"is_cycles":True}),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class ViewLayerOverridePanel(ViewLayerManagerPanel):
    bl_label = "Override"
    bl_idname = "VIEW_LAYER_MANAGER_PT_override_view_layer"
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        props = (
            ("Material Override", "material_override"),
            ("Samples", "samples"),
        )

        draw_passes_grid(scene.view_layers, layout, props)


class VIEW_LAYER_MANAGER_HT_entete(bpy.types.Header):
    bl_space_type = 'VIEW_LAYER_MANAGER_EDITOR'

    def draw(self, context):
        layout = self.layout
        editeur = context.space_data

        layout.template_header()

        layout.separator_spacer()
        layout.prop(editeur, "search_filter", icon='VIEWZOOM', text="")
        layout.separator_spacer()


class VIEW_LAYER_MANAGER_UL_view_layers(UIList):
    def draw_item(self, context, layout, _data, item, icon, _active_data_, _active_propname, _index):
        view_layer = item
        editeur = context.space_data

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.emboss = 'NONE'
            layout.prop(view_layer, "name", text="")
            # layout.prop(view_layer, "group", text="")

            layout.emboss = 'NORMAL'
            # icon = 'FILE_IMAGE'
            # layout.prop(view_layer, "use_for_precomp", icon=icon, text="")

            icon = 'RESTRICT_RENDER_OFF' if view_layer.use else 'RESTRICT_RENDER_ON'
            layout.prop(view_layer, "use", text="", icon=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class VIEW_LAYER_MANAGER_OT_view_layer_remove(bpy.types.Operator):
    """Remove the currently selected view layer"""

    bl_idname = 'view_layer_manager.view_layer_remove'
    bl_label = "Remove the active view layer"

    def execute(self, context):
        scene = context.scene
        editor = context.space_data

        active_index = editor.active_view_layer
        if active_index < 0 or active_index >= len(scene.view_layers):
            return {'CANCELLED'}

        view_layer = scene.view_layers[active_index]
        scene.view_layers.remove(view_layer)
        editor.active_view_layer = len(scene.view_layers) - 1
        return {'FINISHED'}


class ViewLayerUIPanel:
    bl_space_type = 'VIEW_LAYER_MANAGER_EDITOR'
    bl_region_type = 'UI'
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES)


class VIEW_LAYER_MANAGER_PT_view_layers(ViewLayerUIPanel, Panel):
    bl_idname = "VIEW_LAYER_MANAGER_PT_view_layers"
    bl_label = "View Layers"
    bl_category = "Layers"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'CYCLES'}

    def draw(self, context):
        editeur = context.space_data
        scene = context.scene

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.template_list("VIEW_LAYER_MANAGER_UL_view_layers", "", scene, "view_layers", editeur, "active_view_layer", rows=3)

        col = row.column(align=True)
        col.operator("scene.view_layer_add", icon='ADD', text="")
        col.operator("view_layer_manager.view_layer_remove", icon='REMOVE', text="")

classes = (
    ViewLayerParametersPanel,
    ViewLayerCollectionsPanel,
    ViewLayerPassesPanel,
    ViewLayerDataPassesPanelCycles,
    ViewLayerDataPassesPanelEEVEE,
    ViewLayerLightPassesPanelCycles,
    ViewLayerLightPassesPanelEEVEE,
    ViewLayerEffectsPassesPanelEEVEE,
    ViewLayerCryptomattePassesPanelCycles,
    ViewLayerCryptomattePassesPanelEEVEE,
    # ViewLayerShaderAOVPassesPanel,
    # ViewLayerLightGroupsPassesPanelCycles,
    ViewLayerFilterPanel,
    ViewLayerOverridePanel,
    VIEW_LAYER_MANAGER_HT_entete,

    VIEW_LAYER_MANAGER_UL_view_layers,
    VIEW_LAYER_MANAGER_PT_view_layers,

    VIEW_LAYER_MANAGER_OT_view_layer_remove,
)