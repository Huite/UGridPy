import numpy as np
from meshkernel import Mesh2d
from numpy.testing import assert_array_equal

from ugrid import UGrid, UGridMesh2D


def create_ugrid_mesh2d():
    r"""Creates an instance of UGridMesh2D to be used for testing"""

    name = "mesh2d"
    node_x = np.array([0, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 3, 3, 3, 3], dtype=np.double)
    node_y = np.array([0, 0, 1, 1, 2, 2, 3, 3, 0, 1, 2, 3, 0, 1, 2, 3], dtype=np.double)
    edge_node = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            2,
            9,
            4,
            10,
            6,
            11,
            8,
            12,
            9,
            13,
            10,
            14,
            11,
            15,
            12,
            16,
            1,
            3,
            3,
            5,
            5,
            7,
            2,
            4,
            4,
            6,
            6,
            8,
            9,
            10,
            10,
            11,
            11,
            12,
            13,
            14,
            14,
            15,
            15,
            16,
        ],
        dtype=np.int,
    )

    face_x = np.array([0.5, 0.5, 0.5, 1.5, 1.5, 1.5, 2.5, 2.5, 2.5], dtype=np.double)
    face_y = np.array([0.5, 1.5, 2.5, 0.5, 1.5, 2.5, 0.5, 1.5, 2.5], dtype=np.double)
    face_node = np.array(
        [
            1,
            2,
            4,
            3,
            3,
            4,
            6,
            5,
            5,
            6,
            8,
            7,
            2,
            9,
            10,
            4,
            4,
            10,
            11,
            6,
            6,
            11,
            12,
            8,
            9,
            13,
            14,
            10,
            10,
            14,
            15,
            11,
            11,
            15,
            16,
            12,
        ],
        dtype=np.int,
    )

    ugrid_mesh2d = UGridMesh2D(
        name=name,
        node_x=node_x,
        node_y=node_y,
        edge_node=edge_node,
        face_x=face_x,
        face_y=face_y,
        face_node=face_node,
    )
    return ugrid_mesh2d


def test_ugrid_mesh2d_get():
    r"""Tests `mesh2d_get_num_topologies` and `mesh2d_get` to read a mesh2d from file."""

    with UGrid("./data/OneMesh2D.nc", "r") as ug:
        num_mesh2d_topologies = ug.mesh2d_get_num_topologies()
        ugrid_mesh2d = ug.mesh2d_get(num_mesh2d_topologies - 1)

        expected_ugrid_mesh2d = create_ugrid_mesh2d()

        assert expected_ugrid_mesh2d.name == ugrid_mesh2d.name

        assert_array_equal(ugrid_mesh2d.node_x, expected_ugrid_mesh2d.node_x)
        assert_array_equal(ugrid_mesh2d.node_y, expected_ugrid_mesh2d.node_y)
        assert_array_equal(ugrid_mesh2d.edge_node, expected_ugrid_mesh2d.edge_node)

        assert_array_equal(ugrid_mesh2d.face_x, expected_ugrid_mesh2d.face_x)
        assert_array_equal(ugrid_mesh2d.face_y, expected_ugrid_mesh2d.face_y)
        assert_array_equal(ugrid_mesh2d.face_node, expected_ugrid_mesh2d.face_node)


def test_ugrid_mesh2d_define_and_put():
    r"""Tests `mesh2d_define` and `mesh2d_put` to define and write a mesh2d to file."""

    with UGrid("./data/written_files/Mesh2DWrite.nc", "w+") as ug:
        ugrid_mesh2d = create_ugrid_mesh2d()
        topology_id = ug.mesh2d_define(ugrid_mesh2d)
        assert topology_id == 0
        ug.mesh2d_put(topology_id, ugrid_mesh2d)


def test_mesh2d_meshkernel_define_and_put():
    r"""Tests a meshkernel mesh2d is correctly converted to UGridMesh2D and written to file."""
    node_x = np.array([0.0, 1.0, 1.0, 0.0], dtype=np.double)
    node_y = np.array([0.0, 0.0, 1.0, 1.0], dtype=np.double)

    edge_nodes = np.array([0, 1, 1, 2, 2, 3, 2, 0], dtype=np.int)

    face_nodes = np.array([0, 1, 2, 3], dtype=np.int)
    nodes_per_face = np.array([4], dtype=np.int)

    ugrid_mesh2d = Mesh2d(
        node_x=node_x,
        node_y=node_y,
        edge_nodes=edge_nodes,
        face_nodes=face_nodes,
        nodes_per_face=nodes_per_face,
    )

    ugrid_mesh2d = UGrid.from_meshkernel_mesh2d_to_ugrid_mesh2d(
        mesh2d=ugrid_mesh2d, name="mesh2d", is_spherical=False
    )
    with UGrid("./data/written_files/Mesh2DMesKernelWrite.nc", "w+") as ug:
        topology_id = ug.mesh2d_define(ugrid_mesh2d)
        assert topology_id == 0
        ug.mesh2d_put(topology_id, ugrid_mesh2d)


def test_ugrid_mesh2d_get_topology_attributes_names_and_values():
    r"""Tests `topology_get_attributes_names` and `topology_get_attributes_values` to read attributes names and
    values of a mesh2d topology."""

    with UGrid("./data/OneMesh2D.nc", "r") as ug:
        topology_type = ug.topology_get_mesh2d_enum()
        topology_id = 0
        attribute_names = ug.topology_get_attributes_names(topology_id, topology_type)
        attribute_values = ug.topology_get_attributes_values(topology_id, topology_type)
        assert_array_equal(
            attribute_names,
            [
                "cf_role",
                "edge_coordinates",
                "edge_dimension",
                "edge_node_connectivity",
                "face_coordinates",
                "face_dimension",
                "face_node_connectivity",
                "long_name",
                "max_face_nodes_dimension",
                "node_coordinates",
                "node_dimension",
                "topology_dimension",
            ],
        )
        assert_array_equal(
            attribute_values,
            [
                "mesh_topology",
                "mesh2d_edge_x mesh2d_edge_y",
                "mesh2d_nEdges",
                "mesh2d_edge_nodes",
                "mesh2d_face_x mesh2d_face_y",
                "mesh2d_nFaces",
                "mesh2d_face_nodes",
                "Topology data of 2D mesh",
                "mesh2d_nMax_face_nodes",
                "mesh2d_node_x mesh2d_node_y",
                "mesh2d_nNodes",
                "2",
            ],
        )
