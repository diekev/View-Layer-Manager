bl_info = {
    "name": "View Layer Manager",
    "author": "Kévin Dietrich",
    "version": (0, 0, 1),
    "blender": (3, 5, 0),
    "location": "Editors > View Layer Manager",
    "description": "Editor to manage all view layers of the current scene",
    "warning": "Beta",
    "category": "Editor"
}

import bpy

from . import editor
from . import ui

def register_classes(classes):
    for classe in classes:
        bpy.utils.register_class(classe)


def unregister_classes(classes):
    for classe in reversed(classes):
        bpy.utils.unregister_class(classe)


liste_des_classes = [
    editor.classes,
    ui.classes,
]

def register():
    for liste in liste_des_classes:
        register_classes(liste)

def unregister():
    for liste in reversed(liste_des_classes):
        unregister_classes(liste)