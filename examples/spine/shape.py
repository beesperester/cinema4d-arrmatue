import c4d

from rigging.modules.shape import ObjectShape, RecursiveShape
from rigging.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

shape = ObjectShape(
    "pelvis",
    [
        NameValidator("Pelvis_Joint"),
        InstanceValidator(c4d.Ojoint)
    ],
    [
        RecursiveShape(
            ObjectShape(
                "spine",
                [
                    NameValidator("Spine*"),
                    InstanceValidator(c4d.Ojoint)
                ]
            )
        ),
        ObjectShape(
            "l_upperleg",
            [
                NameValidator("L_Upperleg_Joint"),
                InstanceValidator(c4d.Ojoint)
            ]
        ),
        ObjectShape(
            "r_upperleg",
            [
                NameValidator("R_Upperleg_Joint"),
                InstanceValidator(c4d.Ojoint)
            ]
        )
    ]
)