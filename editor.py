import bpy
from bpy.types import Region
from bpy.props import IntProperty

# Tag the given region for a redraw.
# Notably used for the message bus.
def require_region_redraw(region: bpy.types.Region):
    region.tag_redraw()

# Base class for the editor's regions.
class ViewLayerManagerRegion(Region):
    bl_space_type = 'VIEW_LAYER_MANAGER_EDITOR'


class ViewLayerManagerHeaderRegion(ViewLayerManagerRegion):
    bl_region_type = 'HEADER'

    def init(self, window_manager):
        Region.header_init(self)

class ViewLayerManagerUIRegion(ViewLayerManagerRegion):
    bl_region_type = 'UI'

    def init(self, window_manager):
        Region.panels_init(window_manager, self)

class ViewLayerManagerWindowRegion(ViewLayerManagerRegion):
    bl_region_type = 'WINDOW'

    def init(self, window_manager):
        Region.panels_init(window_manager, self)

        types = (bpy.types.ViewLayer, bpy.types.LayerCollection, bpy.types.Collection)

        for t in types:
            bpy.msgbus.subscribe_rna(
                key=t,
                owner=self,
                args=(self, ),
                notify=require_region_redraw,
            )
        
        bpy.msgbus.subscribe_rna(
            key=(bpy.types.Scene, "view_layers"),
            owner=self,
            args=(self, ),
            notify=require_region_redraw,
        )

# Update function for the query string.
# self is the editor.
def update_search_filter(self, context):
    self.search_filter_update()


class ViewLayerManagerSpace(bpy.types.Space):
    bl_idname = 'VIEW_LAYER_MANAGER_EDITOR'
    bl_label = 'View Layer Manager'
    bl_icon = 'RENDER_RESULT'

    search_filter: bpy.props.StringProperty(name="Search Filter", update=update_search_filter, options={'TEXTEDIT_UPDATE'})

    # Property for the active view layer in the UIList.
    active_view_layer: IntProperty()

    def search_filter_get(self, region):
        return self.search_filter


classes = (
    ViewLayerManagerSpace,
    ViewLayerManagerHeaderRegion,
    ViewLayerManagerUIRegion,
    ViewLayerManagerWindowRegion,
)