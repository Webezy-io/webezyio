import pluggy

hookimpl = pluggy.HookimplMarker("webezyio")
"""Marker to be imported and used in plugins (and for own implementations)"""
plugins_hookimpl = pluggy.HookimplMarker("plugins")
