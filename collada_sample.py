"""
Sample script of collada.

See documentation in:
https://pycollada.readthedocs.io/en/latest/creating.html
"""

from collada import Collada, material, geometry, source, scene
import numpy


def main():
    """
    Generate .dae file.
    """

    mesh = Collada()
    effect = material.Effect(
        'effect0', [], 'phong', diffuse=(1, 0, 0), specular=(0, 1, 0))
    mat = material.Material('material0', 'mymaterial', effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    vert_floats = numpy.array([
        -50, 50, 50, 50, 50, 50, -50, -50, 50, 50,
        -50, 50, -50, 50, -50, 50, 50, -50, -50, -50,
        -50, 50, -50, -50
    ])
    normal_floats = numpy.array([
        0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
        0, 1, 0, 1, 0, 0, 1, 0, 0, 1,
        0, 0, 1, 0, 0, -1, 0, 0, -1, 0,
        0, -1, 0, 0, -1, 0, -1, 0, 0, -1,
        0, 0, -1, 0, 0, -1, 0, 0, 1, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
        0, 0, -1, 0, 0, -1, 0, 0, -1, 0,
        0, -1
    ])
    componests = ('X', 'Y', 'Z')
    vert_src = source.FloatSource('cubeverts-array', vert_floats, componests)
    normal_src = source.FloatSource('cubenormals-array', normal_floats, componests)

    input_list = source.InputList()
    input_list.addInput(0, 'VERTEX', '#cubeverts-array')
    input_list.addInput(1, 'NORMAL', '#cubenormals-array')

    indices = numpy.array([
        0, 0, 2, 1, 3, 2, 0, 0, 3, 2,
        1, 3, 0, 4, 1, 5, 5, 6, 0, 4,
        5, 6, 4, 7, 6, 8, 7, 9, 3, 10,
        6, 8, 3, 10, 2, 11, 0, 12, 4, 13,
        6, 14, 0, 12, 6, 14, 2, 15, 3, 16,
        7, 17, 5, 18, 3, 16, 5, 18, 1, 19,
        5, 20, 7, 21, 6, 22, 5, 20, 6, 22,
        4, 23
    ])

    geom = geometry.Geometry(mesh, 'geometry0', 'mycube', [vert_src, normal_src])
    triset = geom.createTriangleSet(indices, input_list, 'materialref')
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    matnode = scene.MaterialNode('materialref', mat, inputs=[])
    geomnode = scene.GeometryNode(geom, [matnode])
    node = scene.Node('node0', children=[geomnode])

    myscene = scene.Scene('myscene', [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    mesh.write('collada_sample.dae')


if __name__ == '__main__':
    main()
