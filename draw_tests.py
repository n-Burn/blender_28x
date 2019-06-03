import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader

bl_info = {
    "name": "Simple Draw Test",
    "description": "Test of gpu drawing functions",
    "author": "nBurn",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "Search Menu > Simple Draw Test",
    "wiki_url": "",
    "category": "Development"
}


def draw_point(v1, rgba):
    coords = [v1]
    bgl.glPointSize(15)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'POINTS', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", rgba)
    batch.draw(shader)
    bgl.glPointSize(1)


def draw_line(v1, v2, rgba):
    coords = [v1, v2]
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", rgba)
    batch.draw(shader)


def draw_filled_tri():
    verts = (150, 400), (200, 450), (150, 500)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": verts})
    shader.bind()
    shader.uniform_float("color", (0.0, 0.5, 0.5, 1.0))
    batch.draw(shader)


def draw_filled_square():
    verts = (150, 300), (250, 300), (250, 350), (150, 350)
    indc = (0, 1, 2), (2, 3, 0)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": verts}, indices=indc)
    shader.bind()
    shader.uniform_float("color", (0.0, 0.5, 0.5, 1.0))
    batch.draw(shader)


def draw_hollow_square():
    verts = (150, 550), (250, 550), (250, 600), (150, 600)
    indc = (0, 1), (1, 2), (2, 3), (3, 0)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": verts}, indices=indc)
    shader.bind()
    shader.uniform_float("color", (0.0, 0.5, 0.5, 1.0))
    batch.draw(shader)


def draw_text(v1):
    font_id = 0
    font_size = 48
    dpi = 72
    blf.position(font_id, v1[0], v1[1], 0)
    blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
    blf.size(font_id, font_size, dpi)
    blf.draw(font_id, "Hello World")


def draw_callback_px(self, context):
    # draw line
    screen_point_0 = 150, 200
    screen_point_1 = 100, 100
    screen_point_2 = 300, 300
    color = 0.173, 0.545, 1.0, 1.0  # blue-ish
    draw_point(screen_point_0, color)
    draw_line(screen_point_1, screen_point_2, color)
    # other draw functions
    draw_text([200, 80])
    draw_filled_tri()
    draw_filled_square()
    draw_hollow_square()


class MyDrawTest(bpy.types.Operator):
    bl_idname = "object.my_draw_operator"
    bl_label = "Simple Draw Test"

    def modal(self, context, event):
        context.area.tag_redraw()
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            print("add-on stopped.\n")
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            print("add-on running.")  # debug
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(MyDrawTest)

def unregister():
    bpy.utils.unregister_class(MyDrawTest)

if __name__ == "__main__":
    register()

